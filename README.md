Brew.
=====

Brew. is a mashing process automation software for Beer brewing.

Brew is intended to run on a Raspberry Pi, connected to an Arduino.

* The Arduino board reads temperature sensors, triggers the stirprocess and controls the heat.
* The Raspberry Pi runs Brew. which contains a webservice allowing you to setup your Beer Mashing Scheme and watch logs for both live and historic details.


Brew is written in Python, Django, Javascript, jQuery, Bootstrap.

###Installation for vanilla Raspbian (or Debian)

Install required libraries

    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get install git apache2 mysql-server python-mysqldb libapache2-mod-wsgi python-setuptools libmysqlclient-dev python-dev php5 phpmyadmin

Clone project

    $ git clone https://github.com/StryKaizer/Brew.git

Install pip and virtualenv

    $ sudo easy_install pip
    $ sudo pip install virtualenv MySQL-python

Create and activate virtual environment in your Brew. folder

    $ cd Brew/
    $ virtualenv ve --no-site-packages
    $ source ve/bin/activate

Install python requirements

    $ sudo ./ve/bin/pip install -r requirements.txt

Create vhost

    <VirtualHost *:80>
        ServerAdmin jimmyhdx@gmail.com
        # ServerName  brew.pi
        DocumentRoot /home/pi/Brew/django/brew
        
        # mod_wsgi settings
        WSGIDaemonProcess brew python-path=/home/pi/Brew/django:/home/pi/Brew/ve/lib/python2.7/site-packages
        WSGIProcessGroup brew
        WSGIScriptAlias / /home/pi/Brew/django/brew/wsgi.py
        
        # Static file alias so static files can be referenced by /static/
        Alias /static/ /home/pi/Brew/django/brew/static/
        
        # Static files permissions
        # Used for serving static files.
        <Directory /home/pi/Brew/django/brew/static>
            Order deny,allow
            Allow from all
        </Directory>
        
        # Project wsgi permissions
        # Used for serving django pages.
        <Directory /home/pi/Brew/django/brew>
            <Files wsgi.py>
                Order deny,allow
                Allow from all
            </Files>
        </Directory>
    </VirtualHost>



Symlink Admin static folder
    sudo ln -s /home/pi/Brew/ve/lib/python2.7/site-packages/django/contrib/admin/static/admin /home/pi/Brew/django/brew/static/admin
    sudo ln -s /home/pi/Brew/ve/lib/python2.7/site-packages/dajaxice/templates/dajaxice /home/pi/Brew/django/brew/static/dajaxice