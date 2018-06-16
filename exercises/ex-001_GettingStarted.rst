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

   * - Depends on exercise(s)
     - None
   * - Prerequisite for exercise(s)
     - All

Objectives
----------

- Get your local environment ready.
- Create an AWS IAM user that will allow programmatic access to the EC2 API.
- Use **awscli** to briefly explore EC2.
- Familiarize yourself with a couple **awscli** commandline options.

Expected Costs
--------------
The activities in this exercise are NOT expected to result in charges to your AWS account.

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
Use the following awscli command to verify that you are able to access the EC2 API by attempting to show the EC2 regions.

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

Using the **'--dry-run'** option lets you verify access without actually runninng the command. Don't be fooled by the message **'An error occurred'**.

.. code-block::

    aws ec2 describe-regions --dry-run

    An error occurred (DryRunOperation) when calling the DescribeRegions operation: Request would have succeeded, but DryRun flag is set.

Verify restriction
------------------
Use the following awscli command to verify that you NOT are able to access the IAM API

.. code-block::

    aws iam get-account-summary

    An error occurred (AccessDenied) when calling the GetAccountSummary operation: User: arn:aws:iam::926075045128:user/apiuser01 is not authorized to perform: iam:GetAccountSummary on resource: *

Formatting output
-----------------
Use the following awscli command with **'--output text'** and **'--output table'** options to see different output formats.

.. code-block::

    aws ec2 describe-regions --output text

    REGIONS ec2.ap-south-1.amazonaws.com    ap-south-1
    REGIONS ec2.eu-west-3.amazonaws.com eu-west-3
    REGIONS ec2.eu-west-2.amazonaws.com eu-west-2
    REGIONS ec2.eu-west-1.amazonaws.com eu-west-1
    REGIONS ec2.ap-northeast-2.amazonaws.com    ap-northeast-2
    REGIONS ec2.ap-northeast-1.amazonaws.com    ap-northeast-1
    REGIONS ec2.sa-east-1.amazonaws.com sa-east-1
    REGIONS ec2.ca-central-1.amazonaws.com  ca-central-1
    REGIONS ec2.ap-southeast-1.amazonaws.com    ap-southeast-1
    REGIONS ec2.ap-southeast-2.amazonaws.com    ap-southeast-2
    REGIONS ec2.eu-central-1.amazonaws.com  eu-central-1
    REGIONS ec2.us-east-1.amazonaws.com us-east-1
    REGIONS ec2.us-east-2.amazonaws.com us-east-2
    REGIONS ec2.us-west-1.amazonaws.com us-west-1
    REGIONS ec2.us-west-2.amazonaws.com us-west-2

.. code-block::

    aws ec2 describe-regions --output table

    ----------------------------------------------------------
    |                     DescribeRegions                    |
    +--------------------------------------------------------+
    ||                        Regions                       ||
    |+-----------------------------------+------------------+|
    ||             Endpoint              |   RegionName     ||
    |+-----------------------------------+------------------+|
    ||  ec2.ap-south-1.amazonaws.com     |  ap-south-1      ||
    ||  ec2.eu-west-3.amazonaws.com      |  eu-west-3       ||
    ||  ec2.eu-west-2.amazonaws.com      |  eu-west-2       ||
    ||  ec2.eu-west-1.amazonaws.com      |  eu-west-1       ||
    ||  ec2.ap-northeast-2.amazonaws.com |  ap-northeast-2  ||
    ||  ec2.ap-northeast-1.amazonaws.com |  ap-northeast-1  ||
    ||  ec2.sa-east-1.amazonaws.com      |  sa-east-1       ||
    ||  ec2.ca-central-1.amazonaws.com   |  ca-central-1    ||
    ||  ec2.ap-southeast-1.amazonaws.com |  ap-southeast-1  ||
    ||  ec2.ap-southeast-2.amazonaws.com |  ap-southeast-2  ||
    ||  ec2.eu-central-1.amazonaws.com   |  eu-central-1    ||
    ||  ec2.us-east-1.amazonaws.com      |  us-east-1       ||
    ||  ec2.us-east-2.amazonaws.com      |  us-east-2       ||
    ||  ec2.us-west-1.amazonaws.com      |  us-west-1       ||
    ||  ec2.us-west-2.amazonaws.com      |  us-west-2       ||
    |+-----------------------------------+------------------+|

