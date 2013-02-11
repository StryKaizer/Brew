Brew.
=====

Brew. is a mashing process automation software for Beer brewing.

Brew is intended to run on a Raspberry Pi, connected to an Arduino.

* The Arduino board reads temperature sensors, triggers the stirprocess and controls the heat.
* The Raspberry Pi runs Brew. which contains a webservice allowing you to setup your Beer Mashing Scheme and watch logs for both live and historic details.


Brew is using these technologies: Python, Django, Javascript, jQuery, Twitter Bootstrap, Vagrant, Puppet, Gunicorn, Nginx, Supervisord, MySQL


###Installation for development

Just use vagrant and virtualbox, fire vagrant up, and go!

###Installation for vanilla Raspbian (or Debian)

Install necessary packages

  sudo apt-get update
  sudo apt-get install git-core nano libmysqlclient-dev mysql-server python-setuptools python-dev
  sudo easy_install pip
  sudo pip install virtualenv

Create database
  mysql -u root -p
  CREATE DATABASE brewpi;
  GRANT ALL PRIVILEGES ON brewpi.* TO brewpi@localhost IDENTIFIED BY 'brewpi';

Setup virtual environment