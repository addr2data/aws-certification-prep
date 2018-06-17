ex-005: Getting Started with CloudFormation
===========================================

Status
------
Draft (once the draft has been completed, a version number and date will be provided)

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

    - Learn how CloudFormation Templates are constructed in YAML.
    - Create a Stack in CloudFormation from a Template that mimics the configuration from ex-003 and ex-004.  

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 1

   * - Component
     - Applicable Costs
     - Notes
   * - CloudFormation
     - 
        + $0.00
     -
   * - VPC
     - 
        + $0.00
     - 
   * - Route Table
     - 
        + $0.00
     -
   * - Subnet
     - 
        + $0.00
     -
   * - Internet Gateway
     - 
        + $0.00
     -
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
     - During this exercise we will be launching two Instances, using ami-a4dc46db (Ubuntu Server 16.04 LTS), which is 'Free tier eligible'. It is not expected that these Instances will need to be running for more than one hour. 
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

Add CloudFormation API access to user 'apiuser01' 
-------------------------------------------------
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
- Under **Add permissions to admin01**, select **Attach existing policies directly**.
- In the search box, type **CloudFormationFullAccess**, then select **CloudFormationFullAccess**.
- Click on **Next: Review**.
- Click **Add permissions**.

Verify access
-------------
Use the following awscli command to verify access to CloudFormation API.

.. code-block::
    
    aws cloudformation describe-stacks

    {
    	"Stacks": []
	}

Review the template
-------------------
Below is the contents of the **'ex-005_template.yaml'** file from the **templates/** directory.

.. code-block::

	---

	Resources:
		VPC:
    		Type: AWS::EC2::VPC
    		Properties: 
      	  		CidrBlock: 10.0.0.0/16
      	  		Tags:
        			- Key: Name
          			  Value: vpc_ex005

  		InternetGateway:
    		Type: AWS::EC2::InternetGateway
    		Properties: 
      			Tags:
        			- Key: Name
          			  Value: ig_ex005

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
          			  Value: rtb_pub_ex005

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
          		  	  Value: sub_pub_ex005
      			VpcId: !Ref VPC
  
  		SubnetPrivate:
    		Type: AWS::EC2::Subnet
    		Properties:
      			CidrBlock: 10.0.2.0/23
      			Tags:
        		- Key: Name
          		  Value: sub_pri_ex005
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
      GroupDescription: "Security Group for ex-005"
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
      ImageId: ami-a4dc46db
      InstanceType: t2.micro
      KeyName: acpkey1
      SecurityGroupIds: 
        - !Ref SecurityGroup
      SubnetId: !Ref SubnetPublic
      Tags: 
        - Key: Name
          Value: i_pub_ex005

  PrivateInstance:
    Type: AWS::EC2::Instance
    Properties: 
      ImageId: ami-a4dc46db
      InstanceType: t2.micro
      KeyName: acpkey1
      SecurityGroupIds: 
        - !Ref SecurityGroup
      SubnetId: !Ref SubnetPrivate
      Tags: 
        - Key: Name
          Value: i_pri_ex005

  FloatingIpAddress:
    Type: "AWS::EC2::EIP"
    Properties:
      InstanceId: !Ref PublicInstance
      Domain: vpc

...









Validate Stack
--------------
aws cloudformation validate-template --template-body file:////Users/addr2data/docs-sphinx/aws-cert-prep/templates/ex-005_template.yaml

{
    "Parameters": []
}


aws cloudformation delete-stack --stack-name ex-005



Create Stack
------------
aws cloudformation create-stack --stack-name ex-005 --template-body file:////Users/addr2data/docs-sphinx/aws-cert-prep/templates/ex-005_template.yaml

{
    "StackId": "arn:aws:cloudformation:us-east-1:926075045128:stack/ex-005/7931a220-7231-11e8-ae07-500c28b12efe"
}





.. code-block::
    
    aws cloudformation describe-stacks

{
    "Stacks": [
        {
            "StackId": "arn:aws:cloudformation:us-east-1:926075045128:stack/ex-005/dbb88910-7234-11e8-afde-500c221b72d1",
            "StackName": "ex-005",
            "CreationTime": "2018-06-17T13:46:38.508Z",
            "RollbackConfiguration": {},
            "StackStatus": "CREATE_COMPLETE",
            "DisableRollback": false,
            "NotificationARNs": [],
            "Tags": []
        }
    ]
}

.. code-block::
    
    aws cloudformation list-stack-instances --stack-set-name ex-005





