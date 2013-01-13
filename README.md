Brew.
=====

Brew. is a mashing process automation software for Beer brewing.

Brew is intended to run on a Raspberry Pi, connected to an Arduino.

* The Arduino board reads temperature sensors, triggers the stirprocess and controls the heat.
* The Raspberry Pi runs Brew. which contains a webservice allowing you to setup your Beer Mashing Scheme and watch logs for both live and historic details.


Brew is written in Python, Django, Javascript, jQuery, Bootstrap.

###Installation

Install required libraries

    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get install git apache2 mysql-server python-mysqldb libapache2-mod-wsgi python-setuptools

Clone project

    $ git clone https://github.com/StryKaizer/Brew.git

Install pip and virtualenv

    $ sudo easy_install pip
    $ sudo pip install virtualenv

Create and activate virtual environment in your Brew. folder

    $ virtualenv ve --no-site-packages
    $ source ve/lib/activate

Install python requirements

    $ sudo ./ve/bin/pip install -r requirements.txt

TODO, complete installation procedure