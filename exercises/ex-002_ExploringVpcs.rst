ex-002: Exploring VPCs
======================

Status
------
Draft (once the draft has been completed, a version number and date will be provided)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001
   * - Prerequisite for exercise(s)
     - None

Objectives
----------
 
 - Become familiar with the basic concepts of VPC
 - Explore the default VPC in your default region. 

Expected Costs
--------------
The activities in this exercise are NOT expected to result in charges to your AWS account.

VPC
---
The AWS VPC (Virtual Private Cloud) gives you control over how your AWS network environment is laid out. You can:

- Create multiple VPCs in each region (see limits below)
- Assign a IPv4 CIDR block to your VPC
- Assign a IPv6 CIDR block to your VPC
- Create subnets
- Define which subnets will be public or private
- Create routing tables
- Create and assocaite Internet Gateways
- Configure NAT to allow private subnets to reach the Internet
- And much more... 

See the following for detailed information on VPC.

-  `Amazon Virtual Private Cloud <https://aws.amazon.com/vpc/>`_

Watch the following videos for more details on how VPCs work under the covers.

-  `AWS re:Invent 2015 | (NET403) Another Day, Another Billion Packets <https://www.youtube.com/watch?v=3qln2u1Vr2E>`_

-  `AWS re:Invent 2017: Advanced VPC Design and New Capabilities for Amazon VPC (NET305) <https://www.youtube.com/watch?v=Pj11NFXDbLY>`_






Default VPC
-----------
Even is you have just created your AWS account and haven't configured anything (other than the IAM user account from ex-001), you will still have a default VPC.

Let's take a look at the default VPC with the **describe-vpcs** command, adding the **'--filter'** option to select only the default VPC.  

.. code-block::
    
    aws ec2 describe-vpcs --filter Name=isDefault,Values=true


Now let's examine the output from that command, rearranging the order a bit.

.. code-block::
    
    {
    "Vpcs": [
        {
            "CidrBlock": "172.31.0.0/16",
            "DhcpOptionsId": "dopt-xxxxxxx",
            "State": "available",
            "VpcId": "vpc-xxxxxxxx",
            "InstanceTenancy": "default",
            "CidrBlockAssociationSet": [
                {
                    "AssociationId": "vpc-cidr-assoc-xxxxxxxx",
                    "CidrBlock": "172.31.0.0/16",
                    "CidrBlockState": {
                        "State": "associated"
                    }
                }
            ],
            "IsDefault": true
        }
    ]
    }

.. code-block::

    {
        "RouteTables": [
            {
                "Associations": [
                    {
                        "Main": true,
                        "RouteTableAssociationId": "rtbassoc-909d95ef",
                        "RouteTableId": "rtb-8707cff8"
                    }
                ],
                "PropagatingVgws": [],
                "RouteTableId": "rtb-8707cff8",
                "Routes": [
                    {
                        "DestinationCidrBlock": "172.31.0.0/16",
                        "GatewayId": "local",
                        "Origin": "CreateRouteTable",
                        "State": "active"
                    },
                    {
                        "DestinationCidrBlock": "0.0.0.0/0",
                        "GatewayId": "igw-3eb6ea46",
                        "Origin": "CreateRoute",
                        "State": "active"
                    }
                ],
                "Tags": [],
                "VpcId": "vpc-fffee284"
            }
        ]
    }

.. list-table::
   :widths: 20, 50
   :header-rows: 1

   * - Field
     - Description
   * - VpcId
     - 
   * - State
     - 
   * - CidrBlock
     - The block of IPv4 addresses assigned to this VPC.
   * - CidrBlockAssociationSet
     - 
   * - DhcpOptionsId
     - 
   * - InstanceTenancy
     - 
   * - IsDefault
     - 

Not shown in this example.

.. list-table::
   :widths: 20, 50
   :header-rows: 1

   * - Field
     - Description
   * - Ipv6CidrBlockAssociationSet
     - The block of IPv6 addresses assigned to this VPC.
   * - Tags
     - 

You can see the default VPC or all VPCs for another **Region** by using the following commands.  

.. code-block::
    
    aws ec2 describe-vpcs --filter Name=isDefault,Values=true --region REGION_NAME
    aws ec2 describe-vpcs --region REGION_NAME

|

VPC Limits
----------
.. list-table::
   :widths: 20, 20, 40
   :header-rows: 1

   * - Resource
     - Default limit
     - Comments
   * - VPCs per region
     - 5
     - The limit for internet gateways per region is directly correlated to this one. Increasing this limit increases the limit on internet gateways per region by the same amount. The number of VPCs in the region multiplied by the number of security groups per VPC cannot exceed 5000.
   * - Subnets per VPC
     - 200
     - 
   * - IPv4 CIDR blocks per VPC
     - 5
     - This limit is made up of your primary CIDR block plus 4 secondary CIDR blocks.
   * - IPv6 CIDR blocks per VPC
     - 1
     - This limit cannot be increased.

*Note: These limits are valid as of 06/13/18. Please you the following link to see the most up to data limits*
https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Appendix_Limits.html

