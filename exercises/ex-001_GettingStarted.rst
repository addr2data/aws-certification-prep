ex-001: Getting started
=======================

Status
------
Version 0.9 (6/14/18) - needs additional review before moving to version 1.0.

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise
     - None
   * - Prerequisite for exercise
     - All

Introduction
------------
The primary purpose of this exercise is to get your local environment ready for basic connectivity to the AWS APIs and to create a user that will allow access to the EC2 API only.

You will use the **awscli** and **awscertprep_cli.py** (Python script included in the project) to test connectivity and briefly explore EC2.

Initial
-------
Install **git** and **virtualenv**, if you don't already have them installed. Here are the links:

- `virtualenv <https://virtualenv.pypa.io/en/stable/>`_
- `git <https://git-scm.com/>`_

Clone this GitHub repo
----------------------
.. code-block::

	git clone git@github.com:addr2data/aws-certification-prep.git

If you don't have your SSH key(s) added GitHub, you can use HTTP instead.

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
- Click on **Next: Permissions**.
- Under **Set permissions for apiuser01**, select **Attach existing policies directly**.
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

Insert the appropriate region for your location (see **AWS Regions** table below).

.. code-block::

    [default]
    region = YOUR_REGION
    output = json

AWS Regions
~~~~~~~~~~~
.. list-table::
   :widths: 25, 25, 25, 25
   :header-rows: 1

   * - Code
     - Name
     - Code
     - Name
   * - us-east-1
     - US East (N. Virginia)
     - us-east-2
     - US East (Ohio)
   * - us-west-1
     - UUS West (N. California)
     - us-west-2
     - US West (Oregon)
   * - ca-central-1
     - Canada (Central)
     - eu-central-1
     - EU (Frankfurt)
   * - eu-west-1
     - EU (Ireland)
     - eu-west-2
     - EU (London)
   * - eu-west-3
     - EU (Paris)
     - ap-northeast-1
     - Asia Pacific (Tokyo)
   * - ap-northeast-2
     - Asia Pacific (Seoul)
     - ap-northeast-3
     - Asia Pacific (Osaka-Local)
   * - ap-southeast-1
     - Asia Pacific (Singapore)
     - ap-southeast-2
     - Asia Pacific (Sydney)
   * - ap-south-1
     - Asia Pacific (Mumbai)
     - sa-east-1
     - South America (São Paulo)

*Note: These regions are valid as of 06/13/18. Please use the following link to see the most up to list of regions*
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html


Verify access
-------------
Use the following awscli command to verify that you are able to access the EC2 API

.. code-block::

	aws ec2 describe-regions

    {
        "Regions": [
            {
                "Endpoint": "ec2.ap-south-1.amazonaws.com",
                "RegionName": "ap-south-1"
            },
            {
                "Endpoint": "ec2.eu-west-3.amazonaws.com",
                "RegionName": "eu-west-3"
            },
            {
                "Endpoint": "ec2.eu-west-2.amazonaws.com",
                "RegionName": "eu-west-2"
            },
            {
                "Endpoint": "ec2.eu-west-1.amazonaws.com",
                "RegionName": "eu-west-1"
            },
            {
                "Endpoint": "ec2.ap-northeast-2.amazonaws.com",
                "RegionName": "ap-northeast-2"
            },
            {
                "Endpoint": "ec2.ap-northeast-1.amazonaws.com",
                "RegionName": "ap-northeast-1"
            },
            {
                "Endpoint": "ec2.sa-east-1.amazonaws.com",
                "RegionName": "sa-east-1"
            },
            {
                "Endpoint": "ec2.ca-central-1.amazonaws.com",
                "RegionName": "ca-central-1"
            },
            {
                "Endpoint": "ec2.ap-southeast-1.amazonaws.com",
                "RegionName": "ap-southeast-1"
            },
            {
                "Endpoint": "ec2.ap-southeast-2.amazonaws.com",
                "RegionName": "ap-southeast-2"
            },
            {
                "Endpoint": "ec2.eu-central-1.amazonaws.com",
                "RegionName": "eu-central-1"
            },
            {
                "Endpoint": "ec2.us-east-1.amazonaws.com",
                "RegionName": "us-east-1"
            },
            {
                "Endpoint": "ec2.us-east-2.amazonaws.com",
                "RegionName": "us-east-2"
            },
            {
                "Endpoint": "ec2.us-west-1.amazonaws.com",
                "RegionName": "us-west-1"
            },
            {
                "Endpoint": "ec2.us-west-2.amazonaws.com",
                "RegionName": "us-west-2"
            }
        ]
    }

Using the **'--dry-run'** option lets you verify access without actually runninng the command. Don't be fooled by the statement **'An error occurred'**.

.. code-block::

    aws ec2 describe-regions --dry-run

    An error occurred (DryRunOperation) when calling the DescribeRegions operation: Request would have succeeded, but DryRun flag is set.

Verify restriction
------------------
Use the following awscli command to verify that you NOT are able to access the EC2 API

.. code-block::

    aws iam get-account-summary

    An error occurred (AccessDenied) when calling the GetAccountSummary operation: User: arn:aws:iam::926075045128:user/apiuser01 is not authorized to perform: iam:GetAccountSummary on resource: *





Availability Zones
------------------
1. Take a look at the **Availability Zones** in your region.

.. code-block::

	aws ec2 describe-availability-zones

2. Take a look at the **Availability Zones** in another region.

.. code-block::

	aws ec2 describe-availability-zones --region us-east-2

3. Now let's look at all the **Regions** and **Availability Zones** together.

.. code-block::

    python awscertprep_cli.py show_regions --avail_zones


Summary
-------
- You have set up your environment to be used with this repo.
- You have created a user **apiuser01** and gave it API access.
- You have assigned **apiuser01** full access to the EC2 API.
- You used **awscli** to verify that **apiuser01** does have access to the EC2 API.
- You used **awscli** to verify that **apiuser01** does NOT have access to the IAM API.
- You used **awscli** to explore AWS **regions** and **Availability Zones**.
 

