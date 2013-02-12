Brew.
=====

Brew. is a mashing process automation software for Beer brewing.

Brew is intended to run on a Raspberry Pi, connected to an Arduino.

* The Arduino board reads temperature sensors, triggers the stirprocess and controls the heat.
* The Raspberry Pi runs Brew. which contains a webservice allowing you to setup your Beer Mashing Scheme and watch logs for both live and historic details.


Brew is using these technologies: Python, Django, Javascript, jQuery, Twitter Bootstrap, Vagrant, Puppet, Gunicorn, Nginx, Supervisord, MySQL


###Installation for development

This project uses Vagrant / Puppet. Install [Vagrant](http://downloads.vagrantup.com/) and [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads) on your machine. 

Clone this repository including all submodules:

    $ git clone --recursive https://github.com/StryKaizer/Brew.git

Navigate to the Brew root directory and run the following command:

    $ vagrant up

In vagrant box run:

    $ /brew-ve/bin/python /brew-project/djangoproject/manage.py runserver 33.33.33.10:8000
    $ /brew-ve/bin/python /brew-project/djangoproject/manage.py celeryd

Development version will be available after provisioning on 33.33.33.10:8000

###Installation for vanilla Raspbian (Documentation is work in progress)

Install necessary packages

    $ sudo apt-get update
    $ sudo apt-get install git-core nano libmysqlclient-dev mysql-server python-setuptools python-dev python-mysqldb nginx
    $ sudo easy_install pip
    $ sudo pip install virtualenv supervisor==3.0b1

Create database

    $ mysql -u root -p
    $ CREATE DATABASE brewpi;
    $ GRANT ALL PRIVILEGES ON brewpi.* TO brewpi@localhost IDENTIFIED BY 'brewpi';

Clone project

    $ sudo git clone --recursive https://github.com/StryKaizer/Brew.git /brew-project

Setup virtual environment

    $ sudo virtualenv /brew-ve
    $ source /brew-ve/bin/activate
    $ sudo pip install -r /brew-project/djangoproject/requirements.txt
    $ deactivate

Hosting

    $ sudo nano /etc/nginx/sites-available/brewpi.conf
    server {
        listen 80;
        server_name brew.pi;
        access_log /var/log/nginx/brewpi.access.log;
        error_log /var/log/nginx/brewpi.error.log;

        # https://docs.djangoproject.com/en/dev/howto/static-files/#serving-static-$
        location /static/ { # STATIC_URL
            alias /brew-static/; # STATIC_ROOT
            expires 30d;
        }

        location / {
            proxy_pass http://127.0.0.1:8080;
        }
    }
    $ sudo ln -s /etc/nginx/sites-available/brewpi.conf /etc/nginx/sites-enabled/brewpi.conf
    $ sudo /etc/init.d/nginx start

Start supervisord as a service: https://github.com/gcollazo/Fabulous/issues/4



