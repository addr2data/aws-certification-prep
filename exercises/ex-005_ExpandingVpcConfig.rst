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

    - Expand the basic VPC configuration created in **ex-002** to include the following VPC components:
      
      + NAT Gateway
      + VPC Endpoint
    
    - Introduce the **Parameter Store** from **AWS Systems Manager (ssm)**.
    - Introduce applying **IAM Roles** to Instances.
   

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable costs**
     - **Notes**
   * - VPC (including Subnets, Route Tables and IntenetGateways).
     - None
     - AWS does not charge for the basic VPC building blocks used in this exercise.
   * - On-demand Instances
     - 
        + $0.0116 per hour per Instance (t2.micro)
     - During this exercise we will be launching two Instances, using Ubuntu Server 16.04 LTS image, which is 'Free tier eligible'. It is not expected that these Instances will need to be running for more than one hour. 
   * - Elastic IPs
     - 
        + $0.00 per hour per EIP that is associated to a running Instance
        + $0.05 per hour per EIP that is NOT associated to a running Instance
     - Unlike ex-004, there will not be periods of time where an EIP is not associated with an running Instance.
   * - Elastic IPs
     - 
        + $0.00 per EIP address remap for the first 100 remaps per month.
        + $0.10 per EIP address remap for additional remaps over 100 per month
     - Unlike ex-004, we will not be re-mapping EIPs.
   * - NAT Gateway
     - Between $0.045 and $0.093 per hour, depending on Region.
     - During this exercise, we will creating a NAT Gateway. It should not need to run for more than hour or so.
   * - NAT Gateway
     - Between $0.045 and $0.093 per GB of data processed, depending on Region.
     - During this exercise, we will creating a NAT Gateway. A small amount of data will be processed.
   * - VPC Endpoint
     - Between $0.01 and $0.021 per hour, depending on Region.
     - During this exercise, we will creating a VPC Endpoint. It should not need to run for more than hour or so.
   * - VPC Endpoint
     - $0.01 per GB of data processed.
     - During this exercise, we will creating a NAT Gateway. A small amount of data will be processed.
   * - Data Transfer
     -
        + $0.00 per GB - Data Transfer IN to Amazon EC2 from Internet
        + $0.00 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(up to 1 GB)**
        + $0.09 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(next 9.999 TB)**
     - We also need to consider Data Transfer charges when using a NAT Gateway.

Limits
------
The following table shows the default limits for the components utilized in this exercise.

You can view all your EC2 limits and request increases by clicking on 'Limits' in the navigation pane of the EC2 console.

Environment variables
---------------------
During these exercises, we will be using the output of some commands to creatie environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Access Management
-----------------
We need to make the following changes in IAM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Add permissions for IAM to 'apiuser01' (up to this point we have only accessed IAM through the AWS Console).
- Add permissions for SSM to 'apiuser01'
- Create a new Role for use later in the exercise.  

Add permissions
~~~~~~~~~~~~~~~
- Login to your AWS account.
- Under services select **IAM**.
- In navigation pane, select **Users**.
- Click on **apiuser01**.
- Under **Add permissions to apiuser01**, select **Attach existing policies directly**.
- In the search box, type **IAMFullAccess**, then select **IAMFullAccess**.
- In the search box, type **AmazonSSMFullAccess**, then select **AmazonSSMFullAccess**.
- Click on **Next: Review**.
- Click **Add permissions**.

Create Role
~~~~~~~~~~~
- In navigation pane, select **Roles**.
- Click **Create role**.
- Under **Select type of trusted entity**, select **AWS service**.
- Under **Choose the service that will use this role**, select **EC2**.
- Click **Next: permissions**.
- In the search box, type **AmazonEC2FullAccess**, then select **AmazonEC2FullAccess**.
- In the search box, type **AmazonSSMFullAccess**, then select **AmazonSSMFullAccess**.
- Click on **Next: Review**.
- Under **Role name**, enter **ec2AccessForInstances**.
- Click **Create role**.

