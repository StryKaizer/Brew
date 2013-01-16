# Puppet config based on https://github.com/tsteur/django-dev-vm

Exec {
  path => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
}

exec { 'make_update':
    command => 'sudo apt-get update',
}

# Setup MySQL
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


# # Setup Memcached
# package {
#   'memcached': 
#     ensure   => latest,
#     require  => Exec['make_update'],
# }

# service { "memcached":
#   ensure  => running,
#   enable  => true,
#   require => Package['memcached'];
# }

# Install required Packages
package {
['git-core', 'curl', 'facter']:
  ensure   => latest,
  require  => Exec['make_update'],
}

# package {
#   ['python-pip', 'python-software-properties', 'python-setuptools', 'python-memcache', 'python-dev', 'build-essential']:
#     ensure   => latest,
#     require  => Exec['make_update'];
# }

package {
['python-pip', 'python-setuptools', 'python-dev', 'build-essential']:
  ensure   => latest,
  require  => Exec['make_update'];
}

package {
'Django':
  ensure   => '1.4.1',
  provider => pip,
  require  => [ Package['python-pip'], Package['python-setuptools'] ],
}

package {
'django-dajaxice':
  ensure   => '0.2',
  provider => pip,
  require  => [ Package['python-pip'], Package['python-setuptools'] ],
}

package {
'django-celery':
  ensure   => '3.0.4',
  provider => pip,
  require  => [ Package['python-pip'], Package['python-setuptools'] ],
}

package {
'django-extensions':
  ensure   => '1.0.2',
  provider => pip,
  require  => [ Package['python-pip'], Package['python-setuptools'] ],
}

# GUNICORN
package {
['gunicorn', ]:
  ensure   => latest,
  provider => pip,
  require  => [ Package['python-pip'], Package['python-setuptools'] ],
}


# NGINX
class { 'nginx': 
  require => Exec['make_update'],
}

nginx::resource::vhost { 'brew.pi':
  ensure   => present,
  proxy => 'http://127.0.0.1:8888',
}

# nginx::resource::vhost { 'brew.pi':
#   ensure   => present,
#   www_root => '/brew/djangoproject',
# }

nginx::resource::location { 'brew.pi':
 ensure   => present,
 www_root => '/brew/djangoproject/brew/static',
 location => '/static',
 vhost    => 'brew.pi',
}