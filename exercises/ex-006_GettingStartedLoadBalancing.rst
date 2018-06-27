ex-006: Getting started with Load Balancing
===========================================

Status
------
Version (Initial Draft)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001
   * - Prerequisite for exercise(s)
     - None

Objectives
----------

    - Explore AWS Application Load Balancer    
    - Explore AWS Network Load Balancer 
   

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
     - 
        + None (AWS does not charge for these basic VPC building blocks)
     - 
        + These basic VPC components will be created as part of the CloudFormation Stack. 
   * - On-demand Instances
     - 
        + $0.0116 per hour per Instance (t2.micro)
     - 
        + During this exercise, we will us three (3) Instances. The AMI that will be used is **'Ubuntu Server 16.04 LTS'**, which combined with the **'t2.micro'** Instance Type, is **'Free tier eligible'**.
        + These Instances will be launched as part of a CloudFormation Stack. 
        + It is not expected that these Instances will need to be running for more than one hour. 
   * - Elastic IPs
     - 
        + $0.00 per hour per EIP that is associated to a running Instance
        + $0.005 per hour per EIP that is NOT associated to a running Instance
     - 
        + During this exercise, we will use one (1) EIP. This EIP will be mapped to an Instance. 
        + This EIP is allocated and mapped as part of a CloudFormation Stack. 
   * - Application Load Balancing
     - 
        + Between $0.0225 and $0.034 per Application Load Balancer-hour (or partial hour), depending on your region.
        + Between $0.008 and $0.011 per LCU-hour (or partial hour), depending on your region.
     - 
        + It is not expected that this Load balancer will need to be running for more than one hour.
   * - Network Load Balancing
     - 
        + Between $0.0225 and $0.034 per Network Load Balancer-hour (or partial hour), depending on your region.
        + Between $0.006 and $0.0083 per LCU-hour (or partial hour), depending on your region.
     - 
        + During this exercise, we will be creating an Application Load Balancer.
        + It is not expected that this Load balancer will need to be running for more than one hour. 

   * - Data Transfer
     -
        + $0.00 per GB - Data Transfer IN to Amazon EC2 from Internet
        + $0.00 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(up to 1 GB)**
        + $0.09 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(next 9.999 TB)**
     - We also need to consider Data Transfer charges when using either the Network or Application Load balancers.

Limits
------
You can view all your EC2 limits and request increases by clicking on 'Limits' in the navigation pane of the EC2 console.

Environment variables
---------------------
During these exercises, we will be using the output of some commands to creatie environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Template
--------
In order to build our starting configuration, we will create a CloudFormation Stack from Template **'ex-006_template.yaml'** in the **'templates'** directory.

The following section only shows the resources that differ from previous Templates.