Verify access
-------------
Use the following awscli command to verify access **iam**.

.. code-block::

    aws iam get-user --user-name apiuser01

Output:

.. code-block::

    {
        "User": {
            "Path": "/",
            "UserName": "apiuser01",
            "UserId": "XXXXXXXXXXXXXXXXXXXXX",
            "Arn": "arn:aws:iam::xxxxxxxxxxx:user/apiuser01",
            "CreateDate": "2018-06-11T19:27:07Z"
        }
    }

Use the following awscli command to verify access **ssm**.

.. code-block::

    aws ssm describe-parameters

Output:

.. code-block::

    {
        "Parameters": []
    }


Template
--------
In order to build our starting configuration, we will use a CloudFormation Template. This template is based on the one that we used in **'ex-004'**, but with the following modifications:

Fixed
~~~~~
The following modifications will persist throughout the lab

- Added a new 'private' Route Table.
- Associated the 'private' Subnet with the 'private' Route Table.
- Added a new security group.
- Added a second Elastic IP.
- Added 'apt' and 'pip' commands to the 'public' and 'private' Instances. These will run at startup and install the necessary packages for the lab.

Temp
~~~~
The following modifications are there to allow Internet access for the 'private' Instance during deployment, so the startup commands can execute successfully.

- Added a default Route that targets the Internet Gateway to the 'private' Route Table.
- Associated with second Elastic IP with the 'private' Instance.

Only the new and modified resources are shown below:

.. code-block::

    ---
    Resources:
    RouteTablePrivate:
      Type: AWS::EC2::RouteTable
      Properties: 
        VpcId: !Ref VPC
        Tags:
          - Key: Name
            Value: rtb_pri_ex005

    DefaultRoutePrivate:
      Type: AWS::EC2::Route
      Properties: 
        DestinationCidrBlock: 0.0.0.0/0
        GatewayId: !Ref InternetGateway
        RouteTableId: !Ref RouteTablePrivate

    AssociateSubnetRouteTablePrivate:
      Type: AWS::EC2::SubnetRouteTableAssociation
      Properties: 
        RouteTableId: !Ref RouteTablePrivate
        SubnetId: !Ref SubnetPrivate

    SecurityGroupEndpoint:
      Type: AWS::EC2::SecurityGroup
      Properties: 
        GroupName: sg_endpoint_ex005
        GroupDescription: "Security Group for EC2 Endpoint in ex-005"
        SecurityGroupIngress:
          - 
            CidrIp: 0.0.0.0/0
            IpProtocol: tcp
            FromPort: 80
            ToPort: 80
          - 
            CidrIp: 0.0.0.0/0
            IpProtocol: tcp
            FromPort: 443
            ToPort: 443
        VpcId: !Ref VPC

    PublicInstance:
      Type: AWS::EC2::Instance
      Properties: 
        ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", 64]
        InstanceType: t2.micro
        KeyName: acpkey1
        SecurityGroupIds: 
          - !Ref SecurityGroupInstances
        SubnetId: !Ref SubnetPublic
        Tags: 
          - Key: Name
            Value: i_pub_ex005
        UserData:
          "Fn::Base64":
              "Fn::Join": [
                  "\n",
                  [
                      "#!/bin/bash",
                      "sudo apt-get update",
                      "sudo apt-get dist-upgrade -y",
                      "sudo apt-get install python3-pip -y",
                      "pip3 install awscli"
                  ]
              ]

    PrivateInstance:
      Type: AWS::EC2::Instance
      Properties: 
        ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", 64]
        InstanceType: t2.micro
        KeyName: acpkey1
        SecurityGroupIds: 
          - !Ref SecurityGroupInstances
        SubnetId: !Ref SubnetPrivate
        Tags: 
          - Key: Name
            Value: i_pri_ex005
        UserData:
          "Fn::Base64":
              "Fn::Join": [
                  "\n",
                  [
                      "#!/bin/bash",
                      "sudo apt-get update",
                      "sudo apt-get dist-upgrade -y",
                      "sudo apt-get install python3-pip -y",
                      "pip3 install awscli"
                  ]
              ]

    FloatingIpAddressNatGateway:
      Type: "AWS::EC2::EIP"
      Properties:
        InstanceId: !Ref PrivateInstance
        Domain: vpc

