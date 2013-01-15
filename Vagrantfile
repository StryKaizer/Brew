# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "squeeze32"
  config.vm.box_url = "http://mathie-vagrant-boxes.s3.amazonaws.com/debian_squeeze_32.box"

  # Use :gui for showing a display for easy debugging of vagrant
  # config.vm.boot_mode = :gui

  # Some VirtualBoxes seem to need this
  config.vm.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]

  config.vm.define :brew do |brew_config|
    brew_config.vm.host_name = "www.brew.pi"

    brew_config.vm.network :hostonly, "33.33.33.10"

    # Pass custom arguments to VBoxManage before booting VM
    #brew_config.vm.customize [
    #  'modifyvm', :id, '--chipset', 'ich9', # solves kernel panic issue on some host machines
    #]

    # Pass installation procedure over to Puppet (see `puppet/manifests/secretsanta.pp`)
    brew_config.vm.provision :puppet do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.module_path = "puppet/modules"
      puppet.manifest_file = "brew.pp"
      puppet.options = [
        '--verbose',
        '--debug',
      ]
    end
  end
end
