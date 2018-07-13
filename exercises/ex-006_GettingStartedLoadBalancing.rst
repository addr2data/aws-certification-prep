ex-006: Getting started with Load-balancing
===========================================

Status
------
Version 0.9 (06/28/18)

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

    - Explore AWS Application Load-balancers    
    - Explore AWS Network Load-balancers

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
        + During this exercise, we will deploy basic VPC components.
        + They will be deployed as part of the CloudFormation Stack. 
   * - On-demand Instances
     - 
        + $0.0116 per hour per Instance (t2.micro)
     - 
        + During this exercise, we will deploy two (2) Instances. The AMI that will be used is **'Ubuntu Server 16.04 LTS'**, which combined with the **'t2.micro'** Instance Type, is **'Free tier eligible'**.
        + They will be deployed as part of a CloudFormation Stack. 
        + They should not need to run for more than a hour or so.
   * - NAT Gateway
     - 
        + Between $0.045 and $0.093 per hour, depending on Region.
        + Between $0.045 and $0.093 per GB of data processed, depending on Region.
     - 
        + During this exercise, we will deploy a NAT Gateway.
        + It will be deployed as part of a CloudFormation Stack. 
        + It should not need to run for more than a hour or so.
        + A small amount of data will be processed through it.
   * - Application Load-balancing
     - 
        + Between $0.0225 and $0.034 per Application Load Balancer-hour (or partial hour), depending on your region.
        + Between $0.008 and $0.011 per LCU-hour (or partial hour), depending on your region.
     - 
        + During this exercise, we will deploy an Application Load balancer.
        + It will be deployed manually using the awscli.
        + It should not need to run for more than a hour or so.
   * - Network Load-balancing
     - 
        + Between $0.0225 and $0.034 per Network Load Balancer-hour (or partial hour), depending on your region.
        + Between $0.006 and $0.0083 per LCU-hour (or partial hour), depending on your region.
     - 
        + During this exercise, we will deploy an Application Load balancer.
        + It will be deployed manually using the awscli.
        + It should not need to run for more than a hour or so.

   * - Data Transfer
     -
        + $0.00 per GB - Data Transfer IN to Amazon EC2 from Internet
        + $0.00 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(up to 1 GB)**
        + $0.09 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(next 9.999 TB)**
     - 
        + We also need to consider Data Transfer charges when using either the Network or Application Load balancers.

Limits
------
You can view all your EC2 limits and request increases by clicking on 'Limits' in the navigation pane of the EC2 console.

Environment variables
---------------------
During these exercises, we will be using the output of some commands to create environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Diagram
-------
In this configuration, we will be building the following configuration.

.. image:: https://github.com/addr2data/aws-certification-prep/blob/master/images/ex-006.png

Template
--------
For our starting configuration, we will create a CloudFormation **Stack** from a Template. Please review **'ex-006_template.yaml'** in the **'templates'** directory.

**Highlights**

    - Two Instances that will act as Web Servers.
    - Two **public** Subnets (10.0.0.0/24 and 10.0.1.0/24). Each in a different Availability Zone.
    - Two **private** Subnets (10.0.128.0/24 and 10.0.129.0/24). Each in a different Availability Zone.
    - An Internet Gateway to allow Internet access to/from the public Subnets.
    - A NAT Gateway to allow Internet access from the private Subnets.
    - A Security Group for the Web Servers that allows **HTTP** from anywhere in the VPC (10.0.0.0/16)
    - A Security Group for the Load-balancer that allows **HTTP** from anywhere (0.0.0.0/0)

**Notable item**

When creating an Application Load-balancer (ALB), you must specify at least two Subnets, from different Availability Zones. In order to achieve this, a couple of CloudFormation built-in functions will be used in the Template

Note: The Network Load-balancer (NLB) does not have this requirement.

