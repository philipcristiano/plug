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


def run_commands(commands):
    for command in commands:
        print
        print command
        cmd_args = shlex.split(command)
        p = subprocess.Popen(cmd_args)
        p.wait()


def install(options):
    plug_path = '/srv/plug/plugs/{0}'.format(options.plug)
    commands = [
        'mkdir -p "{0}"'.format(plug_path),
        'tar -xf {0} -C "{1}" --strip-components 1'.format(options.plug, plug_path),
    ]

    run_commands(commands)



def main():
    (options, args) = parser.parse_args()
    print options, args
    funcs = {
        'create': create,
        'install': install,
    }
    funcs[args[0]](options)
