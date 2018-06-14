ex-003: Basic VPC configuration
===============================

Status
------
Draft (once the draft has been completed, a version number and date will be provided)

Introduction
------------
The primary purpose of this exercise is to have you perform a basic VPC configuration.

Create a VPC
------------
We will create a new VPC with a /16 prefix length (~64K addresses). It will be created in your **Default Region** (we specified this in ex-001). If you wish to create a VPC in another **Region**, you can use the **--region <value>** option with the awscli.

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


Verify that the VPC
-------------------
Ensure that **State** shows **available**.

.. code-block::
    
    aws ec2 describe-vpc --vpc-ids <VpcId>

    {
        "Vpcs": [
            {
                "CidrBlock": "10.0.0.0/16",
                "DhcpOptionsId": "dopt-267dc15d",
                "State": "available",
                "VpcId": "vpc-0ecc9b41c9206502b",
                "InstanceTenancy": "default",
                "CidrBlockAssociationSet": [
                    {
                        "AssociationId": "vpc-cidr-assoc-033bb5db516b80b28",
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


On your own
-----------

Create a VPC in another **Region**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::
    
    aws ec2   create-vpc --cidr-block 10.0.0.0/16 --region <region_name>


Examine the default routing table for this VPC
----------------------------------------------
.. code-block::

    aws ec2 describe-route-tables --filter Name=vpc-id,Values=<VpcId>

    {
        "RouteTables": [
            {
                "Associations": [
                    {
                        "Main": true,
                        "RouteTableAssociationId": "rtbassoc-065d3ee4cde2cd77f",
                        "RouteTableId": "rtb-0095efeac5ebedfaf"
                    }
                ],
                "PropagatingVgws": [],
                "RouteTableId": "rtb-0095efeac5ebedfaf",
                "Routes": [
                    {
                        "DestinationCidrBlock": "10.0.0.0/16",
                        "GatewayId": "local",
                        "Origin": "CreateRouteTable",
                        "State": "active"
                    }
                ],
                "Tags": [],
                "VpcId": "vpc-0ecc9b41c9206502b"
            }
        ]
    }

Create an Internet Gateway
--------------------------
.. code-block::

    aws ec2 create-internet-gateway

    {
        "InternetGateway": {
            "Attachments": [],
            "InternetGatewayId": "igw-047e3ab812d0ebeb2",
            "Tags": []
        }
    }


Attach the Internet Gateway to the VPC
--------------------------------------
.. code-block::

      aws ec2 attach-internet-gateway --internet-gateway-id igw-047e3ab812d0ebeb2 --vpc-id vpc-0ecc9b41c9206502b


Add default route to default routing table for this VPC
-------------------------------------------------------
.. code-block::

    aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --gateway-id igw-047e3ab812d0ebeb2 --route-table-id rtb-0095efeac5ebedfaf

    {
        "Return": true
    }


Re-examine the default routing table for this VPC
-------------------------------------------------
.. code-block::

    aws ec2 describe-route-tables --filter Name=vpc-id,Values=<VpcId>

    {
        "RouteTables": [
            {
                "Associations": [
                    {
                        "Main": true,
                        "RouteTableAssociationId": "rtbassoc-065d3ee4cde2cd77f",
                        "RouteTableId": "rtb-0095efeac5ebedfaf"
                    }
                ],
                "PropagatingVgws": [],
                "RouteTableId": "rtb-0095efeac5ebedfaf",
                "Routes": [
                    {
                        "DestinationCidrBlock": "10.0.0.0/16",
                        "GatewayId": "local",
                        "Origin": "CreateRouteTable",
                        "State": "active"
                    },
                    {
                        "DestinationCidrBlock": "0.0.0.0/0",
                        "GatewayId": "igw-047e3ab812d0ebeb2",
                        "Origin": "CreateRoute",
                        "State": "active"
                    }
                ],
                "Tags": [],
                "VpcId": "vpc-0ecc9b41c9206502b"
            }
        ]
    }

Create a subnet for this VPC
----------------------------
.. code-block::
   
   aws ec2 create-subnet --cidr-block 10.0.0.0/23 --vpc-id vpc-0ecc9b41c9206502b

    {
        "Subnet": {
            "AvailabilityZone": "us-east-1c",
            "AvailableIpAddressCount": 507,
            "CidrBlock": "10.0.0.0/23",
            "DefaultForAz": false,
            "MapPublicIpOnLaunch": false,
            "State": "pending",
            "SubnetId": "subnet-00ab76a6ccaaee13d",
            "VpcId": "vpc-0ecc9b41c9206502b",
            "AssignIpv6AddressOnCreation": false,
            "Ipv6CidrBlockAssociationSet": []
        }
    }

Create a second subnet for this VPC
-----------------------------------
.. code-block::
    aws ec2 create-subnet --cidr-block 10.0.2.0/23 --vpc-id vpc-0ecc9b41c9206502b

    {
        "Subnet": {
            "AvailabilityZone": "us-east-1c",
            "AvailableIpAddressCount": 507,
            "CidrBlock": "10.0.2.0/23",
            "DefaultForAz": false,
            "MapPublicIpOnLaunch": false,
            "State": "pending",
            "SubnetId": "subnet-037dd3a0e579a8da7",
            "VpcId": "vpc-0ecc9b41c9206502b",
            "AssignIpv6AddressOnCreation": false,
            "Ipv6CidrBlockAssociationSet": []
        }
    }

Verify that both subnets are available
--------------------------------------
.. code-block::

    aws ec2 describe-subnets --filter Name=vpc-id,Values=vpc-0ecc9b41c9206502b

    {
        "Subnets": [
            {
                "AvailabilityZone": "us-east-1c",
                "AvailableIpAddressCount": 507,
                "CidrBlock": "10.0.2.0/23",
                "DefaultForAz": false,
                "MapPublicIpOnLaunch": false,
                "State": "available",
                "SubnetId": "subnet-037dd3a0e579a8da7",
                "VpcId": "vpc-0ecc9b41c9206502b",
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
                "SubnetId": "subnet-00ab76a6ccaaee13d",
                "VpcId": "vpc-0ecc9b41c9206502b",
                "AssignIpv6AddressOnCreation": false,
                "Ipv6CidrBlockAssociationSet": []
            }
        ]
    }

Name the subnets **public** and **private** using a tag
-------------------------------------------------------
.. code-block::

    aws ec2 create-tags --resources subnet-00ab76a6ccaaee13d --tags Key=Name,Value=public 

    aws ec2 create-tags --resources subnet-037dd3a0e579a8da7 --tags Key=Name,Value=private 

Create a new routing table to isolate the private network
---------------------------------------------------------