Create Stack
------------
Use the following awscli command to create a new **'Stack'** based on the template.

Note: If you are using the **'acpkey1'** Key Pair, you can leave off the **'--parameters'** option all together.

.. code-block::

    aws cloudformation create-stack \
      --stack-name ex-005 \
      --template-body file://./templates/ex-005_template.yaml \
      --parameters ParameterKey=KeyPairName,ParameterValue=acpkey1

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

Review the Stack details
------------------------
Use the following awscli command to display the **'LogicalResourceId'** and **'PhysicalResourceId'** for all the components in the **Stack**

Notice the format of this portion of the query string **'{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'**, it adds a header for each column.** 

.. code-block::

    aws cloudformation describe-stack-resources --stack-name ex-005 --output table --query 'StackResources[*].{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'

Output:

.. code-block::

    --------------------------------------------------------------------
    |                      DescribeStackResources                      |
    +-----------------------------------+------------------------------+
    |         LogicalResourceId         |     PhysicalResourceId       |
    +-----------------------------------+------------------------------+
    |  AssociateSubnetRouteTablePrivate |  rtbassoc-0106fa7c9f1abd965  |
    |  AssociateSubnetRouteTablePublic  |  rtbassoc-0b406bcb247f9d641  |
    |  AttachInternetGateway            |  ex-00-Attac-K9G3ZXRKN5ZE    |
    |  DefaultRoutePrivate              |  ex-00-Defau-B578935VCXYD    |
    |  DefaultRoutePublic               |  ex-00-Defau-1QAKJG0HP59MA   |
    |  FloatingIpAddressInstance        |  34.224.220.137              |
    |  FloatingIpAddressNatGateway      |  18.233.24.103               |
    |  InternetGateway                  |  igw-050e6dd37ff7cab4e       |
    |  PrivateInstance                  |  i-0270d65b5b52f1c63         |
    |  PublicInstance                   |  i-0920a6d31f2ea8428         |
    |  RouteTablePrivate                |  rtb-00a7da1fa9b8139a4       |
    |  RouteTablePublic                 |  rtb-083e35f3b5c55d410       |
    |  SecurityGroupEndpoint            |  sg-02379d0fa460257f3        |
    |  SecurityGroupInstances           |  sg-012618d749b795de4        |
    |  SubnetPrivate                    |  subnet-0e33e2be84bb50100    |
    |  SubnetPublic                     |  subnet-0043183c98708190c    |
    |  VPC                              |  vpc-001c2fbb0b53fe607       |
    +-----------------------------------+------------------------------+

Environment variables
~~~~~~~~~~~~~~~~~~~~~
Run the following commands to capture the 'PhysicalResourceId' for the applicable components.

.. code-block::

    export EX005_IP_PUBLIC=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`FloatingIpAddressInstance`].PhysicalResourceId')

    export EX005_IP_NAT=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`FloatingIpAddressNatGateway`].PhysicalResourceId')

    export EX005_INST_PRIV=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`PrivateInstance`].PhysicalResourceId')

    export EX005_INST_PUB=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`PublicInstance`].PhysicalResourceId')

    export EX005_RTB_PRIV=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`RouteTablePrivate`].PhysicalResourceId')

    export EX005_SG_ENDPOINT=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`SecurityGroupEndpoint`].PhysicalResourceId')

    export EX005_SUBNET_PUB=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`SubnetPublic`].PhysicalResourceId')

    export EX005_SUBNET_PRIV=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`SubnetPrivate`].PhysicalResourceId')

    export EX005_VPC=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`VPC`].PhysicalResourceId')

