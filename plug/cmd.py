from configobj import ConfigObj
from optparse import OptionParser
import os
import os.path
import shlex
import subprocess
import sys

parser = OptionParser()
parser.add_option('--number', dest='number', help='Number of instances', default="1")


## Plug Commands

def cmd_create(options, package):
    short_package = os.path.split(package)[1]
    short_package = short_package.split('.tar.gz')[0]
    commands = [
        remove_directory('tmp'),
        create_virtual_env('tmp'),
        make_directory('tmp/plug_package_cache'),
        update_distribute('tmp'),
        download_dependencies('tmp', package),
        copy(package, 'tmp/package.tgz'),
    ]
    run_commands(commands)

    config = ConfigObj('plug.config')
    for name, settings in config.items():
        plug_config = ConfigObj('tmp/plug.config')
        plug_config.update(settings)
        plug_config.write()
        commands = [
            'tar cfz {0}.{1}.plug tmp/plug_package_cache tmp/package.tgz tmp/plug.config'.format(short_package, name),
        ]
        run_commands(commands)


def cmd_install(options, plug):
    plug_name = os.path.split(plug)[1]
    if plug_name in installed_plugs():
        cmd_uninstall(options, plug_name)
    plug_path = installed_plug_path(plug_name)

    commands = [
        make_directory(plug_path),
        extract_plug(plug, plug_path),
        create_virtual_env(plug_path),
        update_distribute(plug_path),
        install_package(plug_path),
    ]

    run_commands(commands)

    plug_config = get_config_for_plug(plug_name)
    command = plug_config['command']
    user = plug_config['user']

    run = runit_run_script(plug_path, command, user)

    with open('{0}/run'.format(plug_path), 'w') as run_file:
        run_file.write(run)

    commands = [
        'chmod +x {0}/run'.format(plug_path),
        chown(user, plug_path),
    ]
    run_commands(commands)


def cmd_setup(options, plug):
    plug_name = plug
    instance_number = int(options.number)
    plug_path = installed_plug_path(plug_name)
    user = get_config_for_plug(plug_name)['user']
    for i in range(instance_number):
        instance_name = '{0}.{1}'.format(plug_name, i)
        instance_path = instance_plug_path(plug_name, i)
        commands = [
            make_directory('/srv/plug/plug_instances'),
            remove_directory(instance_path),
            copy(plug_path, instance_path),
            chown(user, instance_path),
            link(instance_path, '/etc/sv/{0}'.format(instance_name)),
            link('/etc/sv/{0}'.format(instance_name), '/etc/service/{0}'.format(instance_name))
        ]
        run_commands(commands)

def cmd_status(options):
    for service in sorted(os.listdir('/etc/service')):
        if os.path.exists(os.path.join('/etc/service', service, 'plug.config')):
            print_command('sv status {0}'.format(service))


def cmd_list(options):
    for item in installed_plugs():
        print item

def cmd_uninstall(options, plug):
    if not plug in installed_plugs():
        print 'That plug is not installed, for a list of install plugs run `plug list`'
        return
    commands = [
        remove_directory(installed_plug_path(plug)),
    ]
    for directory in ['/etc/service', '/etc/sv', '/srv/plug/plug_instances']:
        for service in sorted(os.listdir(directory)):
            if service.startswith(plug):
                if directory == '/etc/service':
                    commands.append('sv stop {0}'.format(service))
                service_path = '{0}/{1}'.format(directory, service)
                commands.append(remove_directory(service_path))
    run_commands(commands)

## Internal Commands
def chown(user, path):
    return 'chown -R {0} "{1}"'.format(user, path)

def copy(src, dst):
    return 'cp -r {0} {1}'.format(src, dst)

def get_config_for_plug(plug_name):
    return ConfigObj(installed_plug_path(plug_name) + '/plug.config')

def create_virtual_env(path):
    return 'virtualenv --no-site-packages --distribute {0}'.format(path)

def download_dependencies(path, package):
    return '{0}/bin/pip install --no-install --download-cache=tmp/plug_package_cache {1}'.format(path, package)

def extract_plug(plug, path):
    return  'tar -xf {0} -C "{1}" --strip-components 1'.format(plug, path)

def install_package(path):
    return '{0}/bin/pip install {0}/package.tgz --download-cache={0}/plug_package_cache'.format(path)

def installed_plugs():
    return sorted(os.listdir(install_path()))

def link(src, dst):
    return 'ln -fs "{0}" "{1}"'.format(src, dst)

def make_directory(path):
    return 'mkdir -p {0}'.format(path)

def move(src, dst):
    return 'mv "{0}" "{1}"'.format(src, dst)

def remove_directory(path):
    return 'rm -rf {0}'.format(path)

def runit_run_script(root_path, command, user):
    return """#!/bin/sh

exec su {2} -c "cd {0}; {0}/{1}"
""".format(root_path, command, user)

def update_distribute(path):
    return '{0}/bin/easy_install -U distribute'.format(path)

## Path Generation
def installed_plug_path(plug_name):
    return '{0}/{1}'.format(install_path(), plug_name)

def instance_plug_path(plug_name, number):
    return '/srv/plug/plug_instances/{0}.{1}'.format(plug_name, number)

def install_path():
    return '/srv/plug/plugs'

def run_commands(commands):
    for command in commands:
        print
        print command
        cmd_args = shlex.split(command)
        p = subprocess.Popen(cmd_args)
        assert p.wait() == 0, 'There was an error running this command'

def print_command(command):
    cmd_args = shlex.split(command)
    p = subprocess.Popen(cmd_args, stdout=sys.stdout)
    p.wait()


def main():
    (options, args) = parser.parse_args()
    funcs = {
        'create': cmd_create,
        'install': cmd_install,
        'setup': cmd_setup,
        'status': cmd_status,
        'list': cmd_list,
        'uninstall': cmd_uninstall,
    }
    funcs[args[0]](options, *args[1:])
