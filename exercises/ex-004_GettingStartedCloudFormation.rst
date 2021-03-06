ex-004: Getting Started with CloudFormation
===========================================

Status
------
Version 1.1 (7/14/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001
   * - Prerequisite for exercise(s)
     - tbd

Objectives
----------
- Learn how CloudFormation Templates are constructed using YAML.
- Create a Stack in CloudFormation from a Template that mimics the configuration from ex-002 and ex-003.

**Note: Going forward, CloudFormation will allow us to quickly spin up a 'starting configuration' at the beginning of an exercise and delete it at the end. This will allow us to minimize costs without having to rebuild configurations by hand.**

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
   * - CloudFormation
     - 
     	+ None
     - 
     	+ There is no charge for CloudFormation itself, only for the resources that you deploy with it.
   * - VPC (including Subnets, Route Tables and Internet Gateways)
     - 
     	+ None
     - 
   * - Security Groups
     - 
     	+ None
     -
   * - On-demand Instances
     - 
        + $0.0116 per hour per Instance (t2.micro)
     - 
     	+ During this exercise, we will use two (2) Instances. The AMI that will be used is **'Ubuntu Server 16.04 LTS'**, which combined with the **'t2.micro'** Instance Type, is **'Free tier eligible'**.
        + It is not expected that these Instances will need to be running for more than one hour.
   * - Elastic IPs
     - 
        + $0.00 per hour per EIP that is associated to a running Instance
        + $0.005 per hour per EIP that is NOT associated to a running Instance
     - 

Limits
------
The following table shows the CloudFormation template limits that are relevant to this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - Resources per Template
     - 200
   * - Max length of Resource name 
     - 255 characters

Environment variables
---------------------
During these exercises, we will be using the output of some commands to creatie environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Diagram
-------
In this exercise, we will recreate the configuration from **ex-002** and **ex-003** using CloudFormation.

.. image:: https://github.com/addr2data/aws-certification-prep/blob/master/images/ex-004.png

Add CloudFormation API access to user 'apiuser01' 
-------------------------------------------------

Currently, the **apiuser01** user only has permissions for **ec2**. We need to add access to CloudFormation. This is a two-step process. First, we'll create a **Policy** that contains the necessary permissions, then we'll attach that policy to the **apiuser01** user.

- Login to your AWS account.
- Under services select **IAM**.

Create a policy
~~~~~~~~~~~~~~~

- Select **Policies**.
- Click **Create policy**.
- Under **Service**, click on the **Choose a service** link.
- In the search box, type **CloudFormation**, the select **CloudFormation**.
- Under **Manual actions**, check the box for **All CloudFormation actions**.
- Click on the **Resources** section to expand it.
- Select **All resources**.
- Click on **Review policy**.
- In the name box, type **CloudFormationFullAccess**.
- Click **Create policy**.

Add permissions to 'apiuser01'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Select **Users**
- Click on **apiuser01**
- Under **Add permissions to apiuser01**, select **Attach existing policies directly**.
- In the search box, type **CloudFormationFullAccess**, then select **CloudFormationFullAccess**.
- Click on **Next: Review**.
- Click **Add permissions**.

Verify access
-------------
Use the following awscli command to verify access to CloudFormation API.

.. code-block::

	aws cloudformation describe-stacks

Output:

.. code-block::

	{
		"Stacks": []
	}

View account limits
-------------------
Use the following awscli command to view your account limits for CloudFormation.

For more information on CloudFormation account limits:
`CloudFormation limits <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html>`_

.. code-block::

	aws cloudformation describe-account-limits

Output:

.. code-block::
	
	{
		"AccountLimits": [
			{
            	"Name": "StackLimit",
            	"Value": 200
        	},
        	{
            	"Name": "StackOutputsLimit",
            	"Value": 60
        	}
		]
	}

Review the template
-------------------
Below is the contents of the **ex-004_template.yaml** file from the **templates** directory.

Notice how the **Parameters:** blocks, allow us create a parameter called **KeyPairName**, which has a default value of **acpkey1**. This will allow us the flexibity to either; use the default value or overide it from the command-line with the **'--parameters'** option.

Notice how the **Mappings:** block allows us to create a 'lookup' table for **ImageIds** per region.

Notice how under **PublicInstance** and **Private Instance**, we use **!FindInMap** to have CloudFormation lookup the correct ImageId, based on the AWS Region we are deploying to. This gives the template flexibility for use in any region.

Notice how **!Ref** is used to reference other resources by name where needed.**

.. code-block::

	---
	Parameters:
	  KeyPairName:
	    Type: String
	    Default: acpkey1
	    Description: Name of existing KeyPair

	Mappings: 
	  RegionMap: 
	    us-east-1: 
	      "64": "ami-a4dc46db"
	    us-east-2: 
	      "64": "ami-6a003c0f"
	    us-west-1:
	      "64": "ami-8d948ced"
	    us-west-2:
	      "64": "ami-db710fa3"
	    ca-central-1:
	      "64": "ami-7e21a11a"
	    eu-west-1:
	      "64": "ami-58d7e821"
	    eu-west-2:
	      "64": "ami-5daa463a"
	    eu-west-3:
	      "64": "ami-1960d164"
	    eu-central-1:
	      "64": "ami-c7e0c82c"
	    ap-northeast-1:
	      "64": "ami-48a45937"
	    ap-northeast-2:
	      "64": "ami-f030989e"
	    ap-southeast-1:
	      "64": "ami-81cefcfd"
	    ap-southeast-2:
	      "64": "ami-963cecf4"
	    ap-south-1:
	      "64": "ami-41e9c52e"
	    sa-east-1:
	      "64": "ami-67fca30b"

	Resources:
	  VPC:
	    Type: AWS::EC2::VPC
	    Properties: 
	      CidrBlock: 10.0.0.0/16
	      Tags:
	        - Key: Name
	          Value: vpc_ex004

	  InternetGateway:
	    Type: AWS::EC2::InternetGateway
	    Properties: 
	      Tags:
	        - Key: Name
	          Value: ig_ex004

	  AttachInternetGateway:
	    Type: AWS::EC2::VPCGatewayAttachment
	    Properties: 
	      InternetGatewayId: !Ref InternetGateway
	      VpcId: !Ref VPC

	  RouteTable:
	    Type: AWS::EC2::RouteTable
	    Properties: 
	      VpcId: !Ref VPC
	      Tags:
	        - Key: Name
	          Value: rtb_pub_ex004

	  DefaultRoute:
	    Type: AWS::EC2::Route
	    Properties: 
	      DestinationCidrBlock: 0.0.0.0/0
	      GatewayId: !Ref InternetGateway
	      RouteTableId: !Ref RouteTable

	  SubnetPublic:
	    Type: AWS::EC2::Subnet
	    Properties:
	      CidrBlock: 10.0.0.0/23
	      Tags:
	        - Key: Name
	          Value: sub_pub_ex004
	      VpcId: !Ref VPC
	  
	  SubnetPrivate:
	    Type: AWS::EC2::Subnet
	    Properties:
	      CidrBlock: 10.0.2.0/23
	      Tags:
	        - Key: Name
	          Value: sub_pri_ex004
	      VpcId: !Ref VPC

	  AssociateSubnetRouteTable:
	    Type: AWS::EC2::SubnetRouteTableAssociation
	    Properties: 
	      RouteTableId: !Ref RouteTable
	      SubnetId: !Ref SubnetPublic

	  SecurityGroup:
	    Type: AWS::EC2::SecurityGroup
	    Properties: 
	      GroupName: sg_ex005
	      GroupDescription: "Security Group for ex-004"
	      SecurityGroupIngress:
	        - 
	          CidrIp: 0.0.0.0/0
	          IpProtocol: tcp
	          FromPort: 22
	          ToPort: 22
	        - 
	          CidrIp: 0.0.0.0/0
	          IpProtocol: icmp
	          FromPort: -1
	          ToPort: -1
	      VpcId: !Ref VPC

	  PublicInstance:
	    Type: AWS::EC2::Instance
	    Properties: 
	      ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", 64]
	      InstanceType: t2.micro
	      KeyName: !Ref KeyPairName
	      SecurityGroupIds: 
	        - !Ref SecurityGroup
	      SubnetId: !Ref SubnetPublic
	      Tags: 
	        - Key: Name
	          Value: i_pub_ex004

	  PrivateInstance:
	    Type: AWS::EC2::Instance
	    Properties: 
	      ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", 64]
	      InstanceType: t2.micro
	      KeyName: !Ref KeyPairName
	      SecurityGroupIds: 
	        - !Ref SecurityGroup
	      SubnetId: !Ref SubnetPrivate
	      Tags: 
	        - Key: Name
	          Value: i_pri_ex004

	  FloatingIpAddress:
	    Type: "AWS::EC2::EIP"
	    Properties:
	      InstanceId: !Ref PublicInstance
	      Domain: vpc

	...

Validate template
-----------------
Use the following awscli command to validate the structure of the template file.

Note: the template-body paramater expects a URL, so the **'file://'** prefix is necessary

.. code-block::

	aws cloudformation validate-template --template-body file://templates/ex-004_template.yaml

Output:

.. code-block::

	{
		"Parameters": []
	}

Template summary
----------------
Use the following awscli command to get a summary of the template.

.. code-block::

	aws cloudformation get-template-summary --template-body file://templates/ex-004_template.yaml

Output:

.. code-block::

	{
    	"Parameters": [],
    	"ResourceTypes": [
        	"AWS::EC2::InternetGateway",
        	"AWS::EC2::VPC",
        	"AWS::EC2::RouteTable",
        	"AWS::EC2::VPCGatewayAttachment",
        	"AWS::EC2::Subnet",
        	"AWS::EC2::SecurityGroup",
        	"AWS::EC2::Subnet",
        	"AWS::EC2::Route",
        	"AWS::EC2::SubnetRouteTableAssociation",
        	"AWS::EC2::Instance",
        	"AWS::EC2::Instance",
        	"AWS::EC2::EIP"
        ],
        "Version": "2010-09-09"
	}

Estimated costs 
---------------
Use the following awscli command to get an estimated monthly cost for the components in the template.

.. code-block::

	aws cloudformation estimate-template-cost --template-body file://templates/ex-004_template.yaml

Output:

.. code-block::

	{
		"Url": "http://calculator.s3.amazonaws.com/calc5.html?key=cloudformation/4fd01c4d-7530-4462-a0c3-608cb6df057d"
	}

Copy the URL and paste it into your browser to see the estimated costs for this template. By default, the calculation is based on the EC2 instances will run 24 hours a day forever.

Create Stack
------------
Use the following awscli command to create a new **Stack** based on the template. If your Key Pair is not named **'acpkey1'**, set the **ParameterValue** to the correct name of your existing Key Pair.

Note: If you are using the **'acpkey1'** Key Pair, you can leave off the **'--parameters'** option all together.

.. code-block::

	aws cloudformation create-stack \
		--stack-name ex-004 \
		--template-body file://templates/ex-004_template.yaml \
		--parameters ParameterKey=KeyPairName,ParameterValue=acpkey1

Output:

.. code-block::

	{
    	"StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-004/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
	}

Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this command until **'StackStatus'** is **'CREATE_COMPLETE'**.

.. code-block::

	aws cloudformation describe-stacks --stack-name ex-004

Output:

.. code-block::

	{
		"Stacks": [
			{
				"StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-004/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            	"StackName": "ex-004",
            	"CreationTime": "2018-06-17T21:47:13.883Z",
            	"RollbackConfiguration": {},
            	"StackStatus": "CREATE_IN_PROGRESS",
            	"DisableRollback": false,
            	"NotificationARNs": [],
            	"Tags": [],
            	"EnableTerminationProtection": false
        	}
		]
	}

Review the events
-----------------
Use the following awscli command to explore the **StackEvents**.

.. code-block::

	aws cloudformation describe-stack-events --stack-name ex-004

Output:

.. code-block::

	... not included do to size ...

Delete the Stack
----------------
Use the following awscli command to delete the Stack.

.. code-block::

	aws cloudformation delete-stack --stack-name ex-004

Output:

.. code-block::

	... not included do to size ...

Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this until you get the following error: "An error occurred (ValidationError) when calling the DescribeStacks operation: Stack with id ex-004 does not exist"

.. code-block::

	aws cloudformation describe-stacks --stack-name ex-004

Output:

.. code-block::

	{
    	"Stacks": [
        	{
            	"StackId": "arn:aws:cloudformation:us-east-1:926075045128:stack/ex-004/fef146e0-7277-11e8-a610-50d5ca63261e",
            	"StackName": "ex-004",
            	"CreationTime": "2018-06-17T21:47:13.883Z",
            	"DeletionTime": "2018-06-17T23:25:39.791Z",
            	"RollbackConfiguration": {},
            	"StackStatus": "DELETE_IN_PROGRESS",
            	"DisableRollback": false,
            	"NotificationARNs": [],
            	"Tags": [],
            	"EnableTerminationProtection": false
        	}
    	]
	}

Summary
-------
- We created a policy that allows full access to CloudFormation.
- Using applied this policy to **apiuser01**. 
- We verified access to CloudFormation for **apiuser01**.
- We reviewed CloudFormation account limits.
- We reviewed the **Template** provided for this exercise. 
- We created a **Stack** and checked the status. 
- We explored the **StackEvents** for this **Stack**.
- We deleted the **Stack** and checked the status

Next steps
----------
In `ex-005 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-005_ExpandingVpcConfig.rst>`_, starting with a Template similar to one used in this exercise, we will expand our VPC configuration to incorporate new components. 




