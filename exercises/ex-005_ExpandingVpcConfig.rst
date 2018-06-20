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
   :header-rows: 1

   * - Component
     - Applicable Costs
     - Notes
   * - VPC (including Subnets, Route Tables and IntenetGateways).
     - None
     - AWS does not charge for the basic VPC building blocks used in this exercise.
   * - NAT Gateway
     - Between $0.045 and $ 0.093 per hour, depending on Region.
     - During this exercise, we will creating a NAT Gateway. It should not need to run for more than hour or so.
   * - NAT Gateway
     - Between $0.045 and $ 0.093 per GB of data processed, depending on Region.
     - During this exercise, we will creating a NAT Gateway. It should not need to run for more than hour or so.

Limits
------
The following table shows the default limits for the components utilized in this exercise.

``NOTE: You can view all your EC2 limits and request increases by clicking on 'Limits' in the navigation pane of the EC2 console.``

.. list-table::
   :widths: 25, 25
   :header-rows: 1

   * - **Component**
     - **Limit**
   * - VPC
     - 5 per region
   * - Route Tables
     - 200 per VPC
   * - Entries per Route Table
     - 50
   * - Subnets
     - 200 per VPC

Environment variables
---------------------
During this exercise, we will be creating environment variables to simplify the syntax of commands run later in the exercise. I have decided to do this manually, because I want to show the the full output from each command and not redirect a filtered output directly into a variable.

Once you are comfortable with the expected output of a command and wish filter the output, then you might want to try the **'--query'** and **'--output'** options available in the awscli command.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Create Stack
------------
Use the following awscli command to create a new **'Stack'** based on the template.

.. code-block::

    aws cloudformation create-stack --stack-name ex-005 --template-body file://./templates/ex-005_template.yaml

    {
        "StackId": "arn:aws:cloudformation:us-east-1:926075045128:stack/ex-005/def0a050-73fa-11e8-a0ab-500c286e44d1"
    }

Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this command until **'StackStatus'** is **'CREATE_COMPLETE'**.

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-005

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:926075045128:stack/ex-005/def0a050-73fa-11e8-a0ab-500c286e44d1",
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


aadddd
------
Use the following awscli command to collect check the **'PhysicalResourceIds'** for the **Stack**

.. code-block::

    aws cloudformation describe-stack-resources --stack-name ex-005 --output table --query 'StackResources[*].[LogicalResourceId, PhysicalResourceId]'

    -------------------------------------------------------------
    |                  DescribeStackResources                   |
    +----------------------------+------------------------------+
    |  AssociateSubnetRouteTable |  rtbassoc-0842e4eb1e9d1edb0  |
    |  AttachInternetGateway     |  ex-00-Attac-10R4E8BTLQ479   |
    |  DefaultRoute              |  ex-00-Defau-Y1F3ACELJ5C3    |
    |  FloatingIpAddress         |  35.169.144.76               |
    |  InternetGateway           |  igw-0786fa8e8b02cea0e       |
    |  PrivateInstance           |  i-04d0be81131ccec17         |
    |  PublicInstance            |  i-039d3e6cfae506c77         |
    |  RouteTable                |  rtb-066460c2ca5b8f0f7       |
    |  SecurityGroup             |  sg-0011153ed095f008f        |
    |  SubnetPrivate             |  subnet-05652264047aabc87    |
    |  SubnetPublic              |  subnet-03ff850c3d2da5855    |
    |  VPC                       |  vpc-0fc4ba21b51dd7c94       |
    +----------------------------+------------------------------+

.. code-block::
    
    aws ec2 describe-addresses --public-ips <FloatingIpAddress>

    {
        "Addresses": [
            {
                "PublicIp": "35.169.144.76",
                "AllocationId": "eipalloc-09617e997c4f04173",
                "Domain": "vpc"
            }
        ]
    }


.. code-block::

    aws cloudformation describe-stack-resource --stack-name ex-005 --logical-resource-id FloatingIpAddress


Environment variables
~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    export EX006_PUB_SUBNET=<SubnetPublic>
    export EX006_EIP=<AllocationId>
    export EX006_VPC=<VPC>

    export EX006_PUB_SUBNET=subnet-03ff850c3d2da5855
    export EX006_EIP=eipalloc-09617e997c4f04173
    export EX006_VPC=vpc-0fc4ba21b51dd7c94 


Create NAT Gateway
------------------
Use the following awscli command to collect check the **'PhysicalResourceIds'* for the **Stack**

Rerun comman until 'State' is 'available'.

.. code-block::

    aws ec2 create-nat-gateway --allocation-id $EX006_EIP --subnet-id $EX006_PUB_SUBNET --client-token addr2data

    {
    "ClientToken": "addr2data",
    "NatGateway": {
        "CreateTime": "2018-06-19T20:38:06.000Z",
        "NatGatewayAddresses": [
            {
                "AllocationId": "eipalloc-09617e997c4f04173",
                "NetworkInterfaceId": "eni-f1b3a561",
                "PrivateIp": "10.0.1.79"
            }
        ],
        "NatGatewayId": "nat-03393ba7a629738ca",
        "State": "pending",
        "SubnetId": "subnet-03ff850c3d2da5855",
        "VpcId": "vpc-0fc4ba21b51dd7c94"
    }
}

.. code-block::

    aws ec2 describe-route-tables --filters Name=vpc-id,Values=$EX006_VPC --output table --query 'RouteTables[*].Associations[*].{Main: Main,RouteTableId: RouteTableId}'

    ------------------------------------
    |        DescribeRouteTables       |
    +--------+-------------------------+
    |  Main  |      RouteTableId       |
    +--------+-------------------------+
    |  True  |  rtb-028f77b7ef9209f43  |
    |  False |  rtb-066460c2ca5b8f0f7  |
    +--------+-------------------------+


Environment variables
~~~~~~~~~~~~~~~~~~~~~
.. code-block::

    export EX005_RTB_MAIN=rtb-028f77b7ef9209f43
    export EX005_NAT=nat-03393ba7a629738ca

Add a Route
-----------
Use the following awscli command to add a Route to the 'main' Route Table.

.. code-block::

    aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $EX006_NAT --route-table-id $EX006_RTB_MAIN

    {
        "Return": true
    }

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