Sanity check
~~~~~~~~~~~~

.. code-block::
    
    echo $EX005_IP_PUBLIC
    echo $EX005_IP_NAT
    echo $EX005_INST_PRIV
    echo $EX005_INST_PRIV
    echo $EX005_RTB_PRIV
    echo $EX005_SG_ENDPOINT
    echo $EX005_SUBNET_PUB
    echo $EX005_SUBNET_PRIV
    echo $EX005_VPC

Verify package installation
---------------------------

Instance ('public')
~~~~~~~~~~~~~~~~~~~
Run the following command to connect the 'public' Instance. 

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_PUBLIC

Run the following command to verify that 'awscli' is installed (version should be 1.15.xx or greater).

.. code-block::

    aws --version

    Type 'exit' to exit the ssh session.

Instance ('private')
~~~~~~~~~~~~~~~~~~~
Run the following command to connect the 'private' Instance. 

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_NAT

Run the following command to verify that 'awscli' is installed (version should be 1.15.xx or greater).

.. code-block::

    aws --version

    Type 'exit' to exit the ssh session.

Disassociate Elastic IP
-----------------------
Now that you have verified that awscli is installed on both Instances, use the following awscli command to disassociate the Elastic IP from the 'private' Instance.

.. code-block::

    aws ec2 disassociate-address --public-ip $EX005_IP_NAT

Delete Route
------------
Now that you have verified that awscli is installed on both Instances, use the following awscli command to delete the default Route in the 'private' Route Table.

.. code-block::

    aws ec2 delete-route --destination-cidr-block 0.0.0.0/0 --route-table-id $EX005_RTB_PRIV

View the Elastic IP details
------------------------------
Use the following awscli command to show the **'AllocationId'** for both Elastic IP addresses.

.. code-block::
    
    aws ec2 describe-addresses --public-ips "$EX005_IP_PUBLIC" "$EX005_IP_NAT"

Output:

.. code-block::

    {
        "Addresses": [
            {
                "PublicIp": "xxx.xxx.xxx.xxx",
                "AllocationId": "eipalloc-xxxxxxxxxxxxxxxxx",
                "Domain": "vpc"
            },
            {
                "InstanceId": "i-xxxxxxxxxxxxxxxxx",
                "PublicIp": "xxx.xxx.xxx.xxx",
                "AllocationId": "eipalloc-xxxxxxxxxxxxxxxxx",
                "AssociationId": "eipassoc-xxxxxxxxxxxxxxxxx",
                "Domain": "vpc",
                "NetworkInterfaceId": "eni-xxxxxxxxxxxxxxxxx",
                "NetworkInterfaceOwnerId": "xxxxxxxxxxxx",
                "PrivateIpAddress": "xxx.xxx.xxx.xxx"
            }
        ]
    }

We can see that only one of the Elastic IPs is associated with an Instance.

Environment variable
~~~~~~~~~~~~~~~~~~~~
Run the following commands to capture the 'AllocationId' for Elastic IPs.

.. code-block::

    export EX005_EIP_PUB_ALLOC=$(aws ec2 describe-addresses --public-ips $EX005_IP_PUBLIC --output text --query Addresses[*].AllocationId)

    export EX005_EIP_NAT_ALLOC=$(aws ec2 describe-addresses --public-ips $EX005_IP_NAT --output text --query Addresses[*].AllocationId)

Sanity check
~~~~~~~~~~~~

.. code-block::

    echo $EX005_EIP_PUB_ALLOC $EX005_EIP_NAT_ALLOC

Create NAT Gateway
------------------
Use the following awscli command to create the **'NAT Gateway'**.

.. code-block::

    aws ec2 create-nat-gateway --allocation-id $EX005_EIP_NAT_ALLOC --subnet-id $EX005_SUBNET_PUB