.. code-block::

    PublicSubnet1:
      Type: AWS::EC2::Subnet
      Properties:
        CidrBlock: 10.0.0.0/24
        AvailabilityZone: !Select 
          - 0
          - Fn::GetAZs: !Ref 'AWS::Region'
        Tags:
          - Key: Name
            Value: subnet_public1_ex006
        VpcId: !Ref VPC
    PublicSubnet2:
      Type: AWS::EC2::Subnet
      Properties:
        CidrBlock: 10.0.1.0/24
        AvailabilityZone: !Select 
          - 1
          - Fn::GetAZs: !Ref 'AWS::Region'
        Tags:
          - Key: Name
            Value: subnet_public2_ex006
        VpcId: !Ref VPC

Explanation:

  - **Fn::GetAZs** returns us a list of Availability Zones (AZ) for a Region. **!Ref 'AWS::Region'** says to use the Region that the Stack is being deployed to.
  - **!Select** lets us select the 1st item (0) in the list, for **PublicSubnet1** and the 2nd item (1) for **PublicSubnet2**, ensuring that the two Subnets are located on different AZs.
  - Every Region has at least two AZs, so this is Template is portable between Regions.

**Notable item**

We will use the same methodology for selecting Availability Zones (AZs) for the **private** Subnets. We will connect one Web Server to each private Subnet.

Note: When a Load balancer node in one AZ is able to distribute client requests to targets (the Web Servers in this case) in all AZs, this in known as Cross-zone Load balancing. This capability is always on in ALBs, but is disabled by default in NLBs.

.. code-block::

    PrivateSubnet1:
      Type: AWS::EC2::Subnet
      Properties:
        CidrBlock: 10.0.128.0/24
        AvailabilityZone: !Select 
          - 0
          - Fn::GetAZs: !Ref 'AWS::Region'
        Tags:
          - Key: Name
            Value: subnet_private1_ex006
        VpcId: !Ref VPC
    PrivateSubnet2:
      Type: AWS::EC2::Subnet
      Properties:
        CidrBlock: 10.0.129.0/24
        AvailabilityZone: !Select 
          - 1
          - Fn::GetAZs: !Ref 'AWS::Region'
        Tags:
          - Key: Name
            Value: subnet_private2_ex006
        VpcId: !Ref VPC


**Notable item**

We need a way to verify the Load-balancer is functioning properly. To accomplish this, we will create a simplistic web server. Python provides a simple HTTP server that can be started, without any configuration, in any directory. Redirecting the contents of '/etc/hostname' to 'index.html' allows us to tell the Web Servers apart. 

.. code-block::
    
    WebInstance1:
      Type: AWS::EC2::Instance
      Properties: 
        ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", 64]
        InstanceType: t2.micro
        KeyName: !Ref KeyPairName
        SecurityGroupIds: 
          - !Ref SecurityGroupWebInstances
        SubnetId: !Ref PrivateSubnet1
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
      DependsOn: DefaultRoutePrivate
    WebInstance2:

      ... excluded for brevity ...

Explanation:

    - The **UserData** property allows us to specify commands to run at Instance startup.
    - **Fn::Join** allows us to join each command with newline character.
    - **!Base64** encodes the data for transmission to the Instance.

Create Stack
------------
Use the following awscli command to create a new CloudFormation **'Stack'** based on the template.

Note: If you are using the **'acpkey1'** Key Pair, you can leave off the **'--parameters'** option all together.

.. code-block::

    aws cloudformation create-stack \
        --stack-name ex-006 \
        --template-body file://templates/ex-006_template.yaml \
        --parameters ParameterKey=KeyPairName,ParameterValue=acpkey1

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

Notice the format of this portion of the query string **'{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'**, it adds a header to each column.** 

.. code-block::

    aws cloudformation describe-stack-resources \
        --stack-name ex-006 \
        --output table \
        --query 'StackResources[*].{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'

Output:

