from optparse import OptionParser
import os.path
import shlex
import subprocess

parser = OptionParser()
parser.add_option('--package', dest='package', help='Source package')
parser.add_option('--plug', dest='plug', help='Plug Path')

def create(options):
    short_package = os.path.split(options.package)[1]
    commands = [
        'rm -rf tmp',
        'virtualenv --no-site-packages --distribute tmp',
        'mkdir -p tmp/plug_package_cache',
        'tmp/bin/easy_install -U distribute',
        'tmp/bin/pip install --no-install --download-cache=tmp/plug_package_cache {0}'.format(options.package),
        'cp {0} tmp/package.tgz'.format(options.package, short_package),
        'cp plug.config tmp/plug.config',
        'tar cfz {0}.plug tmp/plug_package_cache tmp/package.tgz tmp/plug.config'.format(short_package),
    ]
    run_commands(commands)


def install(options):
    short_plug = os.path.split(options.plug)[1]
    plug_path = plug_path_for_plug_name(short_plug)

    commands = [
        'mkdir -p "{0}"'.format(plug_path),
        'tar -xf {0} -C "{1}" --strip-components 1'.format(options.plug, plug_path),
    ]

    run_commands(commands)


def run_commands(commands):
    for command in commands:
        print
        print command
        cmd_args = shlex.split(command)
        p = subprocess.Popen(cmd_args)
        p.wait()


def plug_path_for_plug_name(plug_name):
    return '/srv/plug/plugs/{0}'.format(plug_name)


def plug_path_for_running_plug(plug_name):
    return '{0}/{1}'.format(plug_running_path(), plug_name)


def plug_running_path():
    return '/srv/plug/running_plug'


def setup(options):
    plug_name = options.plug
    plug_path = plug_path_for_plug_name(plug_name)
    running_plug = plug_path_for_running_plug(plug_name)

    run = """#!/bin/sh

ROOT={0}
PID=/var/run/{1}

APP=main:application

if [ -f $PID ]; then rm $PID; fi

cd $ROOT
exec $ROOT/bin/python
""".format(running_plug, plug_name)

    commands = [
        'mkdir -p {0}'.format(running_plug),
        'cp -r {0} {1}'.format(plug_path, plug_running_path()),
        'virtualenv --no-site-packages --distribute {0}'.format(running_plug),
        '{0}/bin/easy_install -U distribute'.format(running_plug),
        '{0}/bin/pip install {0}/package.tgz --download-cache={0}/plug_package_cache'.format(running_plug),
    ]
    run_commands(commands)

    with open('{0}/run'.format(running_plug), 'w') as run_file:
        run_file.write(run)

    commands = [
        'chmod +x {0}/run'.format(running_plug),
        'ln -s {0} /etc/sv/{1}'.format(running_plug, plug_name),
        'ln -s /etc/service/{0} /etc/sv/{0}'.format(plug_name),
    ]
    run_commands(commands)


def main():
    (options, args) = parser.parse_args()
    print options, args
    funcs = {
        'create': create,
        'install': install,
        'setup': setup,
    }
    funcs[args[0]](options)
