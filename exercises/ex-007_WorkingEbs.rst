ex-007: Working with EBS
========================

Status
------
Draft (not complete)

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
   * - EBS (storage)
     - 
        + gp2: Between $0.10 and $0.19 per GB-month of provisioned storage, depending on your region.
        + io1: Between $0.125 and $0.238 per GB-month of provisioned storage, depending on your region.
        + st1: Between $0.045 and $0.086 per GB-month of provisioned storage, depending on your region.
        + sc1: Between $0.025 and $0.048 per GB-month of provisioned storage, depending on your region.
     -
        + Amazon EBS General Purpose SSD (gp2) volumes
        + Amazon EBS Provisioned IOPS SSD (io1) volumes
        + Amazon EBS Throughput Optimized HDD (st1) volumes
        + Amazon EBS Cold HDD (sc1) volumes
   * - EBS (iops)
     - 
        + io1: Between $0.065 and $0.091 per provisioned IOPS-month
     -
        + Amazon EBS Provisioned IOPS SSD (io1) volumes

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

Create Stack
------------
Use the following awscli command to create a new CloudFormation **'Stack'** based on the template.

Note: If you are using the **'acpkey1'** Key Pair, you can leave off the **'--parameters'** option all together.

.. code-block::

    aws cloudformation create-stack \
        --stack-name ex-007 \
        --template-body file://templates/ex-007_template.yaml \
        --parameters ParameterKey=KeyPairName,ParameterValue=acpkey1

Output:

.. code-block::

    {
        "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-006/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }

Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this command until **'StackStatus'** is **'CREATE_COMPLETE'**.

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-007

Output:

.. code-block::

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-007/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "StackName": "ex-007",
                "CreationTime": "2018-06-19T19:56:35.434Z",
                "RollbackConfiguration": {},
                "StackStatus": "CREATE_IN_PROGRESS",
                "DisableRollback": false,
                "NotificationARNs": [],
                "Tags": [],
                "EnableTerminationProtection": false
            }
        ]
    }

Review the Stack details
------------------------
Use the following awscli command to display the **'LogicalResourceId'** and **'PhysicalResourceId'** for all the components in the **Stack**

Notice the format of this portion of the query string **'{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'**, it adds a header to each column.** 

.. code-block::

    aws cloudformation describe-stack-resources \
        --stack-name ex-007 \
        --output table \
        --query 'StackResources[*].{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'

Output:

.. code-block::

    -------------------------------------------------------------------
    |                     DescribeStackResources                      |
    +----------------------------------+------------------------------+
    |        Logical Resource Id       |    Physical Resource Id      |
    +----------------------------------+------------------------------+
    |  AssociateSubnetRouteTablePublic |  rtbassoc-09c998a93d864f70c  |
    |  AttachInternetGateway           |  ex-00-Attac-WDLTSAHTMD9V    |
    |  DefaultRoutePublic              |  ex-00-Defau-1TCX8KG49DZBJ   |
    |  Instance1                       |  i-0f28de878eb1331c3         |
    |  Instance2                       |  i-094a150583aa25923         |
    |  InternetGateway                 |  igw-0491690a9c3213a37       |
    |  RouteTablePublic                |  rtb-0e2d9f380384e7de4       |
    |  SecurityGroup                   |  sg-0e0f80489c622a2a6        |
    |  Subnet                          |  subnet-05a45c4d675b278cb    |
    |  VPC                             |  vpc-00e3fc9ac6986954e       |
    +----------------------------------+------------------------------+

Environment variables
~~~~~~~~~~~~~~~~~~~~~
Run the following commands to capture the 'PhysicalResourceId' for the applicable components, as environment variables.

.. code-block::

    export EX007_INST_01=$(aws cloudformation describe-stack-resources --stack-name ex-007 --output text --query 'StackResources[?LogicalResourceId==`Instance1`].PhysicalResourceId')

    export EX007_INST_02=$(aws cloudformation describe-stack-resources --stack-name ex-007 --output text --query 'StackResources[?LogicalResourceId==`Instance2`].PhysicalResourceId')

Sanity check
~~~~~~~~~~~~

.. code-block::
    
    echo -e '\n'$EX007_INST_01'\n'$EX007_INST_02

Display block storage information
---------------------------------
Use the following awscli command to display the block storage information for both Instances.

.. code-block::

    aws ec2 describe-instances \
        --instance-ids $EX007_INST_01 $EX007_INST_02 \
        --query 'Reservations[*].Instances[*].{BlockDeviceMappings: BlockDeviceMappings,RootDeviceName: RootDeviceName,RootDeviceType: RootDeviceType}'

Output:

