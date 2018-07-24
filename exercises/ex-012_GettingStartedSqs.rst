ex-012: Getting Started with Simple Queue Service
=================================================

Status
------
Draft 0.5 (07/24/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001
   * - Prerequisite for exercise(s)
     - none

Objectives
----------
- To be added

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
   * - To be added
     - 
        + To be added
     -
        + To be added

Limits
------
The following table shows the default limits for the components utilized in this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - To be added
     - To be added

Environment variables
---------------------
During these exercises, we will be using the output of some commands to create environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Amazon Machine Image (AMI)
--------------------------
We are going to use the following AMI, but the **'imageIds'**, for that AMI, are different for each region:

``Ubuntu Server 16.04 LTS (HVM), SSD Volume Type``

Use the following table to identify the **'imageId'** for your region.

.. list-table::
   :widths: 25, 25, 25, 25, 25, 25
   :header-rows: 0

   * - **Region**
     - **ImageId**
     - **Region**
     - **ImageId**
     - **Region**
     - **ImageId**
   * - us-east-1
     - ami-a4dc46db
     - us-east-2
     - ami-6a003c0f
     - us-west-1
     - ami-8d948ced
   * - us-west-2
     - ami-db710fa3
     - ca-central-1
     - ami-7e21a11a
     - eu-west-1
     - ami-58d7e821
   * - eu-west-2
     - ami-5daa463a
     - eu-west-3
     - ami-1960d164
     - eu-central-1
     - ami-c7e0c82c
   * - ap-northeast-1
     - ami-48a45937
     - ap-northeast-2
     - ami-f030989e
     - ap-southeast-1
     - ami-81cefcfd
   * - ap-southeast-2
     - ami-963cecf4
     - ap-south-1
     - ami-41e9c52e
     - sa-east-1
     - ami-67fca30b

Environment Variable
~~~~~~~~~~~~~~~~~~~~
Create an environment variable using your ImageId.

.. code-block::

    export EX012_IMAGE_ID=<ImageId>
    export EX012_IMAGE_ID=ami-a4dc46db

Launch an Instance
-------------------
Use the following awscli command to launch an Instance.

**If you are using a different Key Pair, then replace 'acpkey1' with your '<key-pair-name>'**.

.. code-block::

    aws ec2 run-instances \
        --image-id $EX012_IMAGE_ID \
        --instance-type t2.micro \
        --key-name acpkey1 \
        --associate-public-ip-address

Output:

.. code-block::

    {
        "Groups": [],
        "Instances": [
            {
                "AmiLaunchIndex": 0,
                "ImageId": "ami-a4dc46db",
                "InstanceId": "i-053556b3d9cd148ba",
                "InstanceType": "t2.micro",
                "KeyName": "acpkey1",
                "LaunchTime": "2018-07-24T16:49:11.000Z",
                "Monitoring": {
                    "State": "disabled"
                },
                "Placement": {
                    "AvailabilityZone": "us-east-1c",
                    "GroupName": "",
                    "Tenancy": "default"
                },
                "PrivateDnsName": "ip-172-31-91-8.ec2.internal",
                "PrivateIpAddress": "172.31.91.8",
                "ProductCodes": [],
                "PublicDnsName": "",
                "State": {
                    "Code": 0,
                    "Name": "pending"
                },
                "StateTransitionReason": "",
                "SubnetId": "subnet-0d015b27e803f137c",
                "VpcId": "vpc-0bad0021d156b3192",
                "Architecture": "x86_64",
                "BlockDeviceMappings": [],
                "ClientToken": "",
                "EbsOptimized": false,
                "Hypervisor": "xen",
                "NetworkInterfaces": [
                    {
                        "Attachment": {
                            "AttachTime": "2018-07-24T16:49:11.000Z",
                            "AttachmentId": "eni-attach-04553a68560b957de",
                            "DeleteOnTermination": true,
                            "DeviceIndex": 0,
                            "Status": "attaching"
                        },
                        "Description": "",
                        "Groups": [
                            {
                                "GroupName": "default",
                                "GroupId": "sg-0d800c87283a0b7b1"
                            }
                        ],
                        "Ipv6Addresses": [],
                        "MacAddress": "12:52:c8:b8:a8:56",
                        "NetworkInterfaceId": "eni-0ef69225bece75760",
                        "OwnerId": "926075045128",
                        "PrivateDnsName": "ip-172-31-91-8.ec2.internal",
                        "PrivateIpAddress": "172.31.91.8",
                        "PrivateIpAddresses": [
                            {
                                "Primary": true,
                                "PrivateDnsName": "ip-172-31-91-8.ec2.internal",
                                "PrivateIpAddress": "172.31.91.8"
                            }
                        ],
                        "SourceDestCheck": true,
                        "Status": "in-use",
                        "SubnetId": "subnet-0d015b27e803f137c",
                        "VpcId": "vpc-0bad0021d156b3192"
                    }
                ],
                "RootDeviceName": "/dev/sda1",
                "RootDeviceType": "ebs",
                "SecurityGroups": [
                    {
                        "GroupName": "default",
                        "GroupId": "sg-0d800c87283a0b7b1"
                    }
                ],
                "SourceDestCheck": true,
                "StateReason": {
                    "Code": "pending",
                    "Message": "pending"
                },
                "VirtualizationType": "hvm",
                "CpuOptions": {
                    "CoreCount": 1,
                    "ThreadsPerCore": 1
                }
            }
        ],
        "OwnerId": "926075045128",
        "ReservationId": "r-08fce93090165bb3f"
    }

Environment Variable
~~~~~~~~~~~~~~~~~~~~

.. code-block::

    export EX012_IMAGE_ID=<ImageId>


.. code-block::

aws ec2 describe-instances
[--filters <value>]
[--instance-ids <value>]
[--dry-run | --no-dry-run]
[--cli-input-json <value>]
[--starting-token <value>]
[--page-size <value>]
[--max-items <value>]
[--generate-cli-skeleton <value>]







Summary
-------
- To be added

Next steps
----------
To be added, in 
`ex-xxx <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/<name-of-file>>`_

