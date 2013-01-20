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

# Create static directory
file { "/brew-static":
    ensure => "directory",
}

# PYTHON
class { 'python':
  version    => '2.7',
  dev        => true,
  virtualenv => true,
  gunicorn   => true,
}

# WARNING: Due to virtualbox issue, virtual environment directory needs to be outside our vagrant shared folder
python::virtualenv { '/brew-ve':
  ensure       => present,
  version      => '2.7',
}

python::requirements { '/brew-project/djangoproject/requirements.txt':
  virtualenv => '/brew-ve',
  require => Python::Virtualenv['/brew-ve'],
}

python::gunicorn { 'vhost':
  ensure      => present,
  virtualenv  => '/brew-ve',
  mode        => 'django',
  dir         => '/brew-project/djangoproject',
  bind        => '127.0.0.1:8000',
  environment => 'prod',
  template    => 'python/gunicorn.erb',
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
 www_root => '/brew-static',
 location => '/static',
 vhost    => 'brew.pi',
}