.. code-block::

    +----------------------------------------+------------------------------+
    |           Logical Resource Id          |    Physical Resource Id      |
    +----------------------------------------+------------------------------+
    |  AssociateSubnetWeb1RouteTablePrivate1 |  rtbassoc-xxxxxxxxxxxxxxxxx  |
    |  AssociateSubnetWeb1RouteTablePrivate2 |  rtbassoc-xxxxxxxxxxxxxxxxx  |
    |  AssociateSubnetWeb1RouteTablePublic1  |  rtbassoc-xxxxxxxxxxxxxxxxx  |
    |  AssociateSubnetWeb1RouteTablePublic2  |  rtbassoc-xxxxxxxxxxxxxxxxx  |
    |  AttachInternetGateway                 |  ex-00-Attac-XXXXXXXXXXXXX   |
    |  DefaultRoutePrivate                   |  ex-00-Defau-XXXXXXXXXXXX    |
    |  DefaultRoutePublic                    |  ex-00-Defau-XXXXXXXXXXXX    |
    |  FloatingIpAddressNatGateway           |  xxx.xxx.xxx.xxx             |
    |  InternetGateway                       |  igw-xxxxxxxxxxxxxxxxx       |
    |  NatGateway                            |  nat-xxxxxxxxxxxxxxxxx       |
    |  PrivateSubnet1                        |  subnet-xxxxxxxxxxxxxxxxx    |
    |  PrivateSubnet2                        |  subnet-xxxxxxxxxxxxxxxxx    |
    |  PublicSubnet1                         |  subnet-xxxxxxxxxxxxxxxxx    |
    |  PublicSubnet2                         |  subnet-xxxxxxxxxxxxxxxxx    |
    |  RouteTablePrivate                     |  rtb-xxxxxxxxxxxxxxxxx       |
    |  RouteTablePublic                      |  rtb-xxxxxxxxxxxxxxxxx       |
    |  SecurityGroupLoadBalancer             |  sg-xxxxxxxxxxxxxxxxx        |
    |  SecurityGroupWebInstances             |  sg-xxxxxxxxxxxxxxxxx        |
    |  VPC                                   |  vpc-xxxxxxxxxxxxxxxxx       |
    |  WebInstance1                          |  i-xxxxxxxxxxxxxxxxx         |
    |  WebInstance2                          |  i-xxxxxxxxxxxxxxxxx         |
    +----------------------------------------+------------------------------+

Environment variables
~~~~~~~~~~~~~~~~~~~~~
Run the following commands to capture the 'PhysicalResourceId' for the applicable components, as environment variables.

.. code-block::

    export EX006_SUBNET_LB1=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`PublicSubnet1`].PhysicalResourceId')

    export EX006_SUBNET_LB2=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`PublicSubnet2`].PhysicalResourceId')

    export EX006_SG_LB=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SecurityGroupLoadBalancer`].PhysicalResourceId')

    export EX006_SG_WEB=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SecurityGroupWebInstances`].PhysicalResourceId')

    export EX006_VPC=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`VPC`].PhysicalResourceId')

    export EX006_INST_WEB1=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`WebInstance1`].PhysicalResourceId')

    export EX006_INST_WEB2=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`WebInstance2`].PhysicalResourceId')

Sanity check
~~~~~~~~~~~~

.. code-block::
    
    echo -e $EX006_SUBNET_LB1'\n'$EX006_SUBNET_LB2'\n'$EX006_SG_LB'\n'$EX006_VPC'\n'$EX006_INST_WEB1'\n'$EX006_INST_WEB2'\n'$EX006_SG_WEB


Create Application Load-balancer
--------------------------------
Use the following awscli command to create an Application Load-balancer.

.. code-block::

    aws elbv2 create-load-balancer \
        --name ex-006-app-lb \
        --scheme internet-facing \
        --type application \
        --ip-address-type ipv4 \
        --subnets $EX006_SUBNET_LB1 $EX006_SUBNET_LB2 \
        --security-groups $EX006_SG_LB

Additional information for the above parameters:

