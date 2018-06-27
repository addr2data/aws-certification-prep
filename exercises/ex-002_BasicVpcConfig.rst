ex-002: Basic VPC configuration
===============================

Status
------
Version 1.2 (6/24/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001
   * - Prerequisite for exercise(s)
     - ex-003

Objectives
----------

    - Become familiar with basic VPC configuration (we'll be leaving this configuration in place to support ex-003)

Expected Costs
--------------
The activities in this exercise are NOT expected to result in any charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
   * - 
        + VPC (including Subnets, Route Tables and IntenetGateways)
     - 
        + None
     - 
        + AWS does NOT charge for the basic VPC building blocks used in this exercise.
        + AWS does charge for other VPC components, you will use these components in future exercises.   
    
Limits
------
The following table shows the default limits for the components utilized in this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - VPC
     - 5 per region
   * - Route Tables
     - 200 per VPC
   * - Entries per Route Table
     - 50
   * - Subnets
     - 200 per VPC

Environment variables
---------------------
During these exercises, we will be using the output of some commands to creatie environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Create a VPC
------------
Use the following awscli command to create a new VPC with a /16 prefix length (~64K addresses).

It will be created in your **Default Region** (we specified this in ex-001). If you wish to create a VPC in another Region, you would use the **'--region <value>'** option with the awscli.

.. code-block::
    
    aws ec2 create-vpc --cidr-block 10.0.0.0/16

Output:

.. code-block::

    {
        "Vpc": {
            "CidrBlock": "10.0.0.0/16",
            "DhcpOptionsId": "dopt-xxxxxxxx",
            "State": "pending",
            "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
            "InstanceTenancy": "default",
            "Ipv6CidrBlockAssociationSet": [],
            "CidrBlockAssociationSet": [
                {
                    "AssociationId": "vpc-cidr-assoc-xxxxxxxxxxxxxxxxx",
                    "CidrBlock": "10.0.0.0/16",
                    "CidrBlockState": {
                        "State": "associated"
                    }
                }
            ],
            "IsDefault": false,
            "Tags": []
        }
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
To simplify our commands and reduce the likelihood of typos, we'll use an environment variable for the VPC ID. In the output above, find the **'VpcId'** key.

.. code-block::

    export EX002_VPC=<VpcId>  <-- no quotes

Verify the VPC
--------------
Use the following awscli command to ensure that the VPC State is **'available'**.

.. code-block::
    
    aws ec2 describe-vpcs --vpc-ids $EX002_VPC

Output:

.. code-block::

    {
        "Vpcs": [
            {
                "CidrBlock": "10.0.0.0/16",
                "DhcpOptionsId": "dopt-xxxxxxxx",
                "State": "available",
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx"",
                "InstanceTenancy": "default",
                "CidrBlockAssociationSet": [
                    {
                        "AssociationId": "vpc-cidr-assoc-xxxxxxxxxxxxxxxxx",
                        "CidrBlock": "10.0.0.0/16",
                        "CidrBlockState": {
                            "State": "associated"
                        }
                    }
                ],
                "IsDefault": false
            }
        ]
    }


Examine the main Route Table
-------------------------------
Use the following awscli command to view Main Route Table.

In this command, we'll apply a filter in the Key|Value format to ensure that only the routes associated with our new VPC are displayed. Note that the filter Name is vpc-id

.. code-block::

    aws ec2 describe-route-tables --filter Name=vpc-id,Values=$EX002_VPC

Output:

.. code-block::

    {
        "RouteTables": [
            {
                "Associations": [
                    {
                        "Main": true,
                        "RouteTableAssociationId": "rtbassoc-xxxxxxxxxxxxxxxxx",
                        "RouteTableId": "rtb-xxxxxxxxxxxxxxxxx"
                    }
                ],
                "PropagatingVgws": [],
                "RouteTableId": "rtb-xxxxxxxxxxxxxxxxx",
                "Routes": [
                    {
                        "DestinationCidrBlock": "10.0.0.0/16",
                        "GatewayId": "local",
                        "Origin": "CreateRouteTable",
                        "State": "active"
                    }
                ],
                "Tags": [],
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx"
            }
        ]
    }


The above Route Table is created automatically when a VPC is created. You can see a single entry under **Routes**. This entry will allow for the routing of local traffic for all Subnets associated with the main Route Table. If you don't explicitly associate a subnet with another Route Table, it is implicitly associated with the main Route Table.

We won't be modifying the main Route Table. We will use it to provide routing for the **'private'** Subnet we will create later. Since newly created Subnets are implicitly associated with the main Route Table, it would seem to be a good practice to provide reachability to/from the Internet via a separate Route Table. 

Environment variable
~~~~~~~~~~~~~~~~~~~~
We'll create another environment variable for our Route Table ID, In the output above, find the **'RouteTableId'** key.

.. code-block::

    export EX002_RTB_PRIV=<RouteTableId>

Create a Tag
------------
Use the following awscli command to create a **Tag** for the Main Route Table. Here, we're creating a Tag for the "Name" and setting it to "private"

.. code-block::

    aws ec2 create-tags --resources $EX002_RTB_PRIV --tags Key=Name,Value=private

Create a second Route Table
---------------------------
Use the following awscli command to create a second Route Table.


.. code-block::

    aws ec2 create-route-table --vpc-id $EX002_VPC

Output:

.. code-block::

    {
        "RouteTable": {
            "Associations": [],
            "PropagatingVgws": [],
            "RouteTableId": "rtb-xxxxxxxxxxxxxxxxx",
            "Routes": [
                {
                    "DestinationCidrBlock": "10.0.0.0/16",
                    "GatewayId": "local",
                    "Origin": "CreateRouteTable",
                    "State": "active"
                }
            ],
            "Tags": [],
            "VpcId": "vpc-xxxxxxxxxxxxxxxxx"
        }
    }

In the above output, we can see the same single entry under **Routes**. This will allow for the routing of local traffic for all subnets explicitly associated with this Route Table

Environment variable
~~~~~~~~~~~~~~~~~~~~
Just like above, we'll create another environment variable for our Route Table ID. In the output above, find the **'RouteTableId'** key.

.. code-block::

    export EX002_RTB_PUB=<RouteTableId>

Create a Tag
------------
Use the following awscli command to create a tag for the second Route Table. Here, we're creating a Tag for the "name" and setting it to "public".

.. code-block::

    aws ec2 create-tags --resources $EX002_RTB_PUB --tags Key=Name,Value=public

Sanity check
------------
Use the following command to show the tags that have been created and their assigned objects:

.. code-block::

    aws ec2 describe-tags

Output:

.. code-block::

    {
        "Tags": [
            {
                "ResourceType": "route-table",
                "ResourceId": "rtb-xxxxxxxxxxxxxxxxxx",
                "Value": "public",
                "Key": "Name"
            },
            {
                "ResourceType": "route-table",
                "ResourceId": "rtb-xxxxxxxxxxxxxxxxxx",
                "Value": "private",
                "Key": "Name"
            }
        ]
    }

Confirm that tags exist and are assigned to different **'ResourceIds'**.

Create an Internet Gateway
--------------------------
Use the following awscli command to create an Internet Gateway.

.. code-block::

    aws ec2 create-internet-gateway

Output:

.. code-block::

    {
        "InternetGateway": {
            "Attachments": [],
            "InternetGatewayId": "igw-xxxxxxxxxxxxxxxxx",
            "Tags": []
        }
    }

We will leverage this component to provide connectivity to/from the Internet for the **'public'** Subnet we will create later.

Environment variable
~~~~~~~~~~~~~~~~~~~~
Yep, another environment variable. In the output above, find the **'InternetGatewayId'** key.

.. code-block::

    export EX002_IG=<InternetGatewayId>

Attach the Internet Gateway
---------------------------
Use the following awscli command to attach the Internet Gateway to the VPC.

.. code-block::

      aws ec2 attach-internet-gateway --internet-gateway-id $EX002_IG --vpc-id $EX002_VPC

The above ommand does not return anything, but we can confirm it worked by running the following command:

.. code-block::

    aws ec2 describe-internet-gateways --filters Name=internet-gateway-id,Values=$EX002_IG

Output:

.. code-block::

    {
        "InternetGateways": [
            {
                "Attachments": [
                    {
                        "State": "available",
                        "VpcId": "vpc-xxxxxxxxxxxxxxxxxx"
                    }
                ],
                "InternetGatewayId": "igw-xxxxxxxxxxxxxxxxx",
                "Tags": []
            }
        ]
    }

You'll want to confirm that the VpcId is your VPC ID

Add a Route
-----------
Use the following awscli command to add a **Default Route** that targets the Internet Gateway to the **'public'** Route Table.

.. code-block::

    aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --gateway-id $EX002_IG --route-table-id $EX002_RTB_PUB

Output:

.. code-block::

    {
        "Return": true
    }

This will allow connectivity to/from the Internet for Subnets explicitly associated with this Route Table.

Examine the Route Table
-----------------------
Use the following awscli command to re-examine the **'public'** Route Table.

.. code-block::

    aws ec2 describe-route-tables --filter Name=route-table-id,Values=$EX002_RTB_PUB

Output:

.. code-block::

    {
        "RouteTables": [
            {
                "Associations": [],
                "PropagatingVgws": [],
                "RouteTableId": "rtb-xxxxxxxxxxxxxxxxx",
                "Routes": [
                    {
                        "DestinationCidrBlock": "10.0.0.0/16",
                        "GatewayId": "local",
                        "Origin": "CreateRouteTable",
                        "State": "active"
                    },
                    {
                        "DestinationCidrBlock": "0.0.0.0/0",
                        "GatewayId": "igw-xxxxxxxxxxxxxxxxx",
                        "Origin": "CreateRoute",
                        "State": "active"
                    }
                ],
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "public"
                    }
                ],
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx"
            }
        ]
    }

Now, we now see a second entry under **Routes**; the original has a **'GatewayId'** of 'local' and our new default route has a **'GatewayId'** that matches our Internet Gateway.

Create a Subnet
---------------
In AWS Subnets, the first address is the network address, the last address is the broadcast address and the second through fourth addresses are reserved by AWS

Use the following awscli command to create a Subnet with a CIDR of 10.0.0.0/23 . A prefix length of /23 results in 512 addresses (507 usable).

.. code-block::
   
   aws ec2 create-subnet --cidr-block 10.0.0.0/23 --vpc-id $EX002_VPC

Output:

.. code-block::

    {
        "Subnet": {
            "AvailabilityZone": "us-east-1c",
            "AvailableIpAddressCount": 507,
            "CidrBlock": "10.0.0.0/23",
            "DefaultForAz": false,
            "MapPublicIpOnLaunch": false,
            "State": "pending",
            "SubnetId": "subnet-xxxxxxxxxxxxxxxxx",
            "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
            "AssignIpv6AddressOnCreation": false,
            "Ipv6CidrBlockAssociationSet": []
        }
    }

Notice that the state is pending, but will become available shortly.

Environment variable
~~~~~~~~~~~~~~~~~~~~
Yep, another environment variable. In the output above, find the **'SubnetId'** key..

.. code-block::

    export EX002_SUBNET_PUB=<SubnetId>

Create a second Subnet
----------------------
Use the following awscli command to create a Subnet with a CIDR of 10.0.2.0/23 . A prefix length of /23 results in 512 addresses (507 usable).

.. code-block::

    aws ec2 create-subnet --cidr-block 10.0.2.0/23 --vpc-id $EX002_VPC

Output:

.. code-block::

    {
        "Subnet": {
            "AvailabilityZone": "us-east-1c",
            "AvailableIpAddressCount": 507,
            "CidrBlock": "10.0.2.0/23",
            "DefaultForAz": false,
            "MapPublicIpOnLaunch": false,
            "State": "pending",
            "SubnetId": "subnet-xxxxxxxxxxxxxxxxx",
            "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
            "AssignIpv6AddressOnCreation": false,
            "Ipv6CidrBlockAssociationSet": []
        }
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
Yep, another environment variable. In the output above, find the **'SubnetId'** key..

.. code-block::

    export EX002_SUBNET_PRIV=<SubnetId>

Verify the Subnets
------------------
Use the following awscli command to ensure that the State of both Subnets is **'available'**.

.. code-block::

    aws ec2 describe-subnets --filter Name=vpc-id,Values=$EX002_VPC

Output:

.. code-block::

    {
        "Subnets": [
            {
                "AvailabilityZone": "us-east-1c",
                "AvailableIpAddressCount": 507,
                "CidrBlock": "10.0.2.0/23",
                "DefaultForAz": false,
                "MapPublicIpOnLaunch": false,
                "State": "available",
                "SubnetId": "subnet-xxxxxxxxxxxxxxxxx",
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
                "AssignIpv6AddressOnCreation": false,
                "Ipv6CidrBlockAssociationSet": []
            },
            {
                "AvailabilityZone": "us-east-1c",
                "AvailableIpAddressCount": 507,
                "CidrBlock": "10.0.0.0/23",
                "DefaultForAz": false,
                "MapPublicIpOnLaunch": false,
                "State": "available",
                "SubnetId": "subnet-xxxxxxxxxxxxxxxxx",
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
                "AssignIpv6AddressOnCreation": false,
                "Ipv6CidrBlockAssociationSet": []
            }
        ]
    }

We can see that both Subnets were created in Availability Zone **'us-east-1c'**. If you wish to control where your Subnets are created, you would use the **'--availability-zone <value>'** option with the **'create-subnet'** command.

Create a Tag
------------
Use the following awscli commands to create a Tag for both Subnets.

.. code-block::

    aws ec2 create-tags --resources $EX002_SUBNET_PUB --tags Key=Name,Value=public 

    aws ec2 create-tags --resources $EX002_SUBNET_PRIV --tags Key=Name,Value=private 


Associate a Subnet
------------------
Use the following awscli command to associate the **'public'** subnet with the **'public'** Route Table.

.. code-block::

    aws ec2 associate-route-table --route-table-id $EX002_RTB_PUB --subnet-id $EX002_SUBNET_PUB

Output:

.. code-block::

    {
        "AssociationId": "rtbassoc-xxxxxxxxxxxxxxxxx"
    }

Examine the Route Table
-----------------------
Use the following awscli command to re-examine the **'public'** Route Table.

.. code-block::

    aws ec2 describe-route-tables --filter Name=route-table-id,Values=$EX002_RTB_PUB

Output:

.. code-block::


    {
        "RouteTables": [
            {
                "Associations": [
                    {
                        "Main": false,
                        "RouteTableAssociationId": "rtbassoc-xxxxxxxxxxxxxxxxx",
                        "RouteTableId": "rtb-xxxxxxxxxxxxxxxxx",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx"
                    }
                ],
                "PropagatingVgws": [],
                "RouteTableId": "rtb-xxxxxxxxxxxxxxxxx",
                "Routes": [
                    {
                        "DestinationCidrBlock": "10.0.0.0/16",
                        "GatewayId": "local",
                        "Origin": "CreateRouteTable",
                        "State": "active"
                    },
                    {
                        "DestinationCidrBlock": "0.0.0.0/0",
                        "GatewayId": "igw-xxxxxxxxxxxxxxxxx",
                        "Origin": "CreateRoute",
                        "State": "active"
                    }
                ],
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "public"
                    }
                ],
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx"
            }
        ]
    }

We can now see an entry under **Associations**.

See it in the AWS Console
-------------------------

- Login to your AWS Account.
- Select **Services** --> **Network & Content Delivery** --> **VPC**.
- In the navigation pane, click on **Your VPCs** to see a list of your VPCs.
- In the navigation pane, click on **Subnets** to see a list of your Subnets.
- In the navigation pane, click on **Route Tables** to see a list of your Route Tables.
- Select a Route Table, then in the bottom pane select **Routes** to see the Routes. 
- In the navigation pane, click on **Internet Gateways** to see a list of your Internet Gateways.


Summary
-------
- We created a VPC.
- We created a second Route Table and Tagged it 'public'
- We created an Internet Gateway.
- We attached the Internet Gateway to the VPC.
- We created a Default Route that targeted the Internet Gateway in the 'public' Route Table.
- We created two Subnets and Tagged them 'public' and 'private', respectively.
- We associated the 'public' Subnet with the 'public' Route Table.

Next steps
----------
We will test that our VPC configuration actually works as expected in 
`ex-003 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-003_TestingBasicConnectivity.rst>`_