.. code-block::

    ---
    Resources:      
      SubnetWeb1:
        Type: AWS::EC2::Subnet
        Properties:
          CidrBlock: 10.0.0.0/24
          AvailabilityZone: !Select 
            - 0
            - Fn::GetAZs: !Ref 'AWS::Region'
          Tags:
            - Key: Name
              Value: subnet_web1_ex006
          VpcId: !Ref VPC

      SubnetWeb2:
        Type: AWS::EC2::Subnet
        Properties:
          CidrBlock: 10.0.1.0/24
          AvailabilityZone: !Select 
            - 1
            - Fn::GetAZs: !Ref 'AWS::Region'
          Tags:
            - Key: Name
              Value: subnet_web2_ex006
          VpcId: !Ref VPC

      SecurityGroupJumpbox:
        Type: AWS::EC2::SecurityGroup
        Properties: 
          GroupName: sg_jumpbox_ex006
          GroupDescription: "Security Group for Jumpbox Instance in ex-006"
          SecurityGroupIngress:
            - 
              CidrIp: 0.0.0.0/0
              IpProtocol: tcp
              FromPort: 22
              ToPort: 22
          VpcId: !Ref VPC

      SecurityGroupWebInstances:
        Type: AWS::EC2::SecurityGroup
        Properties: 
          GroupName: sg_web-instances_ex006
          GroupDescription: "Security Group for Web Instances in ex-006"
          SecurityGroupIngress:
            - 
              CidrIp: 10.0.100.0/24
              IpProtocol: tcp
              FromPort: 22
              ToPort: 22
            - 
              CidrIp: 10.0.0.0/16
              IpProtocol: tcp
              FromPort: 80
              ToPort: 80
            - 
              CidrIp: 10.0.0.0/16
              IpProtocol: tcp
              FromPort: 443
              ToPort: 443
          VpcId: !Ref VPC

      SecurityGroupLoadBalancer:
        Type: AWS::EC2::SecurityGroup
        Properties: 
          GroupName: sg_load-balancer_ex006
          GroupDescription: "Security Group for Load balancer in ex-006"
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

      WebInstance1:
        Type: AWS::EC2::Instance
        Properties: 
          ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", 64]
          InstanceType: t2.micro
          KeyName: acpkey1
          SecurityGroupIds: 
            - !Ref SecurityGroupWebInstances
          SubnetId: !Ref SubnetWeb1
          Tags: 
            - Key: Name
              Value: i_web1_ex006
          UserData: !Base64
            "Fn::Join":
              - "\n"
              -
                - "#!/bin/bash"
                - "sudo apt-get update"
                - "sudo apt-get dist-upgrade -y"
                - "sudo echo \"<html><body><h1>$(cat /etc/hostname)</h1></body></html>\" > index.html"
                - "sudo python3 -m http.server 80"
        DependsOn: DefaultRoutePublic

      WebInstance2:
        Type: AWS::EC2::Instance
        Properties: 
          ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", 64]
          InstanceType: t2.micro
          KeyName: acpkey1
          SecurityGroupIds: 
            - !Ref SecurityGroupWebInstances
          SubnetId: !Ref SubnetWeb2
          Tags: 
            - Key: Name
              Value: i_web2_ex006
          UserData: !Base64
            "Fn::Join":
              - "\n"
              -
                - "#!/bin/bash"
                - "sudo apt-get update"
                - "sudo apt-get dist-upgrade -y"
                - "sudo echo \"<html><body><h1>$(cat /etc/hostname)</h1></body></html>\" > index.html"
                - "sudo python3 -m http.server 80"
        DependsOn: DefaultRoutePublic
    ...

Notable items in the Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When creating an Application Load Balancer, it is required that at least two Subnets, from different Availability Zones, be specified. The following built-in functions are used to:

    - Get a list of all the Availability Zones (AZ) in the Region that the Stack is being deployed in.
    - Select the 1st (0) AZ and create **'SubnetWeb1'** there.
    - Select the 2nd (1) AZ and create **'SubnetWeb2'** there.

.. code-block::

    SubnetWeb1:
      Properties:
        AvailabilityZone: !Select 
          - 0
          - Fn::GetAZs: !Ref 'AWS::Region'

    SubnetWeb2:
      Properties:
        AvailabilityZone: !Select 
          - 1
          - Fn::GetAZs: !Ref 'AWS::Region'

In order to create a simple web server, the following commands are run at Instance startup. An 'index.html' file is created that contains the 'hostname' of the Instance and a simple http server is started.

    - The built-in function 'Join', joins each command with a newline character.
    - The built-in function 'Base64', encodes the data.

.. code-block::
    
    WebInstance1:
      UserData: !Base64
        "Fn::Join":
          - "\n"
          -
            - "sudo echo \"<html><body><h1>$(cat /etc/hostname)</h1></body></html>\" > index.html"
            - "sudo python3 -m http.server 80"

    WebInstance2:
      UserData: !Base64
        "Fn::Join":
          - "\n"
          -
            - "sudo echo \"<html><body><h1>$(cat /etc/hostname)</h1></body></html>\" > index.html"
            - "sudo python3 -m http.server 80"

In order to illustrate the **'DependsOn'** resource attribute, we have specified that launching of 'WebInstance1' and 'WebInstance2' must come after the creation of 'DefaultRoutePublic'. In theory, ensuring that a path to the Internet is available before the Instances are launched. 

.. code-block::

    WebInstance1:
      DependsOn: DefaultRoutePublic

    WebInstance2:
      DependsOn: DefaultRoutePublic

Create Stack
------------
Use the following awscli command to create a new **'Stack'** based on the template.

.. code-block::

    aws cloudformation create-stack --stack-name ex-006 --template-body file://templates/ex-006_template.yaml

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

    aws cloudformation describe-stacks --stack-name ex-006

