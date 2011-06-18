from optparse import OptionParser
import os.path
import shlex
import subprocess

parser = OptionParser()
parser.add_option('-p', '--package', dest='package', help='Source package')

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

    for command in commands:
        print command
        print
        cmd_args = shlex.split(command)
        print
        print command
        p = subprocess.Popen(cmd_args)
        p.wait()

def main():
    (options, args) = parser.parse_args()
    print options, args
    if args[0] == 'create': create(options)
