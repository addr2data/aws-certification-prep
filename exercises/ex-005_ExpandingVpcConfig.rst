ex-005: Expanding the VPC configuration
=======================================

Status
------
Version (Draft)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001, ex-003, ex-004
   * - Prerequisite for exercise(s)
     - tbd

Objectives
----------

    - Become familiar with additional VPC components by expanding the VPC configuration created in ex-002 (Basic VPC configuration).

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
   * - VPC (including Subnets, Route Tables and IntenetGateways).
     - None
     - AWS does not charge for the basic VPC building blocks used in this exercise.
   * - NAT Gateway
     - Between $0.045 and $ 0.093 per hour, depending on Region.
     - During this exercise, we will creating a NAT Gateway. It should not need to run for more than hour or so.
   * - NAT Gateway
     - Between $0.045 and $ 0.093 per GB of data processed, depending on Region.
     - During this exercise, we will creating a NAT Gateway. It should not need to run for more than hour or so.
   * - Data Transfer
     -
        + $0.00 per GB - Data Transfer IN to Amazon EC2 from Internet
        + $0.00 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(up to 1 GB)**
        + $0.09 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(next 9.999 TB)**
     - We also need to consider Data Transfer charges when using a NAT Gateway.

Limits
------
The following table shows the default limits for the components utilized in this exercise.

``NOTE: You can view all your EC2 limits and request increases by clicking on 'Limits' in the navigation pane of the EC2 console.``

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - NAT Gateway
     - A NAT gateway supports 5 Gbps of bandwidth and automatically scales up to 45 Gbps.
   * - Nat Gateway
     - Once you associated and Elastic IP with a NAT Gateway, you can not disassociate it. You must delete the NAT Gateway.
   * - Nat Gateway
     - A NAT gateway can support up to 55,000 simultaneous connections to each unique destination.

Environment variables
---------------------
During this exercise, we will be creating environment variables to simplify the syntax of commands run later in the exercise. I have decided to do this manually, because I want to show the the full output from each command and not redirect a filtered output directly into a variable.

Once you are comfortable with the expected output of a command and wish filter the output, then you might want to try the **'--query'** and **'--output'** options available in the awscli command.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Template
--------
In order to build the starting configuration, we will be using a CloudFormation Template that is based on the one we used in **'ex-004', but with the following modifications:

- Added an additional Elastic IP (unassociated).
- Create a new 'private' Route Table.
- Associated the 'private' Subnet with the 'private' Route Table.

Create Stack
------------
Use the following awscli command to create a new **'Stack'** based on the template.

.. code-block::

    aws cloudformation create-stack --stack-name ex-005 --template-body file://./templates/ex-005_template.yaml

Output:

