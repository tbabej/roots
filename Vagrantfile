# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "rarguello/fedora-22"
    config.vm.synced_folder ".", "/home/vagrant/roots", type: "rsync"
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.vm.hostname = "roots-devel"

    config.vm.provider "libvirt" do |libvirt, override|
        libvirt.memory = 1024
    end

    config.vm.provision "shell", inline: <<-SHELL
    # Build essentials
    sudo dnf install -y python-pip git gcc python-devel

    # Developer essentials
    sudo dnf install -y vim

    # Requirements for Pillow and Wand
    sudo dnf install -y libjpeg-turbo-devel zlib-devel ImageMagick-devel

    # Requirement for pypandoc
    sudo dnf install -y pandoc

    pip install -r /home/vagrant/roots/requirements.txt
    pip install git+git://github.com/django-wiki/django-wiki
    pip install git+git://github.com/tbabej/django-avatar
    SHELL
end