Output:

.. code-block::

    {
        "NatGateway": {
            "CreateTime": "2018-06-22T14:32:42.000Z",
            "NatGatewayAddresses": [
                {
                    "AllocationId": "eipalloc-xxxxxxxxxxxxxxxxx"
                }
            ],
            "NatGatewayId": "nat-xxxxxxxxxxxxxxxxx",
            "State": "pending",
            "SubnetId": "subnet-xxxxxxxxxxxxxxxxx",
            "VpcId": "vpc-xxxxxxxxxxxxxxxxx"
        }
    }

Notice that the 'State' is **'pending'**.

Environment variable
~~~~~~~~~~~~~~~~~~~~
Manually create the following environment variable.

.. code-block::

    export EX005_NAT_GATEWAY=<NatGatewayId>


Check the status of the Nat Gateway
-----------------------------------
Use the following awscli command to check the status of the **'NAT Gateway'**.

Rerun this command until the 'State' is **'available'**.

.. code-block::

      aws ec2 describe-nat-gateways --nat-gateway-ids $EX005_NAT_GATEWAY

Output:

.. code-block::

    {
        "NatGateways": [
            {
                "CreateTime": "2018-06-22T14:32:42.000Z",
                "NatGatewayAddresses": [
                    {
                        "AllocationId": "eipalloc-xxxxxxxxxxxxxxxxx",
                        "NetworkInterfaceId": "eni-xxxxxxxx",
                        "PrivateIp": "xxx.xxx.xxx.xxx",
                        "PublicIp": "xxx.xxx.xxx.xxx"
                    }
                ],
                "NatGatewayId": "nat-xxxxxxxxxxxxxxxxx",
                "State": "available",
                "SubnetId": "subnet-xxxxxxxxxxxxxxxxx",
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx"
            }
        ]
    }

Add a Route
-----------
Even though we added a Nat Gateway, there is no Route that directs traffic to it.

Use the following awscli command to add a default Route to the 'private' Route Table.

.. code-block::

    aws ec2 create-route --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $EX005_NAT_GATEWAY --route-table-id $EX005_RTB_PRIV

Output:

.. code-block::
    
    {
        "Return": true
    }

Instance ('private')
--------------------
In an earlier step, we:

    + Disassociated an Elastic IP from the 'private' Instance
    + Removed the default Route, that targeted the **'Internet Gateway'**,  from the 'private' subnet.

In the above step, we added a new default Route, that targets the **'NAT Gateway'**, to the 'private' subnet.

The combination of the **'NAT Gateway'** and the new **'default Route'** will only allow Internet traffic that originates from the 'private' Subnet. 

At this point, the only way to connect to the 'private' Instance now is through the 'public' Instance. In order to do this we will need to collect the 'private' IP address of the 'private' Instance.

Parameter store
---------------
Since we will need access to the above value from the 'public' Instance, an environment variable in our local environment won't be of much use.

Instead, we are going to the **'Parameter store'**, which is part of the **'AWS Systems Manager'**, to store the value of the 'private' IP address of the 'private' instance.

Use the following awscli command to collect and store the 'private' IP address of the 'private' Instance.

.. code-block::

    aws ssm put-parameter --name Ex005-PrivInstancePrivIP --type String --value $(aws ec2 describe-instances --instance-ids $EX005_INST_PRIV --output text --query Reservations[*].Instances[*].NetworkInterfaces[*].PrivateIpAddress)

Output:

.. code-block::
    
    {
        "Version": 1
    }

Instance ('public')
-------------------
In order to access the **'Parameter store'** from the 'public' Instance, we will need to run an 'awscli' command. We verified that the 'awscli' was installed on both Instances in a previous step.

Before we can use the 'awscli' on the 'public' Instance, we must configure it. We are only going to configure the 'region' and NOT the credentials. We will use another method for that.