Output:

.. code-block::

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-005/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "StackName": "ex-006",
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

    aws cloudformation describe-stack-resources --stack-name ex-006 --output table --query 'StackResources[*].{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'

Output:

.. code-block::

    --------------------------------------------------------------------------
    |                         DescribeStackResources                         |
    +-----------------------------------------+------------------------------+
    |           Logical Resource Id           |    Physical Resource Id      |
    +-----------------------------------------+------------------------------+
    |  AssociateSubnetJumpboxRouteTablePublic |  rtbassoc-096e54d60e95fc651  |
    |  AssociateSubnetWeb1RouteTablePublic    |  rtbassoc-06972ab97b655c296  |
    |  AssociateSubnetWeb2RouteTablePublic    |  rtbassoc-0dbe61a08c47c36d9  |
    |  AttachInternetGateway                  |  ex-00-Attac-1UCSPHVOPXXF2   |
    |  DefaultRoutePublic                     |  ex-00-Defau-YMTP8R2B08JM    |
    |  FloatingIpAddressInstance              |  52.73.187.16                |
    |  InternetGateway                        |  igw-0464ded68dd7ea0f9       |
    |  JumpboxInstance                        |  i-0fca677b00c3a1031         |
    |  RouteTablePublic                       |  rtb-0d35eaed91bf21e8a       |
    |  SecurityGroupJumpbox                   |  sg-007b8cf9d92fb0388        |
    |  SecurityGroupLoadBalancer              |  sg-0835a8e19a39d2d72        |
    |  SecurityGroupWebInstances              |  sg-04ea8555fcc3a99a5        |
    |  SubnetJumpbox                          |  subnet-02ba11ac104e63757    |
    |  SubnetWeb1                             |  subnet-0fa9c08f6a27f2a5c    |
    |  SubnetWeb2                             |  subnet-0aa1a04c1a9147efe    |
    |  VPC                                    |  vpc-0df15a2ef5e094e61       |
    |  WebInstance1                           |  i-03789ca2ca19ffec9         |
    |  WebInstance2                           |  i-0ff622c3cf8af230c         |
    +-----------------------------------------+------------------------------+

Environment variables
~~~~~~~~~~~~~~~~~~~~~
Run the following commands to capture the 'PhysicalResourceId' for the applicable components.

