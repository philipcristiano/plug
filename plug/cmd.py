from optparse import OptionParser
import os.path
import shlex
import subprocess

parser = OptionParser()
parser.add_option('--package', dest='package', help='Source package')
parser.add_option('--plug', dest='plug', help='Plug Path')


## Plug Commands

def cmd_create(options):
    short_package = os.path.split(options.package)[1]
    commands = [
        remove_directory('tmp'),
        create_virtual_env('tmp'),
        make_directory('tmp/plug_package_cache'),
        update_distribute('tmp'),
        download_dependencies('tmp', options.packge),
        copy(options.package, 'tmp/package.tgz'),
        copy('plug.config', 'tmp/plug.config'),
        'tar cfz {0}.plug tmp/plug_package_cache tmp/package.tgz tmp/plug.config'.format(short_package),
    ]
    run_commands(commands)


def cmd_install(options):
    short_plug = os.path.split(options.plug)[1]
    plug_path = plug_path_for_plug_name(short_plug)

    commands = [
        make_directory(plug_path),
        extract_plug(options.plug, plug_path),
    ]

    run_commands(commands)


def cmd_setup(options):
    plug_name = options.plug
    plug_path = plug_path_for_plug_name(plug_name)
    running_plug = plug_path_for_running_plug(plug_name)

    run = runit_run_script(running_plug, 'bin/python')

    commands = [
        make_directory(running_plug),
        copy(plug_path, plug_running_path()),
        create_virtual_env(running_plug),
        update_distribute(running_plug),
        install_package(running_plug),
    ]
    run_commands(commands)

    with open('{0}/run'.format(running_plug), 'w') as run_file:
        run_file.write(run)

    commands = [
        'chmod +x {0}/run'.format(running_plug),
        remove_directory('/etc/sv/{0}'.format(plug_name),
        remove_directory('/etc/service/{0}'.format(plug_name),
        'ln -s {0} /etc/sv/{1}'.format(running_plug, plug_name),
        'ln -s /etc/sv/{0} /etc/service/{0}'.format(plug_name),
    ]
    run_commands(commands)

## Internal Commands

def copy(src, dst):
    return 'cp -r "{0}" "{1}"'.format(src, dst)

def create_virtual_env(path):
    return 'virtualenv --no-site-packages --distribute {0}'.format(path)

def download_dependencies(path, package):
    return '{0}/bin/pip install --no-install --download-cache=tmp/plug_package_cache {1}'.format(path, options.package),

def extract_plug(plug, path):
    return  'tar -xf {0} -C "{1}" --strip-components 1'.format(plug, path)

def install_package(path):
    return '{0}/bin/pip install {0}/package.tgz --download-cache={0}/plug_package_cache'.format(path),

def make_directory(path):
    return 'mkdir -p {0}'.format(path)

def remove_directory(path):
    return 'rm -rf {0}'.format(path)

def runit_run_script(root_path, command):
    return """#!/bin/sh

ROOT={0}
COMMAND={1}

cd $ROOT
exec $ROOT/$COMMAND
""".format(root_path, command)

def update_distribute(path):
    return '{0}/bin/easy_install -U distribute'.format(path)

## Path Generation

def plug_path_for_plug_name(plug_name):
    return '/srv/plug/plugs/{0}'.format(plug_name)

def plug_path_for_running_plug(plug_name):
    return '{0}/{1}'.format(plug_running_path(), plug_name)

def plug_running_path():
    return '/srv/plug/running_plug'

def run_commands(commands):
    for command in commands:
        print
        print command
        cmd_args = shlex.split(command)
        p = subprocess.Popen(cmd_args)
        p.wait()

def main():
    (options, args) = parser.parse_args()
    funcs = {
        'create': cmd_create,
        'install': cmd_install,
        'setup': cmd_setup,
    }
    funcs[args[0]](options)