Key file
~~~~~~~~
First we need to copy the **Private Key** file to the 'public' Instance. Use the following command to do that.

.. code-block::

    scp -i acpkey1.pem acpkey1.pem ubuntu@$EX005_IP_PUBLIC:/home/ubuntu

Connect
~~~~~~~
Next we need to connect to the 'public' Instance. Run the following command to do that.

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_PUBLIC

Configure
~~~~~~~~~
Next we need to configure the 'awscli'. 

**We will only configure the 'region' and leave everything else blank.**

.. code-block::

    aws configure

Output:

.. code-block::

    AWS Access Key ID [None]:
    AWS Secret Access Key [None]:
    Default region name [None]: <YOUR_REGION>
    Default output format [None]:

Test
~~~~
Use the following awscli command to test our configuration.

.. code-block::

    aws ec2 describe-regions

Output:

.. code-block::

    Unable to locate credentials. You can configure credentials by running "aws configure".

Type 'exit' to exit the ssh session.


Add a Role
----------
Now we are going to add the 'Role' we created at the beginning of this exercise to both Instances.

Instance ('public')
~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws ec2 associate-iam-instance-profile --instance-id $EX005_INST_PUB --iam-instance-profile Name=Ec2AccessForInstances

Output:

.. code-block::

    {
        "IamInstanceProfileAssociation": {
            "AssociationId": "iip-assoc-xxxxxxxxxxxxxxxxx",
            "InstanceId": "i-xxxxxxxxxxxxxxxxx",
            "IamInstanceProfile": {
                "Arn": "arn:aws:iam::xxxxxxxxxxxx:instance-profile/Ec2AccessForInstances",
                "Id": "XXXXXXXXXXXXXXXXX"
            },
            "State": "associating"
        }
    }

Instance ('private')
~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws ec2 associate-iam-instance-profile --instance-id $EX005_INST_PRIV --iam-instance-profile Name=Ec2AccessForInstances

Output:

.. code-block::

    {
        "IamInstanceProfileAssociation": {
            "AssociationId": "iip-assoc-xxxxxxxxxxxxxxxxx",
            "InstanceId": "i-xxxxxxxxxxxxxxxxx",
            "IamInstanceProfile": {
                "Arn": "arn:aws:iam::xxxxxxxxxxxx:instance-profile/Ec2AccessForInstances",
                "Id": "XXXXXXXXXXXXXXXXX"
            },
            "State": "associating"
        }
    }

Sanity check
~~~~~~~~~~~~

.. code-block::

    aws ec2 describe-iam-instance-profile-associations

Output:

.. code-block::

    {
        "IamInstanceProfileAssociations": [
            {
                "AssociationId": "iip-assoc-xxxxxxxxxxxxxxxxx",
                "InstanceId": "i-xxxxxxxxxxxxxxxxx",
                "IamInstanceProfile": {
                    "Arn": "arn:aws:iam::xxxxxxxxxxxx:instance-profile/Ec2AccessForInstances",
                    "Id": "XXXXXXXXXXXXXXXXX"
                },
                "State": "associated"
            },
            {
                "AssociationId": "iip-assoc-xxxxxxxxxxxxxxxxx",
                "InstanceId": "i-xxxxxxxxxxxxxxxxx",
                "IamInstanceProfile": {
                    "Arn": "arn:aws:iam::xxxxxxxxxxxx:instance-profile/Ec2AccessForInstances",
                    "Id": "XXXXXXXXXXXXXXXXX"
                },
                "State": "associated"
            }
        ]
    }

Ensure that the 'State' is **'associated'**

Instance ('public')
-------------------

Connect
~~~~~~~
Next we need to connect to the 'public' Instance. Run the following command to do that.

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_PUBLIC

Test
~~~~
Use the following awscli command to check that we can now access the **'Parameter store'**.

.. code-block::

    aws ssm get-parameter --name Ex005-PrivInstancePrivIP