.. code-block::

    [
        [
            {
                "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/sda1",
                        "Ebs": {
                            "AttachTime": "2018-06-28T16:52:12.000Z",
                            "DeleteOnTermination": true,
                            "Status": "attached",
                            "VolumeId": "vol-087b5e30b2918119a"
                        }
                    }
                ],
                "RootDeviceName": "/dev/sda1",
                "RootDeviceType": "ebs"
            }
        ],
    
        [
            {
                "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/sda1",
                        "Ebs": {
                            "AttachTime": "2018-06-28T16:52:12.000Z",
                            "DeleteOnTermination": true,
                            "Status": "attached",
                            "VolumeId": "vol-0878fcd959666083b"
                        }
                    }
                ],
                "RootDeviceName": "/dev/sda1",
                "RootDeviceType": "ebs"
            }
        ]
    ]

Display volume information
--------------------------
Use the following awscli command to display the volume information for both Instances.

.. code-block::

    aws ec2 describe-instances \
        --instance-ids $EX007_INST_01 $EX007_INST_02 \
        --output text \
        --query Reservations[*].Instances[*].BlockDeviceMappings[*].Ebs.VolumeId |
        while read line;
        do aws ec2 describe-volumes --volume-ids $line;
        done

Output:

.. code-block::

    {
        "Volumes": [
            {
                "Attachments": [
                    {
                        "AttachTime": "2018-06-28T16:52:12.000Z",
                        "Device": "/dev/sda1",
                        "InstanceId": "i-094a150583aa25923",
                        "State": "attached",
                        "VolumeId": "vol-087b5e30b2918119a",
                        "DeleteOnTermination": true
                    }
                ],
                "AvailabilityZone": "us-east-1e",
                "CreateTime": "2018-06-28T16:52:12.066Z",
                "Encrypted": false,
                "Size": 8,
                "SnapshotId": "snap-0eea1ed47e203f3b8",
                "State": "in-use",
                "VolumeId": "vol-087b5e30b2918119a",
                "Iops": 100,
                "VolumeType": "gp2"
            }
        ]
    }
    {
        "Volumes": [
            {
                "Attachments": [
                    {
                        "AttachTime": "2018-06-28T16:52:12.000Z",
                        "Device": "/dev/sda1",
                        "InstanceId": "i-0f28de878eb1331c3",
                        "State": "attached",
                        "VolumeId": "vol-0878fcd959666083b",
                        "DeleteOnTermination": true
                    }
                ],
                "AvailabilityZone": "us-east-1e",
                "CreateTime": "2018-06-28T16:52:12.003Z",
                "Encrypted": false,
                "Size": 8,
                "SnapshotId": "snap-0eea1ed47e203f3b8",
                "State": "in-use",
                "VolumeId": "vol-0878fcd959666083b",
                "Iops": 100,
                "VolumeType": "gp2"
            }
        ]
    }


Environment variables
~~~~~~~~~~~~~~~~~~~~~
Run the following commands to capture the 'VolumeId' for each Instance.

.. code-block::

    export EX007_INST_01_VOL=$(aws ec2 describe-instances --instance-ids $EX007_INST_01 --output text --query Reservations[*].Instances[*].BlockDeviceMappings[*].Ebs.VolumeId)

    export EX007_INST_02_VOL=$(aws ec2 describe-instances --instance-ids $EX007_INST_02 --output text --query Reservations[*].Instances[*].BlockDeviceMappings[*].Ebs.VolumeId)

Sanity check
~~~~~~~~~~~~

.. code-block::
    
    echo -e '\n'$EX007_INST_01_VOL'\n'$EX007_INST_02_VOL





Modify the size of a volume
---------------------------

.. code-block::

    aws ec2 modify-volume --volume-id $EX007_INST_01_VOL --size 10

Output:

.. code-block::

    {
        "VolumeModification": {
            "VolumeId": "vol-0878fcd959666083b",
            "ModificationState": "modifying",
            "TargetSize": 10,
            "TargetIops": 100,
            "TargetVolumeType": "gp2",
            "OriginalSize": 8,
            "OriginalIops": 100,
            "OriginalVolumeType": "gp2",
            "Progress": 0,
            "StartTime": "2018-06-28T21:09:35.000Z"
        }
    }

Notice that the **'ModificationState'** is **'modifying'**

.. code-block::

    aws ec2 describe-volumes-modifications --volume-ids $EX007_INST_01_VOL

Output:

.. code-block::

    {
        "VolumesModifications": [
            {
                "VolumeId": "vol-0878fcd959666083b",
                "ModificationState": "optimizing",
                "TargetSize": 10,
                "TargetIops": 100,
                "TargetVolumeType": "gp2",
                "OriginalSize": 8,
                "OriginalIops": 100,
                "OriginalVolumeType": "gp2",
                "Progress": 1,
                "StartTime": "2018-06-28T21:09:35.000Z"
            }
        ]
    }



Summary
-------
- To be added

Next steps
----------
In `ex-008 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-008_GettingStartedSnapshots.rst>`_, we will get started with Snapshots.