.. list-table::
   :widths: 50, 50
   :header-rows: 0

   * - **Parameter**
     - **Description**
   * - '--name ex-006-app-lb'
     - Specifies a name for the Load-balancer.
   * - '--scheme internet-facing'
     - 
        + **'internet-facing'**: Load-balancer nodes have public IP addresses and the DNS name is publicly resolvable. You can access the Load-balancer from anywhere.
        + **'internal'**: Load-balancer nodes have private IP addresses, but the DNS name is still publicly resolvable (to private IP). You can only access the Load-balancer from inside the VPC.
   * - '--type application'
     - 
        + **'application'**: Operates at Layer 7 (defaults to application, so we could have left this parameter off).
        + **'network'**: Operates at Layer 4.
   * - '--ip-address-type ipv4'
     - Application Load-balancer can support both ipv4 and ipv6
   * - '--subnets $EX006_SUBNET_WEB1 $EX006_SUBNET_WEB2'
     - 
        + You can only select one Subnet per AZ.
        + Application Load-balancers require two or more Subnets.
        + network Load-balancers require one or more Subnets.
        + Instead of **'--Subnets'**, you can use **'--subnet-mappings'**, which are outside the scope of this exercise.   
   * - '--security-groups $EX006_SG_LB'
     - 
        + One or more Security Groups to control access to an Application Load-balancer.
        + Security Groups are NOT applicable to Network Load-balancers.

Output:

.. code-block::

    {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:loadbalancer/app/ex-006-app-lb/xxxxxxxxxxxxxxxx",
                "DNSName": "ex-006-app-lb-xxxxxxxxx.us-east-1.elb.amazonaws.com",
                "CanonicalHostedZoneId": "XXXXXXXXXXXXXX",
                "CreatedTime": "2018-06-26T14:49:01.260Z",
                "LoadBalancerName": "ex-006-app-lb",
                "Scheme": "internet-facing",
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
                "State": {
                    "Code": "provisioning"
                },
                "Type": "application",
                "AvailabilityZones": [
                    {
                        "ZoneName": "us-east-1b",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx"
                    },
                    {
                        "ZoneName": "us-east-1a",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx"
                    }
                ],
                "SecurityGroups": [
                    "sg-xxxxxxxxxxxxxxxxx"
                ],
                "IpAddressType": "ipv4"
            }
        ]
    }

Check Load-balancer status
--------------------------
Use the following awscli command to check the **'State:Code'** of the Load-balancer.

Rerun this command until **'State:Code'** is **'active'**.

.. code-block::

    aws elbv2 describe-load-balancers --names ex-006-app-lb

Output:

.. code-block::

    {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxxx:loadbalancer/app/ex-006-app-lb/xxxxxxxxxxxxxxxx",
                "DNSName": "ex-006-app-lb-xxxxxxxxxx.us-east-1.elb.amazonaws.com",
                "CanonicalHostedZoneId": "XXXXXXXXXXXXXX",
                "CreatedTime": "2018-06-27T19:08:51.150Z",
                "LoadBalancerName": "ex-006-app-lb",
                "Scheme": "internet-facing",
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
                "State": {
                    "Code": "active"
                },
                "Type": "application",
                "AvailabilityZones": [
                    {
                        "ZoneName": "us-east-1a",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx"
                    },
                    {
                        "ZoneName": "us-east-1b",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx"
                    }
                ],
                "SecurityGroups": [
                    "sg-xxxxxxxxxxxxxxxxx"
                ],
                "IpAddressType": "ipv4"
            }
        ]
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
Create the following environment variable.

.. code-block::

    export EX006_APP_LB=$(aws elbv2 describe-load-balancers --names ex-006-app-lb --output text --query LoadBalancers[*].LoadBalancerArn)


Create Network Load-balancer
--------------------------------
Use the following awscli command to create a Network Load-balancer.

.. code-block::

    aws elbv2 create-load-balancer \
        --name ex-006-net-lb \
        --scheme internet-facing \
        --type network \
        --ip-address-type ipv4 \
        --subnets $EX006_SUBNET_LB1 $EX006_SUBNET_LB2

Output:

.. code-block::

    {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:loadbalancer/net/ex-006-net-lb/xxxxxxxxxxxxxxxx",
                "DNSName": "ex-006-net-lb-xxxxxxxxxxxxxxxx.elb.us-east-1.amazonaws.com",
                "CanonicalHostedZoneId": "XXXXXXXXXXXXXX",
                "CreatedTime": "2018-06-28T14:02:10.158Z",
                "LoadBalancerName": "ex-006-net-lb",
                "Scheme": "internet-facing",
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
                "State": {
                    "Code": "provisioning"
                },
                "Type": "network",
                "AvailabilityZones": [
                    {
                        "ZoneName": "us-east-1b",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx"
                    },
                    {
                        "ZoneName": "us-east-1a",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx"
                    }
                ],
                "IpAddressType": "ipv4"
            }
        ]
    }

