# -*- mode: ruby -*-
# vi: set ft=ruby :

PROJECT_NAME = 'djangoproject'
MOUNT_POINT  = '/brew-project'

Vagrant::Config.run do |config|

  config.vm.box     = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :hostonly, "33.33.33.10"

  config.vm.share_folder PROJECT_NAME, MOUNT_POINT, "."

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.manifest_file  = "brew.pp"
    puppet.module_path    = "puppet/modules"
    puppet.facter = [
            ['project_name', PROJECT_NAME],
            ['django_dir', MOUNT_POINT + '/' + PROJECT_NAME],
            ['django_url', 'brew.pi'],
            ['db_username', 'brew'],
            ['db_password', 'brew'],
            ['db_name', 'brew'],
            ['db_root_password', 'brew'],
    ]
    puppet.options = [
      # '--verbose',
      # '--debug',
      # '--graph',
      # '--graphdir=/vagrant'
    ]
  end

end