.. code-block::

    export EX006_SUBNET_WEB1=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SubnetWeb1`].PhysicalResourceId')

    export EX006_SUBNET_WEB2=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SubnetWeb2`].PhysicalResourceId')

    export EX006_SG_LB=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SecurityGroupLoadBalancer`].PhysicalResourceId')

    export EX006_VPC=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`VPC`].PhysicalResourceId')

    export EX006_INST_WEB1=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`WebInstance1`].PhysicalResourceId')

    export EX006_INST_WEB2=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`WebInstance2`].PhysicalResourceId')

Sanity check
~~~~~~~~~~~~

.. code-block::
    
    echo $EX006_SUBNET_WEB1
    echo $EX006_SUBNET_WEB2
    echo $EX006_SG_LB
    echo $EX006_VPC
    echo $EX006_INST_WEB1
    echo $EX006_INST_WEB2


Create load-balancer
--------------------

.. code-block::

    aws elbv2 create-load-balancer --name ex-006-app-lb --scheme internet-facing --type application --ip-address-type ipv4 --subnets $EX006_SUBNET_WEB1 $EX006_SUBNET_WEB2 --security-groups $EX006_SG_LB

Output:

.. code-block::

    {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:loadbalancer/app/ex-006-app-lb/932c682273bd2b8c",
                "DNSName": "ex-006-app-lb-338618850.us-east-1.elb.amazonaws.com",
                "CanonicalHostedZoneId": "Z35SXDOTRQ7X7K",
                "CreatedTime": "2018-06-26T14:49:01.260Z",
                "LoadBalancerName": "ex-006-app-lb",
                "Scheme": "internet-facing",
                "VpcId": "vpc-0df15a2ef5e094e61",
                "State": {
                    "Code": "provisioning"
                },
                "Type": "application",
                "AvailabilityZones": [
                    {
                        "ZoneName": "us-east-1b",
                        "SubnetId": "subnet-0aa1a04c1a9147efe"
                    },
                    {
                        "ZoneName": "us-east-1a",
                        "SubnetId": "subnet-0fa9c08f6a27f2a5c"
                    }
                ],
                "SecurityGroups": [
                    "sg-0835a8e19a39d2d72"
                ],
                "IpAddressType": "ipv4"
            }
        ]
    }

Environment variables
~~~~~~~~~~~~~~~~~~~~~
Create the following environment variable.

.. code-block::

    export EX006_LB=<LoadBalancerArn>

Create Target Group
-------------------

.. code-block::

    aws elbv2 create-target-group --name ex-006-webservers --protocol HTTP --port 80 --vpc-id $EX006_VPC

Output:

.. code-block::

    {
        "TargetGroups": [
            {
                "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:targetgroup/ex-006-webservers/2f5bbf3fbd91d3b6",
                "TargetGroupName": "ex-006-webservers",
                "Protocol": "HTTP",
                "Port": 80,
                "VpcId": "vpc-0df15a2ef5e094e61",
                "HealthCheckProtocol": "HTTP",
                "HealthCheckPort": "traffic-port",
                "HealthCheckIntervalSeconds": 30,
                "HealthCheckTimeoutSeconds": 5,
                "HealthyThresholdCount": 5,
                "UnhealthyThresholdCount": 2,
                "HealthCheckPath": "/",
                "Matcher": {
                    "HttpCode": "200"
                },
                "TargetType": "instance"
            }
        ]
    }

Environment variables
~~~~~~~~~~~~~~~~~~~~~
Create the following environment variable.

.. code-block::

    export EX006_TG=<TargetGroupArn>

Register Targets
----------------

.. code-block::

    aws elbv2 register-targets --target-group-arn $EX006_TG --targets Id=$EX006_INST_WEB1 Id=$EX006_INST_WEB2


Describe Target Group
---------------------

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX006_TG

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-03789ca2ca19ffec9",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "unused",
                    "Reason": "Target.NotInUse",
                    "Description": "Target group is not configured to receive traffic from the load balancer"
                }
            },
            {
                "Target": {
                    "Id": "i-0ff622c3cf8af230c",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "unused",
                    "Reason": "Target.NotInUse",
                    "Description": "Target group is not configured to receive traffic from the load balancer"
                }
            }
        ]
    }

Create a listener
-----------------

.. code-block::

    aws elbv2 create-listener --load-balancer-arn $EX006_LB --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=$EX006_TG

Output:

.. code-block::

    {
        "Listeners": [
            {
                "ListenerArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:listener/app/ex-006-app-lb/932c682273bd2b8c/d8e6b15fe1631f71",
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:loadbalancer/app/ex-006-app-lb/932c682273bd2b8c",
                "Port": 80,
                "Protocol": "HTTP",
                "DefaultActions": [
                    {
                        "Type": "forward",
                        "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:targetgroup/ex-006-webservers/2f5bbf3fbd91d3b6"
                    }
                ]
            }
        ]
    }

Describe Target Group
---------------------
Let's look at the Target Group again

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX006_TG

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-03789ca2ca19ffec9",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            },
            {
                "Target": {
                    "Id": "i-0ff622c3cf8af230c",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            }
        ]
    }

Load Balancer DNS Name
----------------------

.. code-block::

    aws elbv2 describe-load-balancers --load-balancer-arns $EX006_LB --output text --query LoadBalancers[*].DNSName

Output:

.. code-block::

    ex-006-app-lb-338618850.us-east-1.elb.amazonaws.com

Test connectivity
-----------------
Using 'curl' or your browser test connectivity. Rerun/refresh a few time to make sure you see the IP address of both Web Servers. 

.. code-block::

curl http://ex-006-app-lb-338618850.us-east-1.elb.amazonaws.com


Delete the Load Balancer
------------------------

.. code-block::
    
    aws elbv2 delete-load-balancer --load-balancer-arn $EX006_LB

Delete the Target Group
-----------------------

.. code-block::

    aws elbv2 delete-target-group --target-group-arn $EX006_TG

Delete the Stack
----------------

.. code-block::

    aws cloudformation delete-stack --stack-name ex-006


.. code-block::

    aws cloudformation describe-stacks --stack-name ex-006

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