from fabric.api import *

env.hosts = ['33.33.33.10']
env.password = 'vagrant'
env.user = 'vagrant'

def bootstrap():
    sudo('apt-get update')
    sudo('easy_install -U distribute')

    put('puppet.tgz', '/tmp/puppet.tgz')

    sudo('rm -rf /etc/puppet')
    with cd('/etc'):
        sudo('tar xfz /tmp/puppet.tgz')
    sudo('puppet apply /etc/puppet/manifests/server.pp')

def deploy():
    put('dist/plug-latest.tar.gz', '/tmp/plug.tar.gz')
    sudo('pip install /tmp/plug.tar.gz')

    sudo('rm -rf /srv/plug')
    put('plug.plug', '/tmp/plug.plug')
    sudo('plug install --plug=/tmp/plug.plug')

    sudo('plug setup --plug=plug.plug')
