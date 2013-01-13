Brew.
=====

Brew. is a mashing process automation software for Beer brewing.

Brew is intended to run on a Raspberry Pi, connected to an Arduino.

* The Arduino board reads temperature sensors, triggers the stirprocess and controls the heat.
* The Raspberry Pi runs Brew. which contains a webservice which allows you to setup your Beer Mashing Scheme and watch logs for both live and historic details.


Brew is written in Python, Django, Javascript, jQuery, Bootstrap.

###Installation

Clone project
$ git clone https://github.com/StryKaizer/Brew.git

Install python setup-tools
$ sudo apt-get install python-setuptools

Install pip
$ sudo easy_install pip

Install virtualenv
$ sudo pip install virtualenv

Create virtual environment in your project
$ virtualenv ve --no-site-packages

Activate virtual environment
$ source ve/lib/activate

Install python requirements
$ sudo pip install -r requirements.txt

TOD