Filtering results
-----------------
Use the following awscli command with **'--query'** option to filter results.

.. code-block::

    aws ec2 describe-regions --query Regions[*].RegionName

    [
        "ap-south-1",
        "eu-west-3",
        "eu-west-2",
        "eu-west-1",
        "ap-northeast-2",
        "ap-northeast-1",
        "sa-east-1",
        "ca-central-1",
        "ap-southeast-1",
        "ap-southeast-2",
        "eu-central-1",
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2"
    ]

.. code-block::

    aws ec2 describe-regions --query Regions[*].RegionName --output text

    ap-south-1  eu-west-3   eu-west-2   eu-west-1   ap-northeast-2  ap-northeast-1  sa-east-1   ca-central-1    ap-southeast-1  ap-southeast-2  eu-central-1    us-east-1   us-east-2   us-west-1   us-west-2


Explore your Region
-------------------
Use the following awscli command to examine the **Availability Zones** in your region.

.. code-block::

    aws ec2 describe-availability-zones

    {
        "AvailabilityZones": [
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-1",
                "ZoneName": "us-east-1a"
            },
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-1",
                "ZoneName": "us-east-1b"
            },
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-1",
                "ZoneName": "us-east-1c"
            },
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-1",
                "ZoneName": "us-east-1d"
            },
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-1",
                "ZoneName": "us-east-1e"
            },
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-1",
                "ZoneName": "us-east-1f"
            }
        ]
    }

Explore another Region
----------------------
Use the following awscli command to examine the **Availability Zones** in another region.

.. code-block::
    
    aws ec2 describe-availability-zones --region us-east-2

    {
        "AvailabilityZones": [
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-2",
                "ZoneName": "us-east-2a"
            },
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-2",
                "ZoneName": "us-east-2b"
            },
            {
                "State": "available",
                "Messages": [],
                "RegionName": "us-east-2",
                "ZoneName": "us-east-2c"
            }
        ]
    }

Custom scripts
--------------
Run the following script to see all the **Regions** and **Availability Zones** together.

.. code-block::

    python awscertprep_cli.py show_regions --avail_zones

    Regions                  Availability Zones
    -------                  ------------------
    ap-northeast-1           (ap-northeast-1a, ap-northeast-1c, ap-northeast-1d)
    ap-northeast-2           (ap-northeast-2a, ap-northeast-2c)
    ap-south-1               (ap-south-1a, ap-south-1b)
    ap-southeast-1           (ap-southeast-1a, ap-southeast-1b, ap-southeast-1c)
    ap-southeast-2           (ap-southeast-2a, ap-southeast-2b, ap-southeast-2c)
    ca-central-1             (ca-central-1a, ca-central-1b)
    eu-central-1             (eu-central-1a, eu-central-1b, eu-central-1c)
    eu-west-1                (eu-west-1a, eu-west-1b, eu-west-1c)
    eu-west-2                (eu-west-2a, eu-west-2b, eu-west-2c)
    eu-west-3                (eu-west-3a, eu-west-3b, eu-west-3c)
    sa-east-1                (sa-east-1a, sa-east-1c)
    us-east-1                (us-east-1a, us-east-1b, us-east-1c, us-east-1d, us-east-1e, us-east-1f)
    us-east-2                (us-east-2a, us-east-2b, us-east-2c)
    us-west-1                (us-west-1a, us-west-1b)
    us-west-2                (us-west-2a, us-west-2b, us-west-2c)


Summary
-------
- You have set up your environment to be used with this repo.
- You have created a user **apiuser01** and gave it API access.
- You have assigned **apiuser01** full access to the EC2 API.
- You used **awscli** to verify that **apiuser01** does have access to the EC2 API.
- You used **awscli** to verify that **apiuser01** does NOT have access to the IAM API.
- You used **awscli** to explore AWS **regions** and **Availability Zones**.
 

