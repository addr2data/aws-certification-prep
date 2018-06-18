ex-004: Testing basic connectivity
==================================

Status
------
Version 1.0 (6/18/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001, ex-003
   * - Prerequisite for exercise(s)
     - None

Objectives
----------

    - Become familiar with launching and connecting to on-demand Instances.
    - Test connectivity for the VPC configuration we created in ex-003.

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 1

   * - Component
     - Applicable Costs
     - Notes
   * - Key Pairs
     - None
     - 
   * - Security Groups
     - None
     -
   * - On-demand Instances
     - 
        + $0.0116 per hour per Instance (t2.micro)
     - 
        + During this exercise we will be launching two Instances, using ami-a4dc46db (Ubuntu Server 16.04 LTS), which is 'Free tier eligible'.
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

``NOTE: You can view all your EC2 limits and request increases by clicking on 'Limits' in the navigation pane of the EC2 console.``

.. list-table::
   :widths: 25, 25
   :header-rows: 1

   * - **Component**
     - **Limit**
   * - Key Pairs
     - 5000 per region
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

Create a Key Pair
-----------------
Use the following awscli command to create a new **Key Pair** and save the resulting **'.pem'** file.

**Note: I have only verified that directly redirecting the 'KeyMaterial' to a file produces a valid '.pem' on macOS. Other OSs may have subtle differences.**

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

.. code-block::

    aws ec2 create-security-group --group-name Int2Public --description "Security Group used to connect to instances on public subnet from Internet" --vpc-id $EX003_VPC

    {
        "GroupId": "sg-xxxxxxxxxxxxxxxxx"
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX004_SG=<GroupId>

Add a rule to the Security Group
--------------------------------
Use the following awscli command to add a rule to the above security group.

.. code-block::

    aws ec2 authorize-security-group-ingress --group-id $EX004_SG --protocol tcp --port 22 --cidr 0.0.0.0/0

Examine the Security Group
--------------------------
Use the following awscli command to examine the above security group.

.. code-block::

    aws ec2 describe-security-groups --group-ids $EX004_SG

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
Use the following awscli command to launch an Instance and attach to the **'public'** Subnet.

``Reminder: The only thing that makes it a 'public' Subnet is the fact that it is associated with a Route Table that has a Route to the Internet Gateway.``

We have used the **'--client-token'** to option ensure this operation is  Idempotent.

- `More information on Idempotency <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Run_Instance_Idempotency.html>`_

.. code-block::

    aws ec2 run-instances --image-id ami-a4dc46db --instance-type t2.micro --key-name acpkey1 --subnet-id $EX003_SUBNET_PUB --security-group-ids $EX004_SG --client-token awscertprep-ex-004-001

    {
        ...output excluded due to size...
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX004_INST_PUB=<InstanceId>

Launch a second Instance
------------------------
Use the following awscli command to launch an Instance and attach to the **'private'** Subnet.

``Reminder: The private Subnet is implicitly associated with the Default/Main Route Table, which does NOT have a Route to the Internet Gateway.``

.. code-block::

    aws ec2 run-instances --image-id ami-a4dc46db --instance-type t2.micro --key-name acpkey1 --subnet-id $EX003_SUBNET_PRIV --security-group-ids $EX004_SG --client-token awscertprep-ex-004-005

    {
        ...output excluded due to size...
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX004_INST_PRIV=<InstanceId>


Private IP address
------------------
Use the following awscli command to collect the IP address of the Instance on the **'private'** Subnet.

``Note: you will type this address in a ssh session, so jot it down.``

.. code-block::
    
    aws ec2 describe-instances --instance-ids $EX004_INST_PRIV --output text --query Reservations[*].Instances[*].NetworkInterfaces[*].PrivateIpAddress

Allocate an Elastic IP
----------------------
Use the following awscli command to allocate a public IPv4 address

.. code-block::

    aws ec2 allocate-address --domain vpc

    {
        "PublicIp": "xxx.xxx.xxx.xxx",
        "AllocationId": "eipalloc-xxxxxxxxxxxxxxxxx",
        "Domain": "vpc"
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX004_EIP=<AllocationId>
    export EX004_PUB_IP=<PublicIp>

Associate the Elastic IP
------------------------
Use the following awscli command to associate the Elastic IP with the Instance we launched in the public Subnet.

.. code-block::

    aws ec2 associate-address --allocation-id $EX004_EIP --instance-id $EX004_INST_PUB

    {
        "AssociationId": "eipassoc-xxxxxxxxxxxxxxxxx"
    }

Test inbound connectivity
-------------------------
Use the following commands to test connectivity to the Instance in the public Subnet (via the Elastic IP).

``Expected results: 'ping' should fail and 'ssh' should be successful.``

.. code-block::

    ping $EX004_PUB_IP
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX004_PUB_IP

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

    aws ec2 associate-address --allocation-id $EX004_EIP --instance-id $EX004_INST_PRIV

    {
        "AssociationId": "eipassoc-xxxxxxxxxxxxxxxxx"
    }

Test inbound connectivity
-------------------------
Use the following commands to test connectivity to the Instance in the private Subnet via the Elastic IP.

``Expected results: both 'ping' and 'ssh' should be fail.``

.. code-block::

    ping $EX004_PUB_IP
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX004_PUB_IP

Re-associate the Elastic IP
---------------------------
Use the following awscli command to re-associate the Elastic IP with the Instance we launched in the public Subnet.

.. code-block::

    aws ec2 associate-address --allocation-id $EX004_EIP --instance-id $EX004_INST_PUB

    {
        "AssociationId": "eipassoc-xxxxxxxxxxxxxxxxx"
    }

Reconnect
-------
Use the following command to reconnect to the Instance in the public Subnet.

``Expected results: 'ssh'** should be successful again.``

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX004_PUB_IP

    Do NOT 'exit'

Open a second terminal window and 'cd' to the aws-cert-prep directory. No need to 'activate' virtualenv.

Copy the Private Key
--------------------
From the second terminal window, use the following command to copy the **'acpkey1.pem'** file to the Instance on the public Subnet.

.. code-block::

    scp -i acpkey1.pem acpkey1.pem ubuntu@$EX004_PUB_IP:/home/ubuntu

Close the second terminal window

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

    aws ec2 authorize-security-group-ingress --group-id $EX004_SG --protocol icmp --port -1 --cidr 0.0.0.0/0

Test connectivity
-----------------
Use the following commands to test connectivity to the Instance in the public Subnet.

`Expected results: 'ping' and 'ssh' should now be successful.

.. code-block::

    ping $EX004_PUB_IP
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX004_PUB_IP

You are now connected to the Instance on the public subnet.

Test local connectivity
-----------------------
You should still be connected to the Instance in the public Subnet.

Use the following command to test connectivity to the Instance in the private Subnet via the private IP. 

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

    aws ec2  terminate-instances --instance-ids $EX004_INST_PUB $EX004_INST_PRIV

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

    aws ec2 release-address --allocation-id $EX004_EIP

Delete the Security Group
-------------------------
Use the following awscli command to delete the Security Group.

.. code-block::

    aws ec2 delete-security-group --group-id $EX004_SG

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
We will recreate the configuration built in ex-003 and ex-004, using CloudFormation, in 
`ex-005 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-005_GettingStartedCloudFormation.rst>`_

