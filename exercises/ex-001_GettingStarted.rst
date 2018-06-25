ex-001: Getting started
=======================

Status
------
Version 1.4 (6/24/18)

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
- Create an AWS IAM user that will have programmatic access to the EC2 API.
- Use **awscli** to briefly explore EC2.
- Familiarize yourself with some **awscli** command-line options.
- Create a AWS Key Pair for use in subsequent exercises.
- Create a budget, in AWS Billing, to alert you when your spend reaches a specific threshold.  

Expected Costs
--------------
The activities in this exercise are NOT expected to result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
   * - Key Pairs
     - None
     - 
   * - Budgets
     - 
        + $0.00 for your first two budgets.
        + $0.02 per budget per day, afterwards.
     - If you examine your 'Bill Details' (under Billing) and expand the 'Budgets' section, you will see "$0.00 for 62 Budget-days per month (free tier)". That represents your two free budgets per month.

Limits
------
The following table shows the default limits for the components utilized in this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - Key Pairs
     - 5000 per region

**Note: You can view all your EC2 limits and request increases by clicking on 'Limits' in the navigation pane of the EC2 console.**

Initial
-------
Install **git** and **virtualenv**, if you don't already have them installed.

- git is used to acquire the latest version of this repository
- virtualenv is used to to manage Python packages for different projects. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects. 
- jq is used to parse json data

On Ubuntu, you would simply run

.. code-block::
    
    sudo apt-get install git virtualenv jq

Here are the links:

- `virtualenv <https://virtualenv.pypa.io/en/stable/>`_
- `git <https://git-scm.com/>`_
- `jq <https://stedolan.github.io/jq/download/>`_

Clone this GitHub repo
----------------------
.. code-block::

	git clone git@github.com:addr2data/aws-certification-prep.git

If you don't have your SSH key(s) added GitHub, you can use HTTP instead.

.. code-block::
	
	git clone https://github.com/addr2data/aws-certification-prep.git

Set up your virtual environment
--------------------------------
Use these commands to set up your virtual environment. This allows the packages installed in the next section to be isolated from the rest of your environment.

Afterwards, be sure that your command prompt begins with (aws-certification-prep), which indicates that you are in the correct virtual environment

.. code-block::

 virtualenv aws-certification-prep
 cd aws-certification-prep
 source bin/activate


Install requirements
--------------------
Use this command to install the required packages. We will use **'awscli'** directly throughout the exercises. **'boto'3** and **'docopt'** are required by the **'awscertprep_cli.py'** Python script provided in the project.

.. code-block::

 	pip install boto3 docopt awscli

Set up a user account for API access
------------------------------------
- Login to your AWS account.
- Under services select **IAM**.
- Select **users**
- Click **Add user**
- Under **Set user details**, enter user name **apiuser01**.
- Under **Select AWS access type**, select **Programmatic access** (this account does not require AWS Management Console access.)
- Click on **Next: Permissions**.
- Under **Set permissions for apiuser01**, select **Attach existing policies directly**.
- Search for **AmazonEC2FullAccess**, then select **AmazonEC2FullAccess** (we will add access to other services later).
- Click on **Next: Review**.
- Click **Create user**.
- On the following screen, copy the values for **Access key ID** and **Secret access key**. You'll have to click the Show link in order to display teh actual Secret Key value. Once copied and saved, click Close

Create a credentials file
-------------------------
Back on our workstation, we'll set up the tools to automatically authenticate using the account we just set up.

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

Insert the appropriate region for your location (see the URL where you logged into the AWS Console above. For example us-east-2).

.. code-block::

    [default]
    region = YOUR_REGION
    output = json


For more information on AWS Regions:
`AWS Regions and Availability Zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html>`_


Verify access
-------------
Use the following awscli command to verify that you are able to access the EC2 API by attempting to show the EC2 regions.

.. code-block::

	aws ec2 describe-regions

Output:

.. code-block::

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

            <--- SNIP --->
  
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

Using the **'--dry-run'** option lets you verify access without actually runninng the command. Don't be fooled by the **'An error occurred'** part of the message, the operation was successful.

.. code-block::

    aws ec2 describe-regions --dry-run

Output:

.. code-block::

    An error occurred (DryRunOperation) when calling the DescribeRegions operation: Request would have succeeded, but DryRun flag is set.

Verify restriction
------------------
Use the following awscli command to verify that you NOT are able to access the IAM API

.. code-block::

    aws iam get-account-summary

Output:

.. code-block::

    An error occurred (AccessDenied) when calling the GetAccountSummary operation: User: arn:aws:iam::926075045128:user/apiuser01 is not authorized to perform: iam:GetAccountSummary on resource: *

Formatting output
-----------------
Use the following awscli command with the **'--output text'** option.

.. code-block::

    aws ec2 describe-regions --output text

Output:

