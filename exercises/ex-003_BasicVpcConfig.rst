ex-003: Basic VPC configuration
===============================

Status
------
Draft (once the draft has been completed, a version number and date will be provided)

Introduction
------------
The primary purpose of this exercise is to have you perform a basic VPC configuratione.

Creating a VPC in your default **Region**
-----------------------------------------
.. code-block::
    
    aws ec2 create-vpc --cidr-block 10.0.0.0/16

Let's explore the response.

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


Creating a VPC in another **Region**
------------------------------------
.. code-block::
    
    aws ec2   create-vpc --cidr-block 10.0.0.0/16 --region <region_name>