Output:

.. code-block::

    {
        "Parameter": {
            "Version": 1,
            "Name": "Ex005-PrivInstancePrivIP",
            "Value": "xxx.xxx.xxx.xxx",
            "Type": "String"
        }
    }

Do NOT exit ssh session.

Instance ('private')
-------------------

Connect
~~~~~~~

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$(aws ssm get-parameter --name Ex005-PrivInstancePrivIP --output text --query Parameter.Value)

Configure
~~~~~~~~~
Next we need to configure the 'awscli'. 

**We will only configure the 'region' and leave everything else blank.**

.. code-block::

    aws configure

Output:

.. code-block::

    AWS Access Key ID [None]:
    AWS Secret Access Key [None]:
    Default region name [None]: <YOUR_REGION>
    Default output format [None]:

Test
~~~~

.. code-block::

    aws ec2 describe-regions --region-names <YOUR_REGION>

Output:

.. code-block::

    {
        "Regions": [
            {
                "RegionName": "us-east-1",
                "Endpoint": "ec2.us-east-1.amazonaws.com"
            }
        ]
    }

When we run 'awscli ec2' commands, we are connecting to the public **'Endpoint'** for EC2, through the **'NAT Gateway'**.

Type 'exit' twice to exit both ssh sessions.

Create an Endpoint
------------------
Instead of accessing the public **'Endpoint'**, we can create our own VPC **'Endpoint'** that doesn't require our API calls to EC2 to leave the AWS network.

Use the following awscli command to create a VPC Endpoint. 

.. code-block::

    aws ec2 create-vpc-endpoint --vpc-endpoint-type Interface --vpc-id $EX005_VPC --service-name com.amazonaws.us-east-1.ec2 --subnet-ids $EX005_SUBNET_PRIV --no-private-dns-enabled --security-group-ids $EX005_SG_ENDPOINT

Output:

.. code-block::

    {
        "VpcEndpoint": {
            "VpcEndpointId": "vpce-08994fcde67df4657",
            "VpcEndpointType": "Interface",
            "VpcId": "vpc-0e023b84eab8c4fb0",
            "ServiceName": "com.amazonaws.us-east-1.ec2",
            "State": "pending",
            "PolicyDocument": "{\n  \"Statement\": [\n    {\n      \"Action\": \"*\", \n      \"Effect\": \"Allow\", \n      \"Principal\": \"*\", \n      \"Resource\": \"*\"\n    }\n  ]\n}",
            "RouteTableIds": [],
            "SubnetIds": [
                "subnet-0653d3fee3e302a9b"
            ],
            "Groups": [
                {
                    "GroupId": "sg-049958eab8dbc14c8",
                    "GroupName": "sg_endpoint_ex005"
                }
            ],
            "PrivateDnsEnabled": false,
            "NetworkInterfaceIds": [
                "eni-02a3fc8b69e6f2d72"
            ],
            "DnsEntries": [
                {
                    "DnsName": "vpce-08994fcde67df4657-1bqis1fj.ec2.us-east-1.vpce.amazonaws.com",
                    "HostedZoneId": "Z7HUB22UULQXV"
                },
                {
                    "DnsName": "vpce-08994fcde67df4657-1bqis1fj-us-east-1e.ec2.us-east-1.vpce.amazonaws.com",
                    "HostedZoneId": "Z7HUB22UULQXV"
                }
            ],
            "CreationTimestamp": "2018-06-22T17:05:19.778Z"
        }
    }

Notes
~~~~~
    
    We only created this Endpoint EC2
    We used the **'--no-private-dns-enabled'** option, so we will have to use the public 'DnsName' identified in the output above.

DNS Name
~~~~~~~~
Copy the DNS specified in the output above. 

Environment Variable
~~~~~~~~~~~~~~~~~~~~
export EX005_ENDPOINT=<VpcEndpointId>
export EX005_ENDPOINT=vpce-08994fcde67df4657

