# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "chedi/f22-cloud"
    config.vm.synced_folder ".", "/home/vagrant/roots", type: "rsync"
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.vm.hostname = "roots-devel"

    config.vm.provider "libvirt" do |libvirt, override|
        libvirt.memory = 1024
    end

    config.vm.provision "shell", inline: <<-SHELL
    # Build essentials
    dnf install -y python-pip git gcc python-devel

    # Developer essentials
    dnf install -y vim

    # Requirements for Pillow and Wand
    dnf install -y libjpeg-turbo-devel zlib-devel ImageMagick-devel

    # Requirement for pypandoc
    dnf install -y pandoc

    # pip wishes to be upgraded
    pip install --upgrade pip

    pip install -r /home/vagrant/roots/requirements.txt
    pip install git+git://github.com/django-wiki/django-wiki
    pip install git+git://github.com/tbabej/django-avatar

    # Reinstall of six seems to be necessary for some weird reason
    pip uninstall -y six
    pip install six

    # Create defaults from the .in template files if they do not exist
    cd /home/vagrant/roots

    if [[ ! -f roots/local_settings.py ]]
    then
      cp roots/local_settings.py.in roots/local_settings.py
    fi

    if [[ ! -f roots.db ]]
    then
      python manage.py migrate
      python manage.py shell_plus <<< "execfile('scripts/bootstrap.py')"
    else
      python manage.py migrate
    fi

    # Ensure everything in the repository is owned by vagrant
    chown -R vagrant:vagrant .
    SHELL
end
