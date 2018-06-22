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

    - Expand upon the basic VPC configuration created in **ex-002** to include the following VPC components:
      
      + NAT Gateway
      + Endpoint
    
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

Access Management
-----------------
We need to make the following changes in IAM

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

.. code-block::
    
    # Public address for Elastic IPs
    export EX005_IP_PUBLIC=<FloatingIpAddressInstance>
    export EX005_IP_NAT=<FloatingIpAddressNatGateway>
    
    # InstanceId for 'private' Instance
    export EX005_INST_PRIV=<PrivateInstance>
    
    #RouteTableId for 'private' Route Table
    export EX005_RTB_PRIV=<RouteTablePrivate>
    
    # SecurityGroupId for 'endpoint' Security Group
    export EX005_SG_ENDPOINT=<SecurityGroupEndpoint>
    
    # SubnetId for both Subnets
    export EX005_SUBNET_PUB=<SubnetPublic>
    export EX005_SUBNET_PRIV=<SubnetPrivate>
    
    # VpcId for VPC
    export EX005_VPC=<VPC>


Verify package installation
---------------------------
Run the following commands to verify that 'awscli' was installed on both Instances. 

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_PUBLIC

You are now connected to the 'public' instance.

.. code-block::

    aws --version

Output:

.. code-block::

    aws-cli/1.15.43 Python/3.5.2 Linux/4.4.0-1060-aws botocore/1.10.43

Type exit to exit the ssh session.

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_NAT

You are now connected to the 'public' instance.

.. code-block::

    aws --version

Output:

.. code-block::

    aws-cli/1.15.43 Python/3.5.2 Linux/4.4.0-1060-aws botocore/1.10.43

Type exit to exit the ssh session.


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

Collect the Elastic IP details
------------------------------
Use the following awscli command to show the **'AllocationId'** for both Elastic IP addresses.

.. code-block::
    
    aws ec2 describe-addresses --public-ips "$EX005_IP_PUBLIC" "$EX005_IP_NAT"

Output:

