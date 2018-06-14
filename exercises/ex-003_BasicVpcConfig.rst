ex-003: Basic VPC configuration
===============================

Status
------
Draft (once the draft has been completed, a version number and date will be provided)

Introduction
------------
The primary purpose of this exercise become familiar with basic VPC configuration.

*None of the configuration items in this exercise is expected to generate an costs to your AWS account.*

Create a VPC
------------
Use the following awscli command to create a new VPC with a /16 prefix length (~64K addresses). It will be created in your **Default Region** (we specified this in ex-001).

If you wish to create a VPC in another **Region**, you would use the **--region <value>** option with the awscli.

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


Verify the VPC
--------------
Use the following awscli command to ensure that the VPC **State** is **available**.

.. code-block::
    
    aws ec2 describe-vpc --vpc-ids <VpcId>

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


Examine the default routing table
---------------------------------
Use the following awscli command to view main/default routing table. This is created automatically when a VPC is created. You can see a single entry under **Routes**. This will allow for the routing of traffic locally for all subnets associated with the main/default routing table. If you don't explicit;y associated a subnet with another routing table, it is implicitly associated with the main/default routing table.

We won't be modifying this routing table. We will use it to provide routing for the **private** subnets we create later.    

.. code-block::

    aws ec2 describe-route-tables --filter Name=vpc-id,Values=<VpcId>

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

Add a tag ('Name') to the main/default routing table
----------------------------------------------------
.. code-block::

    aws ec2 create-tags --resources <RouteTableId> --tags Key=Name,Value=private

Create a second routing table
-----------------------------
We can see the same single entry under **Routes**. This will allow for the routing of traffic locally for all subnets explicitly associated with this routing table

.. code-block::

    aws ec2 create-route-table --vpc-id <VpcId>

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

Add a tag ('Name') to the second routing table
----------------------------------------------
.. code-block::

    aws ec2 create-tags --resources <RouteTableId> --tags Key=Name,Value=private

Create an Internet Gateway
--------------------------
We will leverage the **Internet Gateway** to allow some subnets to be accessible from the Internet.

.. code-block::

    aws ec2 create-internet-gateway

    {
        "InternetGateway": {
            "Attachments": [],
            "InternetGatewayId": "igw-xxxxxxxxxxxxxxxxx",
            "Tags": []
        }
    }

Attach the Internet Gateway
---------------------------
We need to attach the **Internet Gateway** to the VPC.

.. code-block::

      aws ec2 attach-internet-gateway --internet-gateway-id <InternetGatewayId> --vpc-id <VpcId>


Add a route to the second routing table
---------------------------------------
We need to add a default route to the second routing table to leverage the **Internet Gateway**. 

.. code-block::

    aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --gateway-id <igw-InternetGatewayId> --route-table-id <RouteTableId>

    {
        "Return": true
    }

Re-examine the second routing table
-----------------------------------
We can see a second entry under **Routes**.

.. code-block::

    aws ec2 describe-route-tables --filter Name=route-table-id,Values=<RouteTableId>

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

Create a subnet
---------------
We created the subnet with a /23. This results in 512 addresses, but 507 addresses are usable. This is because, the first address is the network address, the last address is the broadcast address and the second through fourth addresses are reserved by AWS. 

.. code-block::
   
   aws ec2 create-subnet --cidr-block 10.0.0.0/23 --vpc-id <VpcId>

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

Create a second subnet for this VPC
-----------------------------------
We can also see that both subnets were created in **Availability Zone us-east-1c**.

If you wish to control where your subnets are created, you would use the **--availability-zone <value>** option with the **create-subnet** command.

.. code-block::
    aws ec2 create-subnet --cidr-block 10.0.2.0/23 --vpc-id <VpcId>

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

Verify that both subnets are available
--------------------------------------
.. code-block::

    aws ec2 describe-subnets --filter Name=vpc-id,Values=<VpcId>

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

Name (tag) the subnets **public** and **private**
-------------------------------------------------
.. code-block::

    aws ec2 create-tags --resources <SubnetId> --tags Key=Name,Value=public 

    aws ec2 create-tags --resources <SubnetId> --tags Key=Name,Value=private 


Associate one of the subnets
----------------------------
.. code-block::

    aws ec2 associate-route-table --route-table-id <RouteTableId> --subnet-id <SubnetId>

    {
        "AssociationId": "rtbassoc-xxxxxxxxxxxxxxxxx"
    }

Re-examine the second routing table
-----------------------------------
We can see a an entry under **Associations**.

.. code-block::

    aws ec2 describe-route-tables --filter Name=route-table-id,Values=<RouteTableId>


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

Next steps
----------
In the next exercise we will test that our configuration actually works by launching some instances and verifying connectivity. 

Summary
-------
