ex-002: Basic VPC configuration
===============================

Status
------
Version 1.0 (6/18/18)

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

    - Become familiar with basic VPC configuration.

Expected Costs
--------------
The activities in this exercise are NOT expected to result in any charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 1

   * - Component
     - Applicable Costs
     - Notes
   * - VPC (including subnets, Route Tables and IntenetGateways).
     - None
     - 
        + AWS does not charge for the basic VPC building blocks used in this exercise.
        + We will be leaving this configuration in place to support ex-003.

Limits
------
The following table shows the default limits for the components utilized in this exercise.

``NOTE: You can view all your EC2 limits and request increases by clicking on 'Limits' in the navigation pane of the EC2 console.``

.. list-table::
   :widths: 25, 25
   :header-rows: 1

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
During this exercise, we will be creating environment variables to simplify the syntax of commands run later in the exercise. I have decided to do this manually, because I want to show the the full output from each command and not redirect a filtered output directly into a variable.

Once you are comfortable with the expected output of a command and wish filter the output, then you might want to try the **'--query'** and **'--output'** options available in the awscli command.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Create a VPC
------------
Use the following awscli command to create a new VPC with a /16 prefix length (~64K addresses).

It will be created in your **Default Region** (we specified this in ex-001). If you wish to create a VPC in another Region, you would use the **'--region <value>'** option with the awscli.

``LIMITS: The default limit for VPCs per Region is 5. You would need to open a support case to increase that number.``

.. code-block::
    
    aws ec2 create-vpc --cidr-block 10.0.0.0/16

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
.. code-block::

    export EX002_VPC=<VpcId>

Verify the VPC
--------------
Use the following awscli command to ensure that the VPC State is **'available'**.

.. code-block::
    
    aws ec2 describe-vpcs --vpc-ids $EX002_VPC

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


Examine the default Route Table
-------------------------------
Use the following awscli command to view main/default Route Table.

This is created automatically when a VPC is created. You can see a single entry under **Routes**. This entry will allow for the routing of local traffic for all Subnets associated with the main/default Route Table. If you don't explicitly associate a subnet with another Route Table, it is implicitly associated with the main/default Route Table.

We won't be modifying this Route Table. We will use it to provide routing for the **'private'** Subnet we will create later. Since newly created Subnets are implicitly associated with the main/default Route Table, it would seem to be a good practice to provide reachability to/from the Internet via a separate Route Table. 

.. code-block::

    aws ec2 describe-route-tables --filter Name=vpc-id,Values=$EX002_VPC

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

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX002_RTB_PRIV=<RouteTableId>

Create a Tag
------------
Use the following awscli command to create a **Tag** for the main/default Route Table.

.. code-block::

    aws ec2 create-tags --resources $EX002_RTB_PRIV --tags Key=Name,Value=private

Create a second Route Table
---------------------------
Use the following awscli command to create a second Route Table.

We can see the same single entry under **Routes**. This will allow for the routing of local traffic for all subnets explicitly associated with this Route Table

.. code-block::

    aws ec2 create-route-table --vpc-id $EX002_VPC

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

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX002_RTB_PUB=<RouteTableId>

Create a Tag
------------
Use the following awscli command to create a tag for the second Route Table.

.. code-block::

    aws ec2 create-tags --resources $EX002_RTB_PUB --tags Key=Name,Value=public

Create an Internet Gateway
--------------------------
Use the following awscli command to create an Internet Gateway.

We will leverage this component to provide connectivity to/from the Internet for the **'public'** Subnet we create later.

.. code-block::

    aws ec2 create-internet-gateway

    {
        "InternetGateway": {
            "Attachments": [],
            "InternetGatewayId": "igw-xxxxxxxxxxxxxxxxx",
            "Tags": []
        }
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX002_IG=<InternetGatewayId>

Attach the Internet Gateway
---------------------------
Use the following awscli command to attach the Internet Gateway to the VPC.

.. code-block::

      aws ec2 attach-internet-gateway --internet-gateway-id $EX002_IG --vpc-id $EX002_VPC


Add a Route
-----------
Use the following awscli command to add a **Default Route** that targets the Internet Gateway to the **'public'** Route Table.

This will allow connectivity to/from the Internet for Subnets explicitly associated with this Route Table.

.. code-block::

    aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --gateway-id $EX002_IG --route-table-id $EX002_RTB_PUB

    {
        "Return": true
    }

Examine the Route Table
-----------------------
Use the following awscli command to re-examine the **'public'** Route Table.

We can see a second entry under **Routes**.

.. code-block::

    aws ec2 describe-route-tables --filter Name=route-table-id,Values=$EX002_RTB_PUB

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

Create a Subnet
---------------
Use the following awscli command to create a Subnet with a prefix length of /23 (512 addresses).

We only 507 usable addresses. This is because, the first address is the network address, the last address is the broadcast address and the second through fourth addresses are reserved by AWS. 

.. code-block::
   
   aws ec2 create-subnet --cidr-block 10.0.0.0/23 --vpc-id $EX002_VPC

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

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX002_SUBNET_PUB=<SubnetId>

Create a second Subnet
----------------------
Use the following awscli command to create a Subnet with a prefix length of /23 (512 addresses).

.. code-block::

    aws ec2 create-subnet --cidr-block 10.0.2.0/23 --vpc-id $EX002_VPC

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
.. code-block::

    export EX002_SUBNET_PRIV=<SubnetId>

Verify the Subnets
------------------
Use the following awscli command to ensure that the State of both Subnets is **'available'**.

We can see that both Subnets were created in Availability Zone **'us-east-1c'**.

If you wish to control where your Subnets are created, you would use the **'--availability-zone <value>'** option with the **'create-subnet'** command.

.. code-block::

    aws ec2 describe-subnets --filter Name=vpc-id,Values=$EX002_VPC

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

    {
        "AssociationId": "rtbassoc-xxxxxxxxxxxxxxxxx"
    }

Examine the Route Table
-----------------------
Use the following awscli command to re-examine the **'public'** Route Table.

We can now see an entry under **Associations**.

.. code-block::

    aws ec2 describe-route-tables --filter Name=route-table-id,Values=$EX002_RTB_PUB


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
`ex-004 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-004_TestingBasicConnectivity.rst>`_