.. code-block::

    REGIONS ec2.ap-south-1.amazonaws.com    ap-south-1
    REGIONS ec2.eu-west-3.amazonaws.com eu-west-3
    REGIONS ec2.eu-west-2.amazonaws.com eu-west-2

    <--- SNIP --->

    REGIONS ec2.us-west-1.amazonaws.com us-west-1
    REGIONS ec2.us-west-2.amazonaws.com us-west-2

Use the following awscli command with the **'--output table'** option.

.. code-block::

    aws ec2 describe-regions --output table

Output:

.. code-block::

    ----------------------------------------------------------
    |                     DescribeRegions                    |
    +--------------------------------------------------------+
    ||                        Regions                       ||
    |+-----------------------------------+------------------+|
    ||             Endpoint              |   RegionName     ||
    |+-----------------------------------+------------------+|
    ||  ec2.ap-south-1.amazonaws.com     |  ap-south-1      ||
    ||  ec2.eu-west-3.amazonaws.com      |  eu-west-3       ||

    <--- SNIP --->

    ||  ec2.us-west-1.amazonaws.com      |  us-west-1       ||
    ||  ec2.us-west-2.amazonaws.com      |  us-west-2       ||
    |+-----------------------------------+------------------+|

The --output option is valuable in overriding the default output (json). If you wish to set the output to always be **'text'** or **'table'**, then modify the output parameter we set as default in the ~/.aws/config file

Filtering results
-----------------
Use the following awscli command with **'--query'** option to filter results. In this case, only the **'RegionName'** is returned.

.. code-block::

    aws ec2 describe-regions --query Regions[*].RegionName

Output:

.. code-block::

    [
        "ap-south-1",
        "eu-west-3",

        <--- SNIP --->

        "us-west-1",
        "us-west-2"
    ]

Another use of the query subcommand is to return values for only records that match your criteria. In this case, the **'Endpoint'** is returned for only Region **'us-east-2'**.

.. code-block::

    aws ec2 describe-regions --query 'Regions[?RegionName==`us-east-2`].Endpoint' --output text

Output:

.. code-block::

    ec2.us-east-2.amazonaws.com

Explore your Region
-------------------
Use the following awscli command to examine the **Availability Zones** in your region.

.. code-block::

    aws ec2 describe-availability-zones

Output:

.. code-block::

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

Output:

.. code-block::

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

Python
~~~~~~

.. code-block::

    python awscertprep_cli.py show_regions --avail_zones

Output:

.. code-block::

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


Bash
~~~~
Create a bash script using the following commands and see the results for yourself:

.. code-block::

    #!/bin/bash

    REGIONS=$(aws ec2 describe-regions | jq -r '.Regions[] | .RegionName')

    for reg in $REGIONS
        do
        AZS=$(aws ec2 describe-availability-zones --region $reg | jq -r '.AvailabilityZones | map(.ZoneName) | join (", ")')
        echo REGION:$reg%AZs:$AZS | column -s % -t
        done

Create a Key Pair
-----------------
Use the following awscli command to create a new **Key Pair** and save the resulting **'.pem'** file.

**Note: I have only verified that directly redirecting the 'KeyMaterial' to a file produces a valid '.pem' on macOS. Other OSs may have subtle differences.**

.. code-block::
    
    aws ec2 create-key-pair --key-name acpkey1 --query 'KeyMaterial' --output text > acpkey1.pem

Modify permissions
------------------
Use the following command to modify the permissions on the '.pem'.

.. code-block::
    
    chmod 400 acpkey1.pem

Create a budget
---------------
As you move through these exercises, it is expected that you will incur small charges to you AWS account. To ensure these expenses don't get away from you, we are going to set up a budget.  

- Login to your AWS account.
- Under services, type **Billing** into the search box and select it.
- In the navigation pane, select **'Budgets'**.
- Click **Create budget**.

Section 1
~~~~~~~~~

- Under **Budget type**, select **Cost**.
- Under **Name**, enter a name for your Budget.
- Under **Period**, select **Monthly** (default).
- Under **Start date**, select a start date (defaults to start of billing cycle)
- Under **Budgeted amount**, enter an amount that you don't want to exceed in a month (I set $20.00).
- Skip section 2.

Section 3
~~~~~~~~~
- Under **Notify me when**, enter values that make sense for you (I set it to notify me when 'actual' costs are 'greater than' 50 '%' of 'budgeted amount')
- Under **Email contacts**, enter you email address.
- Click **Create**

Summary
-------
- You have set up your local environment.
- You have created a IAM user **apiuser01** and gave it programmatic access only.
- You have assigned **apiuser01** full access to the EC2 API.
- You used **awscli** to verify that **apiuser01** has access to the EC2 API.
- You used **awscli** to verify that **apiuser01** does NOT have access to the IAM API.
- You used **awscli** to explore AWS **regions** and **Availability Zones**.
- You experimented with a couple of **awscli** commandline options.
- You created a **Budget**.

Next steps
----------
Explore Basic VPC Configuration in 
`ex-002 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-002_BasicVpcConfig.rst>`_

