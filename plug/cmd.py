from optparse import OptionParser
import os.path
import shlex
import subprocess

parser = OptionParser()
parser.add_option('-p', '--package', dest='package', help='Source package')

def create():
    (options, args) = parser.parse_args()
    print options, args
    short_package = os.path.split(options.package)[1]
    commands = [
        'rm -rf tmp',
        'virtualenv --no-site-packages --distribute tmp',
        'mkdir -p tmp/plug_package_cache',
        'tmp/bin/easy_install -U distribute',
        'tmp/bin/pip install --no-install --download-cache=tmp/plug_package_cache {0}'.format(options.package),
        'cp {0} tmp/{1}'.format(options.package, short_package),
        'tar cfz {0}.plug tmp/plug_package_cache tmp/{0}'.format(short_package),
    ]

    for command in commands:
        print command
        print
        cmd_args = shlex.split(command)
        p = subprocess.Popen(cmd_args)
        p.wait()