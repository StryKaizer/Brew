# Puppet config based on https://github.com/tsteur/django-dev-vm

Exec {
  path => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
}

exec { 'make_update':
    command => 'sudo apt-get update',
}


# Custom packages
package {
['git-core', 'facter']:
  ensure   => latest,
  require  => Exec['make_update'],
}

# MYSQL
class { 'mysql': 
require => Exec['make_update'],
}

class { 'mysql::server':
config_hash => { 'root_password' => $db_root_password },
require     => Exec['make_update'],
}

class { 'mysql::python': 
require => Exec['make_update'],
}

mysql::db { $db_name:
user     => $db_username,
password => $db_password,
host     => 'localhost',
grant    => ['all'],
}


# PYTHON
class { 'python':
  version    => '2.7',
  dev        => true,
  virtualenv => true,
  gunicorn   => true,
}

# WARNING: ve directory needs to be outside vagrant shared folder (virtualbox issue)
python::virtualenv { '/brew-ve':
  ensure       => present,
  version      => '2.7',
  # requirements => '/brew/djangoproject/requirements.txt',  # For some reason this doesnt work
}

python::requirements { '/brew/djangoproject/requirements.txt':
  virtualenv => '/brew-ve',
}

# Create static directory
file { "/brew/static":
    ensure => "directory",
}


# NGINX
class { 'nginx': 
  require => Exec['make_update'],
}

nginx::resource::vhost { 'brew.pi':
  ensure   => present,
  proxy => 'http://127.0.0.1:8000',
}

nginx::resource::location { 'brew.pi':
 ensure   => present,
 www_root => '/brew/static',
 location => '/static',
 vhost    => 'brew.pi',
}