.. code-block::

    {
        "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-005/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }

Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this command until **'StackStatus'** is **'CREATE_COMPLETE'**.

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-005

Output:

.. code-block::

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-005/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "StackName": "ex-005",
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


Collect the Stack details
-------------------------
Use the following awscli command to collect the **'LogicalResourceId'** and **'PhysicalResourceId'** for all the components in the **Stack**

``Notice the format of this portion of the query string '{LogicalResourceId: LogicalResourceId,PhysicalResourceId: PhysicalResourceId}', it adds a header for each column.`` 

.. code-block::

    aws cloudformation describe-stack-resources --stack-name ex-005 --output table --query 'StackResources[*].{LogicalResourceId: LogicalResourceId,PhysicalResourceId: PhysicalResourceId}'

Output:

.. code-block::

    --------------------------------------------------------------------
    |                      DescribeStackResources                      |
    +-----------------------------------+------------------------------+
    |         LogicalResourceId         |     PhysicalResourceId       |
    +-----------------------------------+------------------------------+
    |  AssociateSubnetRouteTablePrivate |  rtbassoc-0d241d3c9bb2dc49f  |
    |  AssociateSubnetRouteTablePublic  |  rtbassoc-06aff24c36acac6e0  |
    |  AttachInternetGateway            |  ex-00-Attac-1VF12BB0ZDLSF   |
    |  DefaultRoutePublic               |  ex-00-Defau-1N09WMGQ4J1ZB   |
    |  FloatingIpAddressInstance        |  18.205.251.20               |
    |  FloatingIpAddressNatGateway      |  18.233.207.198              |
    |  InternetGateway                  |  igw-0464cdfdfe38e889a       |
    |  PrivateInstance                  |  i-010507233a97824fc         |
    |  PublicInstance                   |  i-0b989e42e6e390ad3         |
    |  RouteTablePrivate                |  rtb-06d4437e94da8d880       |
    |  RouteTablePublic                 |  rtb-0299307de3927c7ba       |
    |  SecurityGroup                    |  sg-067dab68bcdd1330b        |
    |  SubnetPrivate                    |  subnet-05302080bc4e3c993    |
    |  SubnetPublic                     |  subnet-0a63cccd8930927cf    |
    |  VPC                              |  vpc-09ca97dcc166ba6c1       |
    +-----------------------------------+------------------------------+

Environment variables
~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    export EX005_PUB_SUBNET=<SubnetPublic>
    export EX005_VPC=<VPC>
    export EX005_RTB_PRIV=<RouteTablePrivate>
    export EX005_IP_PUBLIC=<FloatingIpAddressInstance>
    export EX005_INST_PRIV=<PrivateInstance>

Also, collect the **'AllocationId'** for the **'FloatingIpAddressNatGateway'**.

.. code-block::
    
    aws ec2 describe-addresses --public-ips <FloatingIpAddressNatGateway>

Output:

.. code-block::

    {
        "Addresses": [
            {
                "PublicIp": "xxx.xxx.xxx.xxx",
                "AllocationId": "eipalloc-xxxxxxxxxxxxxxxxx",
                "Domain": "vpc"
            }
        ]
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~

.. code-block::

    export EX005_EIP_ALLOC=<AllocationId>

Create NAT Gateway
------------------
Use the following awscli command to create the **'NAT Gateway'**.

``Notice the use of '--client-token', this makes the operation idempotent. Rerun this command until 'State' is 'available'.``

.. code-block::

    aws ec2 create-nat-gateway --allocation-id $EX005_EIP_ALLOC --subnet-id $EX005_PUB_SUBNET --client-token ex005_001

Output:

.. code-block::

    {
        "ClientToken": "ex005_001",
        "NatGateway": {
            "CreateTime": "2018-06-20T16:54:05.000Z",
            "NatGatewayAddresses": [
                {
                    "AllocationId": "eipalloc-0e7a961dab989f4b8"
                }
            ],
            "NatGatewayId": "nat-0bd8ea5771f6626c3",
            "State": "pending",
            "SubnetId": "subnet-0a63cccd8930927cf",
            "VpcId": "vpc-09ca97dcc166ba6c1"
        }
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~

.. code-block::

    export EX005_NAT_GATEWAY=<NatGatewayId>

Private IP address
------------------
Use the following awscli command to collect the IP address of the 'private' Instance.

``Note: you will type this address in a ssh session, so jot it down.``

.. code-block::
    
    aws ec2 describe-instances --instance-ids $EX005_INST_PRIV --output text --query Reservations[*].Instances[*].NetworkInterfaces[*].PrivateIpAddress

Output:

.. code-block::
    xxx.xxx.xxx.xxx

Connect to public Instance
--------------------------
Use the following commands to:
    
    - Copy of the 'acpkey1.pem' to the 'public' Instance
    - Connect to the 'public' Instance

.. code-block::

    scp -i acpkey1.pem acpkey1.pem ubuntu@$EX005_IP_PUBLIC:/home/ubuntu
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_PUBLIC

    Do NOT exit.

Connect to private Instance
---------------------------
You should still be connected to the Instance in the public Subnet.

Use the following command to connect to the 'private' Instance.

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<ip-addr-private-instance>

    Do NOT exit.

Test outbound connectivity
--------------------------
Use the following command to test outbound connectivity from the 'private' Instance.

``Expected results: 'apt update' should fail.``

.. code-block::

    sudo apt update

    Type 'cntrl-c' to kill 'apt'

    Type 'exit' twice to disconnect from both Instances.

Even though we created a NAT Gateway, we have created a Route to it in the 'private' Route Table.


Add a Route
-----------
Use the following awscli command to add a Route to the 'private' Route Table.

.. code-block::

    aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $EX005_NAT_GATEWAY --route-table-id $EX005_RTB_PRIV

    {
        "Return": true
    }

Connect to public Instance
--------------------------
Use the following command to reconnect to the 'public' Instance

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_PUBLIC

    Do NOT exit.

Connect to private Instance
---------------------------
You should still be connected to the Instance in the public Subnet.

Use the following command to connect to the 'private' Instance.

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<ip-addr-private-instance>

    Do NOT exit.

Test outbound connectivity
--------------------------
Use the following command to test outbound connectivity from the 'private' Instance.

``Expected results: 'apt update' should now succeed.``

.. code-block::

    sudo apt update

    Type 'exit' twice to disconnect from both Instances.








Summary
-------
- We created a VPC.
- We created a second Route Table and Tagged it 'public'
- We created an Internet Gateway.
- We attached the Internet Gateway to the VPC.
- We created a Default Route that targeted the Internet Gateway in the 'public' Route Table.
- We created two Subnets and Tagged them 'public' and 'private', respectively.
- We associated the 'public' Subnet with the 'public' Route Table.

Next steps
----------
We will test that our VPC configuration actually works as expected in 
`ex-004 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-004_TestingBasicConnectivity.rst>`_




Dave's Stuff
------------

.. code-block::

    export EX005_PUB_SUBNET=subnet-0a63cccd8930927cf
    export EX005_EIP_ALLOC=eipalloc-0e7a961dab989f4b8
    export EX005_VPC=vpc-09ca97dcc166ba6c1
    export EX005_RTB_PRIV=rtb-06d4437e94da8d880
    export EX005_IP_PUBLIC=18.205.251.20
    export EX005_NAT_GATEWAY=nat-0bd8ea5771f6626c3
    export EX005_INST_PRIV=i-010507233a97824fc

    10.0.3.212