Check Load-balancer status
--------------------------
Use the following awscli command to check the **'State:Code'** of the Load-balancer.

Rerun this command until **'State:Code'** is **'active'**.

.. code-block::

    aws elbv2 describe-load-balancers --names ex-006-net-lb

Output:

.. code-block::

    {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:loadbalancer/net/ex-006-net-lb/xxxxxxxxxxxxxxxx",
                "DNSName": "ex-006-net-lb-xxxxxxxxxxxxxxxx.elb.us-east-1.amazonaws.com",
                "CanonicalHostedZoneId": "XXXXXXXXXXXXXX",
                "CreatedTime": "2018-06-28T14:02:10.158Z",
                "LoadBalancerName": "ex-006-net-lb",
                "Scheme": "internet-facing",
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
                "State": {
                    "Code": "active"
                },
                "Type": "network",
                "AvailabilityZones": [
                    {
                        "ZoneName": "us-east-1a",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx",
                        "LoadBalancerAddresses": [
                            {}
                        ]
                    },
                    {
                        "ZoneName": "us-east-1b",
                        "SubnetId": "subnet-xxxxxxxxxxxxxxxxx",
                        "LoadBalancerAddresses": [
                            {}
                        ]
                    }
                ],
                "IpAddressType": "ipv4"
            }
        ]
    }

Environment variable
~~~~~~~~~~~~~~~~~~~~
Create the following environment variable.

.. code-block::

    export EX006_NET_LB=$(aws elbv2 describe-load-balancers --names ex-006-net-lb --output text --query LoadBalancers[*].LoadBalancerArn)

Sanity check
------------

.. code-block::
    
    echo -e '\n'$EX006_APP_LB'\n'$EX006_NET_LB

Create Target Group for Application Load-balancer
-------------------------------------------------
The first Target Group we are going to create will be used with the Application load-balancer.

Here we will set the protocol to HTTP, since the Application Load-balancer is operating at Layer 7. 

.. code-block::

    aws elbv2 create-target-group --name ex-006-tg-app-lb --protocol HTTP --port 80 --vpc-id $EX006_VPC

Output:

