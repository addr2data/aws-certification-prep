ex-004: Testing basic connectivity
==================================

Status
------
Draft (once the draft has been completed, a version number and date will be provided)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise
     - ex-004
   * - Prerequisite for exercise
     - None


Introduction
------------
The primary purpose of this exercise is to become familiar with launching on-demand instances, connecting to those instances and testing connectivity for the VPC configuration performed in ex-003. 


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
     - 
        + $0.00
     - 
   * - Security Groups
     - 
        + $0.00
     -
   * - On-demand Instances
     - 
        + $0.0116 per hour per Instance (t2.micro)
     - During this exercise we will be launching two Instance, using ami-a4dc46db (Ubuntu Server 16.04 LTS), which is 'Free tier eligible'. It is not expected that these Instances will need to be running for more than one hour. 
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




Create a Key Pair
-----------------
Use the following awscli command to create a new **Key Pair** and save the resulting **'.pem'** file.

``LIMITS: You can have up to 5000 Key Pairs per region.``

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

You can create up to 500 security groups per VPC

.. code-block::

    aws ec2 create-security-group --group-name Int2Public --description "Security Group used to connect to instances on public subnet from Internet" --vpc-id vpc-0ecc9b41c9206502b

    {
        "GroupId": "sg-01f180a16b3948693"
    }

Add a rule to the Security Group
--------------------------------
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

*Reminder: The only thing that makes it a public Subnet is that it is associated with a Route Table that has a Route to the Internet Gateway.

We have used the option **'--client-token'** to ensure this operation is  Idempotent.

- `More information on Idempotency <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Run_Instance_Idempotency.html>`_

.. code-block::

    aws ec2 run-instances --image-id ami-a4dc46db --instance-type t2.micro --key-name acpkey1 --subnet-id subnet-00ab76a6ccaaee13d --security-group-ids sg-01f180a16b3948693 --client-token awscertprep-ex-004-004

Launch a second Instance
------------------------
Use the following awscli command to launch an Instance in the 'private' Subnet.

*Reminder: The private Subnet is implicitly associated with the Default/Main Route Table, which does NOT have a Route to the Internet Gateway.

.. code-block::

    aws ec2 run-instances --image-id ami-a4dc46db --instance-type t2.micro --key-name acpkey1 --subnet-id subnet-037dd3a0e579a8da7 --security-group-ids sg-01f180a16b3948693 --client-token awscertprep-ex-004-005

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
Use the following awscli command to associate the Elastic IP with the Instance we launched in the public Subnet.

.. code-block::

    aws ec2 associate-address --allocation-id eipalloc-090dfc687075050e2 --instance-id i-0c19982239ebb148d

    {
        "AssociationId": "eipassoc-097543d512f520d2d"
    }

Test inbound connectivity
-------------------------
Use the following commands to test connectivity to the Instance in the public Subnet (via the Elastic IP).

**'ping'** should fail and **'ssh'** should be successful.

.. code-block::
    ping 54.89.230.154
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@54.89.230.154

Test outbound connectivity
--------------------------
Use the following command to test connectivity from the Instance in the public Subnet.

**'apt update'** should be successful.

.. code-block::
    sudo apt update

    Type 'exit' to disconnect from the Instance.

Re-associate the Elastic IP
---------------------------
Use the following awscli command to re-associate the Elastic IP with the Instance we launched in the private Subnet.

.. code-block::

    aws ec2 associate-address --allocation-id eipalloc-090dfc687075050e2 --instance-id i-0e93ed17d9c9819f7

    {
        "AssociationId": "eipassoc-0c11541cbd138171d"
    }

Test inbound connectivity
-------------------------
Use the following commands to test connectivity to the Instance in the private Subnet via the Elastic IP.

Both **'ping'** and **'ssh'** should be fail.

.. code-block::
    ping 54.89.230.154
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@54.89.230.154

Re-associate the Elastic IP
---------------------------
Use the following awscli command to re-associate the Elastic IP with the Instance we launched in the public Subnet.

.. code-block::

    aws ec2 associate-address --allocation-id eipalloc-090dfc687075050e2 --instance-id i-0c19982239ebb148d

    {
        "AssociationId": "eipassoc-0675e7c77e1dfc852"
    }

Try to connect
--------------
Use the following command to reconnect to the Instance in the public Subnet.

**'ssh'** should be successful.

.. code-block::
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@54.89.230.154

    Do NOT 'exit'

Open a second terminal window and 'cd' to the aws-cert-prep directory. No need to 'activate' virtualenv.

Copy the Private Key
--------------------
From the second terminal window, use the following command to copy the **'acpkey1.pem'** file to the Instance on the public Subnet.

.. code-block::
    scp -i acpkey1.pem acpkey1.pem ubuntu@54.89.230.154:/home/ubuntu

Close the second terminal window

Test local connectivity
-----------------------
Use the following commands to test connectivity to the Instance in the private Subnet via the private IP. You should still be connected to the Instance in the public Subnet.

**'ping'** should fail and **'ssh'** should now be successful.

.. code-block::
    ping 10.0.2.103
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@10.0.2.103

You are now connected to the Instance on the private subnet.

Test outbound connectivity
--------------------------
Use the following command to test oubound connectivity from the Instance in the private Subnet.

**'apt update'** should be fail.

.. code-block::
    sudo apt update

    Type 'cntrl-c' to kill 'apt'

    Type 'exit' twice to disconnect from both Instances.

The private subnet has no inbound or outbound path to the Internet. In a later exercise we will create a **NAT Gateway** to allow for outbound connectivity to the Internet.

Add a rule to the Security Group
--------------------------------
From the second terminal window (not connected to the Instance), use the following awscli command to create a new rule to the above security group.

.. code-block::

    aws ec2 authorize-security-group-ingress --group-id sg-01f180a16b3948693 --protocol icmp --port -1 --cidr 0.0.0.0/0

Test connectivity
-----------------
Use the following command to test ICMP connectivity to the Instance in the public Subnet via the private IP.

You should still be connected to the Instance in the public Subnet.

**'ping'** should fail and **'ssh'** should now be successful.

.. code-block::
    ping 54.89.230.154

Terminate Instances
-------------------
Use the following awscli commands to terminate both instances.

Examine the current state. Both should show a **'currentState'** of **'shutting-down'**.

This operation is idempotent. Rerun the command until you see a **'currentState'** of **'terminated'**.

.. code-block::

    aws ec2  terminate-instances --instance-ids i-0c19982239ebb148d i-0e93ed17d9c9819f7

    {
        "TerminatingInstances": [
            {
                "CurrentState": {
                    "Code": 32,
                    "Name": "shutting-down"
                },
                "InstanceId": "i-0c19982239ebb148d",
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
                "InstanceId": "i-0e93ed17d9c9819f7",
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

    aws ec2 release-address --allocation-id eipalloc-090dfc687075050e2

Delete the Security Group
-------------------------
Use the following awscli command to delete the Security Group.

.. code-block::

    aws ec2 delete-security-group --group-id sg-01f180a16b3948693





