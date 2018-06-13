ex-001: Getting started
=======================

Initial
-------
Install **git** and **virtualenv**, if you don't already have them installed. Here are the links:

- `virtualenv <https://virtualenv.pypa.io/en/stable/>`_
- `git <https://git-scm.com/>`_


Clone this GitHub repo
----------------------
.. code-block::

	git clone git@github.com:addr2data/aws-certification-prep.git

.. code-block::

	Note: If you don't your SSH keys set up on GitHub, you can use HTTP.
	
	git clone https://github.com/addr2data/aws-certification-prep.git


Set up your virtual environment
--------------------------------
.. code-block::

 virtualenv aws-certification-prep
 cd aws-certification-prep
 source bin/activate


Install requirements
--------------------
.. code-block::

 pip install boto3 docopt awscli


Set up a user account for API access
------------------------------------
- Login to your AWS account.
- Under services select **IAM**.
- Select **users**
- Click **Add user**
- Under **Set user details**, enter user name **apiuser01**.
- Under **Select AWS access type**, select **Programmatic access**.
- Under **Set permissions for <user name>**, select **Attach existing policies directly**.
- Click on **Next: Permissions**.
- Search for **AmazonEC2FullAccess**, then select **AmazonEC2FullAccess**.
- Click on **Next: Review**.
- Click **Create user**.
- On the following screen, copy the values for **Access key ID** and **Secret access key**.


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