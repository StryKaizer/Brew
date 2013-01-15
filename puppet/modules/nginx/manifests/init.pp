class nginx {

    exec { "nginx update" :
        command => '/usr/bin/apt-get update',
    }

    package { [
            "nginx",
        ]:
        ensure => present,
        require => Exec["nginx update"],
    }

}