ex-001: Getting started
=======================

Creating a virtual environment
------------------------------

.. code-block::

 [sudo] pip3 install virtualenv


If you are not familiar with virtualenv, here is a link to the project page.

`virtualenv project page <https://virtualenv.pypa.io/en/stable/>`_



- Install boto3

Credentials
~~~~~~~~~~~
mkdir ~/.aws
vi ~/.aws/credentials

	[default]
	aws_access_key_id = YOUR_ACCESS_KEY
	aws_secret_access_key = YOUR_SECRET_KEY

Configuration
~~~~~~~~~~~~~
vi ~/.aws/config

	[default]
	region=us-east-1