Delete a Route
--------------
Use the following awscli command to delete the default Route that targets in Nat Gateway in the 'private' Route Table. This will prevent us from getting to public Endpoint for EC2.

.. code-block::

    aws ec2 delete-route --destination-cidr-block 0.0.0.0/0 --route-table-id $EX005_RTB_PRIV

Instance ('public')
-------------------

Connect
~~~~~~~
Next we need to connect to the 'public' Instance. Run the following command to do that.

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_PUBLIC

Do NOT exit ssh session.

Instance ('private')
-------------------

Connect
~~~~~~~

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$(aws ssm get-parameter --name Ex005-PrivInstancePrivIP --output text --query Parameter.Value)

test
~~~~

.. code-block::

    aws ec2 describe-regions --region-names us-east-1

    Command will hang. 'cntrl-c' quit. 

.. code-block::

    aws ec2 describe-regions --region-names us-east-1 --endpoint-url https://<your-dns-name>

Output:

.. code-block::

    {
        "Regions": [
            {
                "RegionName": "us-east-1",
                "Endpoint": "ec2.us-east-1.amazonaws.com"
            }
        ]
    }

Cleanup
-------

NAT Gateway
~~~~~~~~~~~
Use the following awscli command to delete the **'NAT Gateway'**.

.. code-block::

    aws ec2 delete-nat-gateway --nat-gateway-id $EX005_NAT_GATEWAY

Output:

.. code-block::

    {
        "NatGatewayId": "nat-027ce1b40eea72b49"
    }

Use the following awscli command to verify that the **'NAT Gateway'** State is is **'deleted'**.

.. code-block::

    aws ec2 describe-nat-gateways --nat-gateway-ids $EX005_NAT_GATEWAY

Output:

.. code-block::

    {
        "NatGateways": [
            {
                "CreateTime": "2018-06-22T14:32:42.000Z",
                "DeleteTime": "2018-06-22T17:39:27.000Z",
                "NatGatewayAddresses": [
                    {
                        "AllocationId": "eipalloc-01e30ff85d3c3fb1d",
                        "NetworkInterfaceId": "eni-e52f27dc",
                        "PrivateIp": "10.0.1.144",
                        "PublicIp": "34.196.25.177"
                    }
                ],
                "NatGatewayId": "nat-027ce1b40eea72b49",
                "State": "deleted",
                "SubnetId": "subnet-0ae46bfc8cb541824",
                "VpcId": "vpc-0e023b84eab8c4fb0"
            }
        ]
    }

VPC Endpoint
~~~~~~~~~~~~
Use the following awscli command to delete the **'VPC Endpoint'**.

.. code-block::

    aws ec2 delete-vpc-endpoints --vpc-endpoint-ids $EX005_ENDPOINT

Output:

.. code-block::

    {
        "Unsuccessful": []
    }


Stack
~~~~~

.. code-block::

    aws cloudformation delete-stack --stack-name ex-005


.. code-block::

    aws cloudformation describe-stack --stack-name ex-005

Output:

.. code-block::

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:926075045128:stack/ex-005/523f72f0-7619-11e8-b431-50fae583d0fe",
                "StackName": "ex-005",
                "CreationTime": "2018-06-22T12:39:36.117Z",
                "DeletionTime": "2018-06-22T17:51:31.095Z",
                "RollbackConfiguration": {},
                "StackStatus": "DELETE_IN_PROGRESS",
                "DisableRollback": false,
                "NotificationARNs": [],
                "Tags": [],
                "EnableTerminationProtection": false
            }
        ]
    }

Output:

.. code-block::

    An error occurred (ValidationError) when calling the DescribeStacks operation: Stack with id ex-005 does not exist



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
In `ex-006 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-006_GettingStartedLoadBalancing.rst>`_, we will spin up a base configuration with CloudFormation, then add Load-balancing. 

