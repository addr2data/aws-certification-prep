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
   * - Application Load-balancing
     - 
        + Between $0.0225 and $0.034 per Application Load Balancer-hour (or partial hour), depending on your region.
        + Between $0.008 and $0.011 per LCU-hour (or partial hour), depending on your region.
     - 
        + It is not expected that this Load balancer will need to be running for more than one hour.
   * - Network Load-balancing
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
During these exercises, we will be using the output of some commands to create environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Template
--------
For our starting configuration, we will create a CloudFormation **Stack** from a Template. Please review **'ex-006_template.yaml'** in the **'templates'** directory.

**Highlights**

    - Two Instances that will act as Web Servers.
    - One Instance that will act a Jumpbox (with public IP)
    - A Subnet for each Web Server (10.0.0.0/24 and 10.0.1.0/24), each in a different Availability Zone 
    - A Subnet for the Jumpbox (10.0.100.0/24)
    - A Security Group for the Jumpbox that allows **SSH** from anywhere (0.0.0.0/0).
    - A Security Group for the Web Servers that allows **SSH** from the Jumpbox Subnet (10.0.100.0/24) and **HTTP** from anywhere in the VPC (10.0.0.0/16)
    - A Security Group for the Load-balancer that allows **HTTP** from anywhere (0.0.0.0/0)

**Notable item**

When creating an Application Load-balancer, you must specify at least two Subnets, from different Availability Zones. In order to achieve this, a couple of CloudFormation built-in functions will be used in the Template

Note: The Network Load-balancer does not have this requirement.

.. code-block::

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

Explanation:

  - **Fn::GetAZs** returns us a list of Availability Zones (AZ) for a Region. **!Ref 'AWS::Region'** says to use the Region that the Stack is being deployed to.
  - **!Select** lets us select the 1st (0) item in the list, for **SubnetWeb1** and the 2nd (1) for **SubnetWeb2**, ensuring that the two Subnets are on different AZs.
  - Every Region has at least two AZs, so this is Template is portable between Regions.

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
Run the following commands to capture the 'PhysicalResourceId' for the applicable components, as environment variables.

.. code-block::

    export EX006_SUBNET_WEB1=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SubnetWeb1`].PhysicalResourceId')

    export EX006_SUBNET_WEB2=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SubnetWeb2`].PhysicalResourceId')

    export EX006_SG_LB=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SecurityGroupLoadBalancer`].PhysicalResourceId')

    export EX006_SG_WEB=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`SecurityGroupWebInstances`].PhysicalResourceId')

    export EX006_VPC=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`VPC`].PhysicalResourceId')

    export EX006_INST_WEB1=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`WebInstance1`].PhysicalResourceId')

    export EX006_INST_WEB2=$(aws cloudformation describe-stack-resources --stack-name ex-006 --output text --query 'StackResources[?LogicalResourceId==`WebInstance2`].PhysicalResourceId')

Sanity check
~~~~~~~~~~~~

.. code-block::
    
    echo -e '\n'$EX006_SUBNET_WEB1'\n'$EX006_SUBNET_WEB2'\n'$EX006_SG_LB'\n'$EX006_VPC'\n'$EX006_INST_WEB1'\n'$EX006_INST_WEB2'\n'$EX006_SG_WEB


Create Application Load-balancer
--------------------------------
Use the following awscli command to create an Application Load-balancer.

.. code-block::

    aws elbv2 create-load-balancer \
        --name ex-006-app-lb \
        --scheme internet-facing \
        --type application \
        --ip-address-type ipv4 \
        --subnets $EX006_SUBNET_WEB1 $EX006_SUBNET_WEB2 \
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
        --subnets $EX006_SUBNET_WEB1 $EX006_SUBNET_WEB2

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

You can see that **'State'** is **'healthy'**.

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
        GroupName: sg_load-balancer_ex006
        GroupDescription: "Security Group for Load balancer in ex-006"
        SecurityGroupIngress:
          - 
            CidrIp: 0.0.0.0/0
            IpProtocol: tcp
            FromPort: 80
            ToPort: 80
        VpcId: !Ref VPC

The Security Group that is applied to the Web Servers only allows HTTP (TCP port 80) from inside the VPC (10.0.0.0/16).

    The Application Load-balancer changes the source IP of packets it receives to it's private IP address, so those packets are not blocked by the Security Group rule.

    The Network Load-balancer does NOT change the source IP of packets it receives, so those packets are blocked by the Security Group rule.

.. code-block::

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
