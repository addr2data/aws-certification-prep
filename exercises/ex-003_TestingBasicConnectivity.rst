ex-003: Testing basic connectivity
==================================

Status
------
Version 1.1 (6/24/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001, ex-002
   * - Prerequisite for exercise(s)
     - None

Objectives
----------

    - Become familiar with launching and connecting to on-demand Instances.
    - Test connectivity for the VPC configuration we created in ex-002.

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 1

   * - Component
     - Applicable Costs
     - Notes
   * - Security Groups
     - None
     -
   * - On-demand Instances
     - 
        + $0.0116 per hour per Instance (t2.micro)
     - 
        + During this exercise we will be launching two Instances, using the Ubuntu Server 16.04 LTS AMI, which is 'Free tier eligible'.
        + It is not expected that these Instances will need to be running for more than one hour. 
   * - Elastic IPs
     - 
        + $0.00 per hour per EIP that is associated to a running Instance
        + $0.05 per hour per EIP that is NOT associated to a running Instance
     - During this exercise there will be short periods of time where an EIP is not associated with an running Instance, so you might incur a very small charge.
   * - Elastic IPs
     - 
        + $0.00 per EIP address remap for the first 100 remaps per month.
        + $0.10 per EIP address remap for additional remaps over 100 per month
     - During this exercise we will remap an EIP a couple of times.  

Limits
------
The following table shows the default limits for the components utilized in this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 1

   * - **Component**
     - **Limit**
   * - Security Groups
     - 500 per VPC
   * - Security Groups per Elastic Network Interface
     - 5
   * - Rules per Security Group
     - 50
   * - On-demand Instances
     - 20 per region
   * - Elastic IP adresses
     - 5 per region

Environment variables
---------------------
During this exercise, we will be creating environment variables to simplify the syntax of commands run later in the exercise. I have decided to do this manually, because I want to show the the full output from each command and not redirect a filtered output directly into a variable.

Once you are comfortable with the expected output of a command and wish filter the output, then you might want to try the **'--query'** and **'--output'** options available in the awscli command.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Create a Security Group
-----------------------
We will be adding the Instances that we create later in the exercise to this Security Group.

**Note: We'll be reusing the environment variables created in the previous exercise**

Use the following awscli command to create a new Security Group.

.. code-block::

    aws ec2 create-security-group --group-name Int2Public --description "Security Group used to connect to instances on public subnet from Internet" --vpc-id $EX002_VPC

Output:

.. code-block::

    {
        "GroupId": "sg-xxxxxxxxxxxxxxxxx"
    }

Troubleshooting:
~~~~~~~~~~~~~~~~
If you get an error that reads **'aws: error: argument --vpc-id: expected one argument'**, it probably means that your EX002_VPC environment variable is not set. You can retreive the VPC ID value by running the following command:

.. code-block::

    aws ec2 describe-vpcs

Then set the environment variable again:

.. code-block::

    export EX002_VPC=<VpcId>


Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX003_SG=<GroupId>

Add a rule to the Security Group
--------------------------------
We'll need to add an ingress rule to our security group. This rule will allow inbound traffic to SSH (tcp port 22) from anywhere (0.0.0.0/0). By default, Security Groups allows all outbound traffic.

We will cover Security Groups in more detail in a later exercise.

Use the following awscli command to add a rule to the above security group.

.. code-block::

    aws ec2 authorize-security-group-ingress --group-id $EX003_SG --protocol tcp --port 22 --cidr 0.0.0.0/0

Examine the Security Group
--------------------------
Use the following awscli command to examine the above security group.

.. code-block::

    aws ec2 describe-security-groups --group-ids $EX003_SG

Output:

.. code-block::

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

Amazon Machine Image (AMI)
--------------------------
We are going to use the following AMI, but the 'imageIds' are different for each region:

``Ubuntu Server 16.04 LTS (HVM), SSD Volume Type``

Use the following table to identify the 'imageId' for your region.

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

Create an environment variable using your ImageId.

.. code-block::

    export EX003_IMAGE_ID=<ImageId>


Launch an Instance
-------------------
Use the following awscli command to launch an Instance and attach to the **'public'** Subnet. From here onwards, we will refer to this Instance as the 'public' Instance.

**Note: The only thing that makes it a 'public' Subnet is the fact that it is associated with a Route Table that has a default Route to the Internet Gateway.``

We have used the **'--client-token'** to option ensure this operation is  Idempotent.

- `More information on Idempotency <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Run_Instance_Idempotency.html>`_

.. code-block::

    aws ec2 run-instances --image-id $EX003_IMAGE_ID --instance-type t2.micro --key-name acpkey1 --subnet-id $EX003_SUBNET_PUB --security-group-ids $EX003_SG --client-token awscertprep-ex-003-001

Additional information on the above parameters:

.. list-table::
   :widths: 50, 50
   :header-rows: 0

   * - **Parameter**
     - **Description**
   * - '--image-id $EX003_IMAGE_ID'
     - What AMI to use
   * - '--instance-type t2.micro'
     - The Instance type defines the number of vCPUs, the amount of Memory, the size and type Storage, Network performance, etc...
   * - '--key-name acpkey1'
     - What Key Pair to use.
   * - '--subnet-id $EX003_SUBNET_PUB'
     - 
   * - '--security-group-ids $EX003_SG'
     - 
   * - '--client-token awscertprep-ex-003-001'
     - 

Output:

.. code-block::

    {
        ...output excluded due to size...
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX003_INST_PUB=<InstanceId>

Launch a second Instance
------------------------
Use the following awscli command to launch an Instance and attach to the **'private'** Subnet.

``Reminder: The private Subnet is implicitly associated with the Default/Main Route Table, which does NOT have a Route to the Internet Gateway.``

.. code-block::

    aws ec2 run-instances --image-id $EX003_IMAGE_ID --instance-type t2.micro --key-name acpkey1 --subnet-id $EX003_SUBNET_PRIV --security-group-ids $EX003_SG --client-token awscertprep-ex-003-005

Output:

.. code-block::

    {
        ...output excluded due to size...
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX003_INST_PRIV=<InstanceId>

Private IP address
------------------
Use the following awscli command to collect the IP address of the Instance on the **'private'** Subnet.

``Note: you will type this address in a ssh session, so jot it down.``

.. code-block::
    
    aws ec2 describe-instances --instance-ids $EX003_INST_PRIV --output text --query Reservations[*].Instances[*].NetworkInterfaces[*].PrivateIpAddress

Output:

.. code-block::
    
    xxx.xxx.xxx.xxx

Allocate an Elastic IP
----------------------
Use the following awscli command to allocate a public IPv4 address

.. code-block::

    aws ec2 allocate-address --domain vpc

Output:

.. code-block::

    {
        "PublicIp": "xxx.xxx.xxx.xxx",
        "AllocationId": "eipalloc-xxxxxxxxxxxxxxxxx",
        "Domain": "vpc"
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX003_EIP=<AllocationId>
    export EX003_PUB_IP=<PublicIp>

Associate the Elastic IP
------------------------
Use the following awscli command to associate the Elastic IP with the Instance we launched in the public Subnet.

.. code-block::

    aws ec2 associate-address --allocation-id $EX003_EIP --instance-id $EX003_INST_PUB

Output:

.. code-block::

    {
        "AssociationId": "eipassoc-xxxxxxxxxxxxxxxxx"
    }

Test inbound connectivity
-------------------------
Use the following commands to test connectivity to the Instance in the public Subnet (via the Elastic IP).

``Expected results: 'ping' should fail and 'ssh' should be successful.``

.. code-block::

    ping $EX003_PUB_IP
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX003_PUB_IP

Test outbound connectivity
--------------------------
Use the following command to test connectivity from the Instance in the public Subnet.

``Expected results: 'apt update' should be successful.``

.. code-block::

    sudo apt update

    Type 'exit' to disconnect from the Instance.

Re-associate the Elastic IP
---------------------------
Use the following awscli command to re-associate the Elastic IP with the Instance we launched in the private Subnet.

.. code-block::

    aws ec2 associate-address --allocation-id $EX003_EIP --instance-id $EX003_INST_PRIV

Output:

.. code-block::

    {
        "AssociationId": "eipassoc-xxxxxxxxxxxxxxxxx"
    }

Test inbound connectivity
-------------------------
Use the following commands to test connectivity to the Instance in the private Subnet via the Elastic IP.

``Expected results: both 'ping' and 'ssh' should be fail.``

.. code-block::

    ping $EX003_PUB_IP
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX003_PUB_IP

Re-associate the Elastic IP
---------------------------
Use the following awscli command to re-associate the Elastic IP with the Instance we launched in the public Subnet.

.. code-block::

    aws ec2 associate-address --allocation-id $EX003_EIP --instance-id $EX003_INST_PUB

Output:

.. code-block::

    {
        "AssociationId": "eipassoc-xxxxxxxxxxxxxxxxx"
    }

Reconnect
-------
Use the following command to reconnect to the Instance in the public Subnet.


.. code-block::

    scp -i acpkey1.pem acpkey1.pem ubuntu@$EX003_PUB_IP:/home/ubuntu
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX003_PUB_IP

    Do NOT 'exit'

Test local connectivity
-----------------------
You should still be connected to the Instance in the public Subnet.

Use the following commands to test connectivity to the Instance in the private Subnet.

``Expected results: 'ping' should fail and 'ssh' should be successful.``

.. code-block::

    ping <ip-addr-private-instance>
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<ip-addr-private-instance>

You are now connected to the Instance on the private subnet.

Test outbound connectivity
--------------------------
Use the following command to test oubound connectivity from the Instance in the private Subnet.

``Expected results: 'apt update' should fail.``

.. code-block::

    sudo apt update

    Type 'cntrl-c' to kill 'apt'

    Type 'exit' twice to disconnect from both Instances.

The private subnet has no inbound or outbound path to the Internet. In a later exercise we will create a **NAT Gateway** to allow for outbound connectivity for priavte Subnets to the Internet.

Add a rule to the Security Group
--------------------------------
Use the following awscli command to create a new rule to the above security group.

.. code-block::

    aws ec2 authorize-security-group-ingress --group-id $EX003_SG --protocol icmp --port -1 --cidr 0.0.0.0/0

Test connectivity
-----------------
Use the following commands to test connectivity to the Instance in the public Subnet.

`Expected results: 'ping' and 'ssh' should now be successful.

.. code-block::

    ping $EX003_PUB_IP
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX003_PUB_IP

You are now connected to the Instance on the public subnet.

Test local connectivity
-----------------------
You should still be connected to the 'public' Instance.

Use the following command to test connectivity to the 'private' Instance. 

``Expected results: 'ping' should now be successful.``

.. code-block::

    ping <ip-addr-private-instance>

    Type 'exit' to disconnect from the public Instances.

Terminate Instances
-------------------
Use the following awscli command to terminate both instances.

Examine the current state. Both should show a **'currentState'** of **'shutting-down'**.

This operation is idempotent. Rerun the command until you see a **'currentState'** of **'terminated'**.

.. code-block::

    aws ec2  terminate-instances --instance-ids $EX003_INST_PUB $EX003_INST_PRIV

Output:

.. code-block::

    {
        "TerminatingInstances": [
            {
                "CurrentState": {
                    "Code": 32,
                    "Name": "shutting-down"
                },
                "InstanceId": "i-xxxxxxxxxxxxxxxxx",
                "PreviousState": {
                    "Code": 16,
                    "Name": "running"
                }
            },
            {
                "CurrentState": {
                    "Code": 32,
                    "Name": "shutting-down"
                },
                "InstanceId": "i-xxxxxxxxxxxxxxxxx",
                "PreviousState": {
                    "Code": 16,
                    "Name": "running"
                }
            }
        ]
    }

Release the Elastic IP
----------------------
Use the following awscli command to release the public IPv4 address

.. code-block::

    aws ec2 release-address --allocation-id $EX003_EIP

Delete the Security Group
-------------------------
Use the following awscli command to delete the Security Group.

.. code-block::

    aws ec2 delete-security-group --group-id $EX003_SG

Delete the VPC
--------------
Use the following awscli command to delete the VPC.

This will delete the VPC itself, plus the Subnets, Route Tables and Internet Gateway.

.. code-block::

    aws ec2 delete-vpc --vpc-id $EX003_VPC

Summary
-------
- We created a Key Pair.
- We created a Security Group.
- We added rules to the Security Group.
- We create two Instances.
- We allocated a Elastic IP.
- We map/re-mapped that Elastic IP to Instances.
- We tested connectivity to/from both the 'public' and 'private' Instances.

Next steps
----------
We will recreate the configuration built in ex-002 and ex-003, using CloudFormation, in 
`ex-004 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-004_GettingStartedCloudFormation.rst>`_