.. code-block::

    {
        "Addresses": [
            {
                "InstanceId": "i-0f7330c25b6d0f104",
                "PublicIp": "34.206.65.237",
                "AllocationId": "eipalloc-0b7d64f6df9f80f3f",
                "AssociationId": "eipassoc-0f0f10754fe61a7e8",
                "Domain": "vpc",
                "NetworkInterfaceId": "eni-01ef6e3f2adf74ca9",
                "NetworkInterfaceOwnerId": "926075045128",
                "PrivateIpAddress": "10.0.0.19"
            },
            {
                "InstanceId": "i-0aaeed60c8b12d28e",
                "PublicIp": "52.3.43.107",
                "AllocationId": "eipalloc-086c8e2ad16d6d0dc",
                "AssociationId": "eipassoc-024bf10e595476ff3",
                "Domain": "vpc",
                "NetworkInterfaceId": "eni-0fff02db0513e638f",
                "NetworkInterfaceOwnerId": "926075045128",
                "PrivateIpAddress": "10.0.1.17"
            }
        ]
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
Here we are going to break our rule about manually creating environment variables to prevent confusion.

.. code-block::

    export EX005_EIP_PUB_ALLOC=$(aws ec2 describe-addresses --public-ips $EX005_IP_PUBLIC --output text --query Addresses[*].AllocationId)

    export EX005_EIP_NAT_ALLOC=$(aws ec2 describe-addresses --public-ips $EX005_IP_NAT --output text --query Addresses[*].AllocationId)

    echo $EX005_EIP_PUB_ALLOC $EX005_EIP_NAT_ALLOC

Create NAT Gateway
------------------
Use the following awscli command to create the **'NAT Gateway'**.

``Notice the use of '--client-token', this makes the operation idempotent. Rerun this command until 'State' is 'available'.``

.. code-block::

    aws ec2 create-nat-gateway --allocation-id $EX005_EIP_NAT_ALLOC --subnet-id $EX005_SUBNET_PUB --client-token ex005_001

Output:

.. code-block::

    {
        "ClientToken": "ex005_001",
        "NatGateway": {
            "CreateTime": "2018-06-20T16:54:05.000Z",
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

Environment variable
~~~~~~~~~~~~~~~~~~~~

.. code-block::

    export EX005_NAT_GATEWAY=<NatGatewayId>

Parameter Store
---------------
Here we are going to use the **'Parameter Store'**, which is part of the **'AWS Systems Manager'** to store the 'private' IP of the 'private' Instance.
This will be useful, because the Parameter Store is available to use anywhere we have the 'awscli' and access to 'ssm'.

Use the following awscli command to collect and store the 'private' IP address of the 'private' Instance.

.. code-block::

    aws ssm put-parameter --name Ex005-PrivateIP --type String --value $(aws ec2 describe-instances --instance-ids $EX005_INST_PRIV --output text --query Reservations[*].Instances[*].NetworkInterfaces[*].PrivateIpAddress)

Output:

.. code-block::
    
    {
        "Version": 1
    }

Connect to public Instance
--------------------------
Use the following commands to:
    
    - Copy of the 'acpkey1.pem' to the 'public' Instance
    - Connect to the 'public' Instance

.. code-block::

    scp -i acpkey1.pem acpkey1.pem ubuntu@$EX005_IP_PUBLIC:/home/ubuntu
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@$EX005_IP_PUBLIC

    Do NOT exit.

Configure awscli
----------------
You are connected to the 'public' Instance.

.. code-block::
    aws ssm get-parameter --name Ex005-PrivateIP --region <YourRegion>

Output:

.. code-block::

    Unable to locate credentials. You can configure credentials by running "aws configure".

We won't configure credentials on the Instances, instead will will create a role in IAM and add that role to both Instances. 





You must specify a region. You can also configure your region by running "aws configure".



Connect to private Instance
---------------------------
You should still be connected to the 'public' Instance.

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

Even though we created a NAT Gateway, we also need created a default route that targets the NAT Gateway in the 'private' Route Table.


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
You should still be connected to the 'public' Instance.

Use the following command to reconnect to the 'private' Instance.

.. code-block::

    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<ip-addr-private-instance>

    Do NOT exit.

Test outbound connectivity
--------------------------
Use the following command to test outbound connectivity from the 'private' Instance.

``Expected results: 'apt update' should now succeed.``

.. code-block::

    sudo apt update

    Do NOT exit.


Install 'awscli'
----------------
Use the following command to test outbound connectivity from the 'private' Instance.

``Expected results: 'apt update' should now succeed.``

.. code-block::

    sudo apt install awscli

    Do NOT exit.


aws configure

AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]: us-east-1
Default output format [None]: json


aws ec2 describe-regions
Unable to locate credentials. You can configure credentials by running "aws configure".


    Type 'exit' twice to disconnect from both Instances.

sudo apt install python3-pip


aws ec2 associate-iam-instance-profile --instance-id $EX005_INST_PRIV --iam-instance-profile Name=EC2ForInstances

{
    "IamInstanceProfileAssociation": {
        "AssociationId": "iip-assoc-033488be77d6a4ef1",
        "InstanceId": "i-010507233a97824fc",
        "IamInstanceProfile": {
            "Arn": "arn:aws:iam::926075045128:instance-profile/EC2ForInstances",
            "Id": "AIPAIP7IETIKUVOSU3PJK"
        },
        "State": "associating"
    }
}


aws ec2 describe-iam-instance-profile-associations
{
    "IamInstanceProfileAssociations": [
        {
            "AssociationId": "iip-assoc-033488be77d6a4ef1",
            "InstanceId": "i-010507233a97824fc",
            "IamInstanceProfile": {
                "Arn": "arn:aws:iam::926075045128:instance-profile/EC2ForInstances",
                "Id": "AIPAIP7IETIKUVOSU3PJK"
            },
            "State": "associated"
        }
    ]
}


aws ec2 describe-regions
{
    "Regions": [
        {
            "RegionName": "ap-south-1",
            "Endpoint": "ec2.ap-south-1.amazonaws.com"
        },
        {
            "RegionName": "eu-west-3",
            "Endpoint": "ec2.eu-west-3.amazonaws.com"
        },
        {
            "RegionName": "eu-west-2",
            "Endpoint": "ec2.eu-west-2.amazonaws.com"
        },
        {
            "RegionName": "eu-west-1",
            "Endpoint": "ec2.eu-west-1.amazonaws.com"
        },
        {
            "RegionName": "ap-northeast-2",
            "Endpoint": "ec2.ap-northeast-2.amazonaws.com"
        },
        {
            "RegionName": "ap-northeast-1",
            "Endpoint": "ec2.ap-northeast-1.amazonaws.com"
        },
        {
            "RegionName": "sa-east-1",
            "Endpoint": "ec2.sa-east-1.amazonaws.com"
        },
        {
            "RegionName": "ca-central-1",
            "Endpoint": "ec2.ca-central-1.amazonaws.com"
        },
        {
            "RegionName": "ap-southeast-1",
            "Endpoint": "ec2.ap-southeast-1.amazonaws.com"
        },
        {
            "RegionName": "ap-southeast-2",
            "Endpoint": "ec2.ap-southeast-2.amazonaws.com"
        },
        {
            "RegionName": "eu-central-1",
            "Endpoint": "ec2.eu-central-1.amazonaws.com"
        },
        {
            "RegionName": "us-east-1",
            "Endpoint": "ec2.us-east-1.amazonaws.com"
        },
        {
            "RegionName": "us-east-2",
            "Endpoint": "ec2.us-east-2.amazonaws.com"
        },
        {
            "RegionName": "us-west-1",
            "Endpoint": "ec2.us-west-1.amazonaws.com"
        },
        {
            "RegionName": "us-west-2",
            "Endpoint": "ec2.us-west-2.amazonaws.com"
        }
    ]
}


aws ec2 delete-nat-gateway --nat-gateway-id $EX005_NAT_GATEWAY

{
    "NatGatewayId": "nat-0bd8ea5771f6626c3"
}


aws ec2 describe-nat-gateways

{
    "NatGateways": [
        {
            "CreateTime": "2018-06-20T16:54:05.000Z",
            "DeleteTime": "2018-06-20T19:00:40.000Z",
            "NatGatewayAddresses": [
                {
                    "AllocationId": "eipalloc-0e7a961dab989f4b8",
                    "NetworkInterfaceId": "eni-06204113",
                    "PrivateIp": "10.0.1.95",
                    "PublicIp": "18.233.207.198"
                }
            ],
            "NatGatewayId": "nat-0bd8ea5771f6626c3",
            "State": "deleted",
            "SubnetId": "subnet-0a63cccd8930927cf",
            "VpcId": "vpc-09ca97dcc166ba6c1"
        }
    ]
}

aws ec2 describe-route-tables --route-table-ids $EX005_RTB_PRIV --query RouteTables[*].Routes

[
    [
        {
            "DestinationCidrBlock": "10.0.0.0/16",
            "GatewayId": "local",
            "Origin": "CreateRouteTable",
            "State": "active"
        },
        {
            "DestinationCidrBlock": "0.0.0.0/0",
            "NatGatewayId": "nat-0bd8ea5771f6626c3",
            "Origin": "CreateRoute",
            "State": "blackhole"
        }
    ]
]



aws ec2 delete-route --destination-cidr-block 0.0.0.0/0 --route-table-id $EX005_RTB_PRIV


aws ec2 describe-route-tables --route-table-ids $EX005_RTB_PRIV --query RouteTables[*].Routes
[
    [
        {
            "DestinationCidrBlock": "10.0.0.0/16",
            "GatewayId": "local",
            "Origin": "CreateRouteTable",
            "State": "active"
        }
    ]
]


aws ec2 describe-regions

cntrl-z to kill


aws ec2 describe-vpc-endpoint-services --query ServiceNames

[
    "com.amazonaws.us-east-1.codebuild",
    "com.amazonaws.us-east-1.codebuild-fips",
    "com.amazonaws.us-east-1.dynamodb",
    "com.amazonaws.us-east-1.ec2",
    "com.amazonaws.us-east-1.ec2messages",
    "com.amazonaws.us-east-1.elasticloadbalancing",
    "com.amazonaws.us-east-1.execute-api",
    "com.amazonaws.us-east-1.kinesis-streams",
    "com.amazonaws.us-east-1.kms",
    "com.amazonaws.us-east-1.logs",
    "com.amazonaws.us-east-1.s3",
    "com.amazonaws.us-east-1.servicecatalog",
    "com.amazonaws.us-east-1.sns",
    "com.amazonaws.us-east-1.ssm"
]

aws ec2 describe-vpc-endpoint-services --service-names com.amazonaws.us-east-1.ec2

{
    "ServiceNames": [
        "com.amazonaws.us-east-1.ec2"
    ],
    "ServiceDetails": [
        {
            "ServiceName": "com.amazonaws.us-east-1.ec2",
            "ServiceType": [
                {
                    "ServiceType": "Interface"
                }
            ],
            "AvailabilityZones": [
                "us-east-1a",
                "us-east-1b",
                "us-east-1c",
                "us-east-1d",
                "us-east-1e",
                "us-east-1f"
            ],
            "Owner": "amazon",
            "BaseEndpointDnsNames": [
                "ec2.us-east-1.vpce.amazonaws.com"
            ],
            "PrivateDnsName": "ec2.us-east-1.amazonaws.com",
            "VpcEndpointPolicySupported": false,
            "AcceptanceRequired": false
        }
    ]
}





aws ec2 create-vpc-endpoint --vpc-endpoint-type Interface --vpc-id $EX005_VPC --service-name com.amazonaws.us-east-1.ec2 --subnet-ids $EX005_PRIV_SUBNET --no-private-dns-enabled --client-token ex005_002

{
    "VpcEndpoint": {
        "VpcEndpointId": "vpce-00c85c41acae918a4",
        "VpcEndpointType": "Interface",
        "VpcId": "vpc-09ca97dcc166ba6c1",
        "ServiceName": "com.amazonaws.us-east-1.ec2",
        "State": "pending",
        "PolicyDocument": "{\n  \"Statement\": [\n    {\n      \"Action\": \"*\", \n      \"Effect\": \"Allow\", \n      \"Principal\": \"*\", \n      \"Resource\": \"*\"\n    }\n  ]\n}",
        "RouteTableIds": [],
        "SubnetIds": [
            "subnet-05302080bc4e3c993"
        ],
        "Groups": [
            {
                "GroupId": "sg-097e6344b484220d2",
                "GroupName": "default"
            }
        ],
        "PrivateDnsEnabled": false,
        "NetworkInterfaceIds": [
            "eni-08c9cee27844d3a4b"
        ],
        "DnsEntries": [
            {
                "DnsName": "vpce-00c85c41acae918a4-p8mkeogq.ec2.us-east-1.vpce.amazonaws.com",
                "HostedZoneId": "Z7HUB22UULQXV"
            },
            {
                "DnsName": "vpce-00c85c41acae918a4-p8mkeogq-us-east-1f.ec2.us-east-1.vpce.amazonaws.com",
                "HostedZoneId": "Z7HUB22UULQXV"
            }
        ],
        "CreationTimestamp": "2018-06-20T19:36:06.547Z"
    }
} 




[--security-group-ids <value>]

[--private-dns-enabled | --no-private-dns-enabled]
[--cli-input-json <value>]
[--generate-cli-skeleton <value>]

export EX005_VPC_ENDPOINT=<VpcEndpointId>


aws ec2 delete-vpc-endpoints --vpc-endpoint-ids $EX005_VPC_ENDPOINT

{
    "Unsuccessful": []
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
To be added

