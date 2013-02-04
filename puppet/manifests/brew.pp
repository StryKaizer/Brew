# $project_name = 'djangoproject'
# $django_dir = '/brew-prject/djangoproject'
# $django_url = 'brew.pi'
# $db_username = 'brew'
# $db_password = 'brew'
# $db_name = 'brew'
# $db_root_password = 'brew'

Exec {
  path => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
}

exec { 'make_update':
    command => 'sudo apt-get update',
}


# Custom packages
package {
['git-core', 'facter', 'nano', 'libmysqlclient-dev']:
  ensure   => latest,
  require  => Exec['make_update'],
}





### MYSQL ###

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



### PYTHON ###
class { 'python':
  version    => '2.7',
  dev        => true,
  virtualenv => true,
  # gunicorn   => true,
}

# WARNING: Due to virtualbox issue, virtual environment directory needs to be outside our vagrant shared folder
python::virtualenv { '/brew-ve':
  ensure       => present,
  version      => '2.7',
  require => Class['python'],
}

python::requirements { '/brew-project/djangoproject/requirements.txt':
  virtualenv => '/brew-ve',
  require => Python::Virtualenv['/brew-ve'],
}

# Create static directory
file { "/brew-static":
    ensure => "directory",
    before => Exec['collectstatic'],
}

# Generate static content
exec{ 'collectstatic':
  command => '/brew-ve/bin/python /brew-project/djangoproject/manage.py collectstatic --noinput',
  require => Python::Requirements['/brew-project/djangoproject/requirements.txt'],
}


### SUPERVISOR, for running gunicorn and gevent ###
package { 'supervisor': 
    ensure  => '3.0b1',
    provider => pip,
}

file { '/etc/supervisord.conf':
  ensure => file,
  mode   => 600,
  source => '/brew-project/puppet/manifests/supervisord.conf',
  require => Package['supervisor'],
}

exec { 'supervisord':
    command => 'supervisord',
    require => File['/etc/supervisord.conf']
}


### NGINX ###
class { 'nginx': 
  require => Exec['make_update'],
}

nginx::resource::vhost { 'brew.pi':
  ensure   => present,
  proxy => 'http://127.0.0.1:8000',
}

nginx::resource::location { 'brew.pi':
 ensure   => present,
 location => '/static/',
 location_alias => '/brew-static/',
 vhost    => 'brew.pi',
}