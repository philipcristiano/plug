
class lucid64 {
  exec { "Update APT":
    command => "/usr/bin/apt-get -q -q update",
  }

  user { "plug_user":
    comment => 'This user was created by Puppet',
    ensure => 'present',
  }

  package { "runit":
    ensure => present,
  }

  package { "python-pip":
    ensure => present,
  }

  package { "python-distribute":
    ensure => present,
  }

  package { "python-virtualenv":
    ensure => present,
  }

  package { "git-core":
    ensure => present,
  }
}
include lucid64
