ex-001: Getting started
=======================

Initial
-------
Install **git** and **virtualenv**, if you don't already have them installed. Here are the links:

`virtualenv <https://virtualenv.pypa.io/en/stable/>`_

`git <https://git-scm.com/>`_


Clone this GitHub repo
----------------------
.. code-block::

	git clone git@github.com:addr2data/aws-certification-prep.git

*Note: If you don't your SSH keys set up on GitHub, you can use HTTP.*

.. code-block::
	
	git clone https://github.com/addr2data/aws-certification-prep.git


Set up your virtual environment
--------------------------------
.. code-block::

 virtualenv aws-certification-prep
 cd aws-certification-prep
 source bin/activate


Install the requirements
--------------------
.. code-block::

 pip install boto3 docopt awscli


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