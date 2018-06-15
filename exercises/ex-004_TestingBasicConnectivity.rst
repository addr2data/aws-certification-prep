ex-004: Testing basic connectivity
==================================

Status
------
Draft (once the draft has been completed, a version number and date will be provided)

Introduction
------------
The primary purpose of this exercise is to become familiar with launching on-demand instances, connecting to those instances and testing the VPC configuration from ex-003. 

*Note:  The activities in this exercise are expected to generate any costs to your AWS account.*

Create a Key Pair
-----------------
Use the following awscli command to create a new **Key Pair** and save the resulting **'.pem'** file.

You can have up to 5000 Key Pairs per region.

*Note: I have only verified that **'> <filename>'** produces a valid '.pem' on macOS.*

.. code-block::
    
    aws ec2 create-key-pair --key-name acpkey1 --query 'KeyMaterial' --output text > acpkey1.pem

Modify permissions
------------------
Use the following command to modify the permissions on the '.pem'.

.. code-block::
    
    chmod 400 acpkey1.pem

Create a Security Group
-----------------------
Use the following awscli command to create a new Security Group.

You can create up to 500 security groups per VPC

.. code-block::

    aws ec2 create-security-group --group-name Int2Public --description "Security Group used to connect to instances on public subnet from Internet" --vpc-id vpc-0ecc9b41c9206502b

    {
        "GroupId": "sg-01f180a16b3948693"
    }

Create add a rule
-----------------
Use the following awscli command to create a new rule to the above security group.

.. code-block::

    aws ec2 authorize-security-group-ingress --group-id sg-01f180a16b3948693 --protocol tcp --port 22 --cidr 0.0.0.0/0

Examine the Security Group
--------------------------
Use the following awscli command to examine the above security group.

.. code-block::

    aws ec2 describe-security-groups --group-ids sg-0d7c69511ecdbf73a

    {
        "SecurityGroups": [
            {
                "Description": "Security Group used to connect to instances on public subnet from Internet",
                "GroupName": "Int2Public",
                "IpPermissions": [
                    {
                        "FromPort": 22,
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "ToPort": 22,
                        "UserIdGroupPairs": []
                    }
                ],
                "OwnerId": "xxxxxxxxxxxx",
                "GroupId": "sg-xxxxxxxxxxxxxxxxx",
                "IpPermissionsEgress": [
                    {
                        "IpProtocol": "-1",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0"
                            }
                        ],
                        "Ipv6Ranges": [],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": []
                    }
                ],
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx"
            }
        ]
    }

Launch an Instance
-------------------
Use the following awscli command to launch an Instance in the 'public' Subnet.

*Reminder: The only thing that makes that Subnet public is that it is associated with a Route Table that has a Route to the Internet Gateway.

We have used the option **'--client-token'** to ensure this operation is  Idempotent.

- `More information on Idempotency <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Run_Instance_Idempotency.html>`_

.. code-block::

    aws ec2 run-instances --image-id ami-a4dc46db --instance-type t2.micro --key-name acpkey1 --subnet-id subnet-00ab76a6ccaaee13d --security-group-ids sg-01f180a16b3948693 --client-token awscertprep-ex-004-004

Allocate an Elastic IP
----------------------
Use the following awscli command to allocate a public IPv4 address

.. code-block::

    aws ec2 allocate-address --domain vpc

    {
        "PublicIp": "54.89.230.154",
        "AllocationId": "eipalloc-090dfc687075050e2",
        "Domain": "vpc"
    }

Associate the Elastic IP
------------------------
Use the following awscli command to associate the Elastic IP with the Instance we just launched.

.. code-block::

    aws ec2 associate-address --allocation-id eipalloc-090dfc687075050e2 --instance-id i-0c19982239ebb148d

    {
        "AssociationId": "eipassoc-097543d512f520d2d"
    }

Connect to the Instance
-----------------------
Use the following command to test connectivity to the Instance via the Elastic IP.

.. code-block::
    ssh -i acpkey1.pem ubuntu@54.89.230.154







