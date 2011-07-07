from fabric.api import *
import time

env.hosts = ['33.33.33.10']
env.password = 'vagrant'
env.user = 'vagrant'

def bootstrap():
    sudo('apt-get update')

    put('puppet.tgz', '/tmp/puppet.tgz')

    sudo('rm -rf /etc/puppet')
    with cd('/etc'):
        sudo('tar xfz /tmp/puppet.tgz')
    sudo('puppet apply /etc/puppet/manifests/server.pp')

    sudo('easy_install -U distribute')

def deploy():
    put('dist/plug-latest.tar.gz', '/tmp/plug.tar.gz')
    sudo('pip install /tmp/plug.tar.gz')

def test():
    #sudo('rm -rf /srv/plug')
    put('*.plug', '/tmp')
    sudo('plug install --plug=/tmp/plug-0.1.0.server1.plug')
    sudo('plug setup --plug=plug-0.1.0.server1.plug')
    #sudo('plug install --plug=/tmp/plug-0.1.0.server2.plug')
    #sudo('plug setup --plug=plug-0.1.0.server2.plug')
    sudo('plug list')
    time.sleep(1)
    sudo('plug status')