.. code-block::

    {
        "TargetGroups": [
            {
                "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:targetgroup/ex-006-tg-app-lb/xxxxxxxxxxxxxxxx",
                "TargetGroupName": "ex-006-tg-app-lb",
                "Protocol": "HTTP",
                "Port": 80,
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
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

Environment variable
~~~~~~~~~~~~~~~~~~~~
Create the following environment variable.

.. code-block::

    export EX006_APP_TG=$(aws elbv2 describe-target-groups --names ex-006-tg-app-lb --output text --query TargetGroups[*].TargetGroupArn)

Create Target Group for Network Load-balancer
---------------------------------------------
The second Target Group we are going to create will be used with the Network load-balancer.

Here we will set the protocol to TCP, since the Network Load-balancer is operating at Layer 4. 

.. code-block::

    aws elbv2 create-target-group --name ex-006-tg-net-lb --protocol TCP --port 80 --vpc-id $EX006_VPC

Output:

.. code-block::

    {
        "TargetGroups": [
            {
                "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:targetgroup/ex-006-tg-net-lb/xxxxxxxxxxxxxxxx",
                "TargetGroupName": "ex-006-tg-net-lb",
                "Protocol": "TCP",
                "Port": 80,
                "VpcId": "vpc-xxxxxxxxxxxxxxxxx",
                "HealthCheckProtocol": "TCP",
                "HealthCheckPort": "traffic-port",
                "HealthCheckIntervalSeconds": 30,
                "HealthCheckTimeoutSeconds": 10,
                "HealthyThresholdCount": 3,
                "UnhealthyThresholdCount": 3,
                "TargetType": "instance"
            }
        ]
    }


Environment variable
~~~~~~~~~~~~~~~~~~~~
Create the following environment variable.

.. code-block::

    export EX006_NET_TG=$(aws elbv2 describe-target-groups --names ex-006-tg-net-lb --output text --query TargetGroups[*].TargetGroupArn)


Sanity check
------------

.. code-block::
    
    echo -e '\n'$EX006_APP_TG'\n'$EX006_NET_TG

Register Targets
----------------
Targets can be registered to multiple Target Groups.

Application Load-balancer
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws elbv2 register-targets \
        --target-group-arn $EX006_APP_TG \
        --targets Id=$EX006_INST_WEB1 Id=$EX006_INST_WEB2

Network Load-balancer
~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws elbv2 register-targets \
        --target-group-arn $EX006_NET_TG \
        --targets Id=$EX006_INST_WEB1 Id=$EX006_INST_WEB2

Describe Target Group health
----------------------------
Let's take a look at the health of both Target Groups.


Application Load-balancer
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX006_APP_TG

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-xxxxxxxxxxxxxxxxx",
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
                    "Id": "i-xxxxxxxxxxxxxxxxx",
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

Network Load-balancer
~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX006_NET_TG

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-xxxxxxxxxxxxxxxxx",
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
                    "Id": "i-xxxxxxxxxxxxxxxxx",
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

You can see that **'State'** is **'unused'**. We need to create a **Listener** before the Targets can be used.


Create Listener for each Load-balancer
--------------------------------------

Application Load-balancer 
~~~~~~~~~~~~~~~~~~~~~~~~~
Here we set the protocol to HTTP.

.. code-block::

    aws elbv2 create-listener \
        --load-balancer-arn $EX006_APP_LB \
        --protocol HTTP \
        --port 80 \
        --default-actions Type=forward,TargetGroupArn=$EX006_APP_TG

Output:

.. code-block::

    {
        "Listeners": [
            {
                "ListenerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:listener/app/ex-006-app-lb/xxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxx",
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:loadbalancer/app/ex-006-app-lb/xxxxxxxxxxxxxxxx",
                "Port": 80,
                "Protocol": "HTTP",
                "DefaultActions": [
                    {
                        "Type": "forward",
                        "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:targetgroup/ex-006-tg-app-lb/xxxxxxxxxxxxxxxx"
                    }
                ]
            }
        ]
    }


Network Load-balancer 
~~~~~~~~~~~~~~~~~~~~~
Here we set the protocol to TCP.

.. code-block::

    aws elbv2 create-listener \
        --load-balancer-arn $EX006_NET_LB \
        --protocol TCP \
        --port 80 \
        --default-actions Type=forward,TargetGroupArn=$EX006_NET_TG

Output:

.. code-block::

    {
        "Listeners": [
            {
                "ListenerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:listener/net/ex-006-net-lb/xxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxx",
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:loadbalancer/net/ex-006-net-lb/xxxxxxxxxxxxxxxx",
                "Port": 80,
                "Protocol": "TCP",
                "DefaultActions": [
                    {
                        "Type": "forward",
                        "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:targetgroup/ex-006-tg-net-lb/xxxxxxxxxxxxxxxx"
                    }
                ]
            }
        ]
    }

Describe Target Group health
----------------------------
Let's take another look at the health of both Target Groups.


Application Load-balancer
~~~~~~~~~~~~~~~~~~~~~~~~~
Rerun this command until 'State' is 'healthy'.

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX006_APP_TG

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-xxxxxxxxxxxxxxxxx",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            },
            {
                "Target": {
                    "Id": "i-xxxxxxxxxxxxxxxxx",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            }
        ]
    }

Network Load-balancer
~~~~~~~~~~~~~~~~~~~~~
Rerun this command until 'State' is 'healthy'.

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX006_NET_TG

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-xxxxxxxxxxxxxxxxx",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            },
            {
                "Target": {
                    "Id": "i-xxxxxxxxxxxxxxxxx",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            }
        ]
    }

Verify Application Load-balancer
--------------------------------

DNS Name
~~~~~~~~
.. code-block::

    aws elbv2 describe-load-balancers \
      --load-balancer-arns $EX006_APP_LB \
      --output text \
      --query LoadBalancers[*].DNSName

Output:

.. code-block::

    ex-006-app-lb-xxxxxxxxxx.us-east-1.elb.amazonaws.com

Test connectivity
~~~~~~~~~~~~~~~~~
Using 'curl' or your browser test connectivity. Rerun/refresh a few times to make sure you see the host name of both Web Servers.

**Expected result:** Success

.. code-block::

    curl http://ex-006-app-lb-xxxxxxxxxx.us-east-1.elb.amazonaws.com


Verify Network Load-balancer
----------------------------

DNS Name
~~~~~~~~
.. code-block::

    aws elbv2 describe-load-balancers \
      --load-balancer-arns $EX006_NET_LB \
      --output text \
      --query LoadBalancers[*].DNSName

Output:

.. code-block::

    ex-006-net-lb-xxxxxxxxxxxxxxxx.elb.us-east-1.amazonaws.com

Test connectivity
~~~~~~~~~~~~~~~~~
Using 'curl' or your browser test connectivity. Rerun/refresh a few times to make sure you see the host name of both Web Servers.

**Expected result:** Fail

.. code-block::

    curl http://ex-006-net-lb-xxxxxxxxxxxxxxxx.elb.us-east-1.amazonaws.com

    Cntrl-c to kill

Explanation of results
----------------------
The Security Group that is applied to the Application Load-balancer allows HTTP (TCP port 80) from anywhere (0.0.0.0/0) and the Network Load-balancer does use Security Groups, so no issue there. 

.. code-block::

    SecurityGroupLoadBalancer:
      Type: AWS::EC2::SecurityGroup
      Properties: 
        GroupName: sg_loadbalancer_ex006
        GroupDescription: "Security Group for Load balancer."
        SecurityGroupIngress:
          - 
            CidrIp: 0.0.0.0/0
            IpProtocol: tcp
            FromPort: 80
            ToPort: 80
        VpcId: !Ref VPC

The Security Group that is applied to the Web Servers only allows HTTP (TCP port 80) from inside the VPC (10.0.0.0/16).

    The Application Load-balancer changes the source IP of packets it receives to it's private IP address, so those packets are not blocked by the Security Group rule.

    By default, the Network Load-balancer does NOT change the source IP of packets it receives, so those packets are blocked by the Security Group rule.

.. code-block::

    SecurityGroupWebInstances:
      Type: AWS::EC2::SecurityGroup
      Properties: 
        GroupName: sg_webinstances_ex006
        GroupDescription: "Security Group for Web Instances."
        SecurityGroupIngress:
          - 
            CidrIp: 10.0.0.0/16
            IpProtocol: tcp
            FromPort: 80
            ToPort: 80
        VpcId: !Ref VPC

Resolve the issue
-----------------

Add a rule
~~~~~~~~~~
Let's add a rule to security group for the Web Servers that allows HTTP (TCP port 80) from anywhere (0.0.0.0/0)

.. code-block::

 aws ec2 authorize-security-group-ingress \
    --group-id $EX006_SG_WEB \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

Test connectivity
~~~~~~~~~~~~~~~~~
Using 'curl' or your browser test connectivity. Rerun/refresh a few times to make sure you see the host name of both Web Servers.

**Expected result:** Success

.. code-block::

    curl http://ex-006-net-lb-xxxxxxxxxxxxxxxx.elb.us-east-1.amazonaws.com

Cross-zone load balancing
-------------------------
Now let's see which load balancer is doing cross-zone load balancing.

Application Load balancer (ALB)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First, we will use **nslookup** to find the IP address of both nodes.

.. code-block::

    nslookup $(aws elbv2 describe-load-balancers --load-balancer-arns $EX006_APP_LB --output text --query LoadBalancers[*].DNSName)

Output:

.. code-block::

    Non-authoritative answer:
    Name:   ex-006-app-lb-xxxxxxxxx.us-east-1.elb.amazonaws.com
    Address: xxx.xxx.xxx.xxx
    Name:   ex-006-app-lb-xxxxxxxxx.us-east-1.elb.amazonaws.com
    Address: xxx.xxx.xxx.xxx

Next, using 'curl' or your browser test connectivity to each load balancer node. Rerun/refresh a few times.

**Expected result:** You should be able to access both Web Servers through either load balancer node.

.. code-block::

    curl http://xxx.xxx.xxx.xxx

    curl http://xxx.xxx.xxx.xxx

Network Load balancer (NLB)
~~~~~~~~~~~~~~~~~~~~~~~~~~~
First, we will use **nslookup** to find the IP address of both nodes.

.. code-block::

    nslookup $(aws elbv2 describe-load-balancers --load-balancer-arns $EX006_NET_LB --output text --query LoadBalancers[*].DNSName)

Output:

.. code-block::

    Non-authoritative answer:
    Name:   ex-006-net-lb-xxxxxxxxx.us-east-1.elb.amazonaws.com
    Address: xxx.xxx.xxx.xxx
    Name:   ex-006-net-lb-xxxxxxxxx.us-east-1.elb.amazonaws.com
    Address: xxx.xxx.xxx.xxx

Next, using 'curl' or your browser test connectivity to each load balancer node. Rerun/refresh a few times.

**Expected result:** You should only be able to access one Web Server through either load balancer node. (Cross-zone load balancing is disabled by default)

.. code-block::

    curl http://xxx.xxx.xxx.xxx

    curl http://xxx.xxx.xxx.xxx

Enable Cross-zone load balancing on the NLB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws elbv2 modify-load-balancer-attributes \
        --load-balancer-arn $EX006_NET_LB \
        --attributes Key=load_balancing.cross_zone.enabled,Value=true

Output:

.. code-block::

    {
        "Attributes": [
            {
                "Key": "deletion_protection.enabled",
                "Value": "false"
            }
        ]
    }

Describe load balancer attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws elbv2 describe-load-balancer-attributes --load-balancer-arn $EX006_NET_LB

Output:

.. code-block::

    {
        "Attributes": [
            {
                "Key": "load_balancing.cross_zone.enabled",
                "Value": "true"
            },
            {
                "Key": "deletion_protection.enabled",
                "Value": "false"
            }
        ]
    }

Using 'curl' or your browser test connectivity to each load balancer node. Rerun/refresh a few times.

**Expected result:** You should only be able to access one Web Server through either load balancer node. (Cross-zone load balancing is disabled by default)

.. code-block::

    curl http://xxx.xxx.xxx.xxx

    curl http://xxx.xxx.xxx.xxx


Clean up
--------

Delete the Application Load-balancer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deleting a Load-balancer with also delete the associated Target Group.

.. code-block::
    
    aws elbv2 delete-load-balancer --load-balancer-arn $EX006_APP_LB

Delete the Network Load-balancer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deleting a Load-balancer with also delete the associated Target Group.

.. code-block::
    
    aws elbv2 delete-load-balancer --load-balancer-arn $EX006__NET_LB

Delete the Stack
----------------

.. code-block::

    aws cloudformation delete-stack --stack-name ex-006

Check the status
----------------

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

Rerun this command until you get the following response.

Output:

.. code-block::

    An error occurred (ValidationError) when calling the DescribeStacks operation: Stack with id ex-005 does not exist

Summary
-------
- We created an Application Load-balancer.
- We created a Network Load-balancer.
- We created a Target Group for the Application Load-balancer.
- We created a Target Group for the Network Load-balancer.
- We registered the Web Servers with both Target Groups.
- We created a Listener for the Application Load-balancer.
- We created a Listener for the Network Load-balancer.
- We tested connectivity through the Application Load-balancer.
- We tested connectivity through the Network Load-balancer.
- We resolved an issue with connectivity through the Network Load-balancer.

Next steps
----------
In `ex-007 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-007_WorkingEbs.rst>`_, we will become familiar with managing EBS volumes. 
