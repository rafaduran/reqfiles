# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define 'centos' do |centos|
    centos.vm.box = 'centos63'
    centos.vm.box_url = 'https://dl.dropbox.com/u/7225008/Vagrant/CentOS-6.3-x86_64-minimal.box'
  end

  config.vm.define 'ubuntu' do |ubuntu|
    ubuntu.vm.box = 'precise64'
    ubuntu.vm.box_url = 'http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box'
  end

  config.vm.define 'debian' do |debian|
    debian.vm.box = 'debian-squeeze'
    debian.vm.box_url = 'http://f.willianfernandes.com.br/vagrant-boxes/DebianSqueeze64.box'
  end
end
