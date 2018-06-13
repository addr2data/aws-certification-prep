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

If you don't your SSH keys set up on GitHub, you can use HTTP instead.

.. code-block::
	
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
- Search for **AmazonEC2FullAccess**, then select **AmazonEC2FullAccess** (we will add access to other services later).
- Click on **Next: Review**.
- Click **Create user**.
- On the following screen, copy the values for **Access key ID** and **Secret access key**.


Create a credentials file
-------------------------
.. code-block::

	mkdir ~/.aws
	vi ~/.aws/credentials

Insert the **Access key ID** and **Secret access key** that you copied in the previous step. Save the file.

.. code-block::

	[default]
	aws_access_key_id = YOUR_ACCESS_KEY
	aws_secret_access_key = YOUR_SECRET_KEY


Create a configuration file
---------------------------
.. code-block::

	vi ~/.aws/config

Insert the appropriate region for your location (see region table below).

.. code-block::

	[default]
	region = YOUR_REGION


AWS Regions
~~~~~~~~~~~
.. list-table::
   :widths: 25, 25
   :header-rows: 1

   * - Code
     - Name
   * - us-east-1
     - US East (N. Virginia)
   * - us-east-2
     - US East (Ohio)
   * - us-west-1
     - UUS West (N. California)
   * - us-west-2
     - US West (Oregon)
   * - ca-central-1
     - Canada (Central)
   * - eu-central-1
     - EU (Frankfurt)
   * - eu-west-1
     - EU (Ireland)
   * - eu-west-2
     - EU (London)
   * - eu-west-3
     - EU (Paris)
   * - ap-northeast-1
     - Asia Pacific (Tokyo)
   * - ap-northeast-2
     - Asia Pacific (Seoul)
   * - ap-northeast-3
     - Asia Pacific (Osaka-Local)
   * - ap-southeast-1
     - Asia Pacific (Singapore)
   * - ap-southeast-2
     - Asia Pacific (Sydney)
   * - ap-south-1
     - Asia Pacific (Mumbai)
   * - sa-east-1
     - South America (São Paulo)

*Note: These regions are valid as of 06/13/18. Please use the following link to see the most up to list of regions*
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html


Testing access
--------------
1. Verify that you are able to access the EC2 API.

.. code-block::

	aws ec2 describe-regions

2. Verify that you are **NOT** able to access the IAM API.

.. code-block::

	aws iam get-account-summary


Availability Zones
------------------
1. Take a look at the Availability Zones in your region.

.. code-block::

	aws ec2 describe-availability-zones


https://github.com/addr2data/aws-certification-prep/blob/master/images/ex-001-image-01.png



