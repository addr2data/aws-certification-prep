ex-011: Getting started with Auto Scaling
=========================================

Status
------
Version 0.8 (7/14/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001
   * - Prerequisite for exercise(s)
     - 

Objectives
----------
- Explore **Fleet Management** by using **Auto Scale** to deploy/terminate EC2 instances.

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
        + They will be deployed using Auto Deploy. 
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
        + It will be deployed as part of a CloudFormation Stack.
        + It should not need to run for more than a hour or so.
   * - Auto Scale
     - 
        + None (AWS does not charge for Auto Scale)
     - 
        + We will configure Auto Scale manually using the awscli. 
   * - Data Transfer
     -
        + $0.00 per GB - Data Transfer IN to Amazon EC2 from Internet
        + $0.00 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(up to 1 GB)**
        + $0.09 per GB per month - Data Transfer OUT of Amazon EC2 to Internet **(next 9.999 TB)**
     - 
        + We also need to consider Data Transfer charges when using either the Application Load balancers.

Limits
------
The following table shows the default limits for the components utilized in this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - To be added
     - To be added

Environment variables
---------------------
During these exercises, we will be using the output of some commands to create environment variables. This will help simplify the syntax subsequent commands.

In some places, we will do this manually, because we want to show the the full output of the command. In other places, we will use the **'--query'** and **'--output'** options available in the awscli command to filter the output directly into a variable.

Setting environment variables may be different on different OSs. Please refer to the documentation for your OS.

Diagram
-------
In this exercise, we will be building the following configuration.

.. image:: https://github.com/addr2data/aws-certification-prep/blob/master/images/ex-011.png

Template
--------
For our starting configuration, we will create two CloudFormation **Stacks** from Template. Please review **'ex-011a_template.yaml'** and **'ex-011b_template.yaml'** in the **'templates'** directory.

We are using two templates in order to introduce an additional capability (export/import) available in CloudFormation Templates.

**Highlights**

    - Two **public** Subnets (10.0.0.0/24 and 10.0.1.0/24). Each in a different Availability Zone.
    - Two **private** Subnets (10.0.128.0/24 and 10.0.129.0/24). Each in a different Availability Zone.
    - An Internet Gateway to allow Internet access to/from the public Subnets.
    - A NAT Gateway to allow Internet access from the private Subnets.
    - A Security Group for the Web Servers that allows **HTTP** from anywhere in the VPC (10.0.0.0/16)
    - A Security Group for the Load-balancer that allows **HTTP** from anywhere (0.0.0.0/0)
    - A Launch Template for use with Auto Scale.
    - An Application Load balancer, plus an associated Target Group and Listener.

**Notable item**

In Template **ex-011a_template.yaml**, we will define some **Outputs**. After we deploy the first stack using this Template, these **Outputs** will available for import by Template **ex-011b_template.yaml**

.. code-block::

    Outputs:
      VPC:
        Value: !Ref VPC
        Export:
          Name: !Sub '${AWS::StackName}-VPC'
      SecurityGroupWebInstances:
        Value: !Ref SecurityGroupWebInstances
        Export:
          Name: !Sub '${AWS::StackName}-SecurityGroupWebInstances'
      SecurityGroupLoadBalancer:
        Value: !Ref SecurityGroupLoadBalancer
        Export:
          Name: !Sub '${AWS::StackName}-SecurityGroupLoadBalancer'
      SubnetPublic1:
        Value: !Ref SubnetPublic1
        Export:
          Name: !Sub '${AWS::StackName}-SubnetPublic1'
      SubnetPublic2:
        Value: !Ref SubnetPublic2
        Export:
          Name: !Sub '${AWS::StackName}-SubnetPublic2'
      SubnetPrivate1:
        Value: !Ref SubnetPrivate1
        Export:
          Name: !Sub '${AWS::StackName}-SubnetPrivate1'
      SubnetPrivate2:
        Value: !Ref SubnetPrivate2
        Export:
          Name: !Sub '${AWS::StackName}-SubnetPrivate2'

**Notable item**

In Template **ex-011b_template.yaml**, we create a **Launch Template** that will be used by Auto Scale to launch new Instances.

.. code-block::

    Resources:
      LaunchTemplate:
        Type: "AWS::EC2::LaunchTemplate"
        Properties:
          LaunchTemplateName: launch_template_ex011
          LaunchTemplateData:
            ImageId: !FindInMap [RegionMap, !Ref "AWS::Region", 64]
            InstanceType: t2.micro
            KeyName: !Ref KeyPairName
            SecurityGroupIds: 
              - Fn::ImportValue:
                  !Sub '${StackName}-SecurityGroupWebInstances'
            UserData: !Base64
              Ref: UserData

**Notable item**

In Template **ex-011b_template.yaml**, we create a Application Load balancer, a Target Group and a Listener.

.. code-block::

    Resources:
      AppLoadBalancer:
        Type: "AWS::ElasticLoadBalancingV2::LoadBalancer"
        Properties:
          Name: elb-app-ex011
          Scheme: internet-facing
          SecurityGroups:
            - Fn::ImportValue:
                !Sub '${StackName}-SecurityGroupLoadBalancer'
          Subnets:
            - Fn::ImportValue:
                !Sub '${StackName}-SubnetPublic1'
            - Fn::ImportValue:
                !Sub '${StackName}-SubnetPublic2'
          Type: application
          IpAddressType: ipv4
      WebServerTargetGroup:
        Type: "AWS::ElasticLoadBalancingV2::TargetGroup"
        Properties:
          Name: ex-011-tg-app-lb
          Port: 80
          Protocol: HTTP
          TargetType: instance
          VpcId:
            Fn::ImportValue:
                !Sub '${StackName}-VPC'
      WebServerListener:
        Type: "AWS::ElasticLoadBalancingV2::Listener"
        Properties: 
          DefaultActions:
            -
              TargetGroupArn: !Ref WebServerTargetGroup
              Type: forward
          LoadBalancerArn: !Ref AppLoadBalancer
          Port: 80
          Protocol: HTTP
        DependsOn:
          - AppLoadBalancer
          - WebServerTargetGroup


Create the first Stack
----------------------
Use the following awscli command to create a new CloudFormation **'Stack'** based on the template.

.. code-block::

    aws cloudformation create-stack \
        --stack-name ex-011a \
        --template-body file://templates/ex-011a_template.yaml

Output:

.. code-block::

    {
        "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-011a/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }

Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this command until **'StackStatus'** is **'CREATE_COMPLETE'**.

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-011a

Output:

.. code-block::

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-011a/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "StackName": "ex-011a",
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

Once you reach **'CREATE_COMPLETE'**, you should also be able to see the **Outputs** that we defined in the Template.

Output:

.. code-block::

    "Outputs": [
                    {
                        "OutputKey": "SubnetPrivate1",
                        "OutputValue": "subnet-xxxxxxxxxxxxxxxxx",
                        "ExportName": "ex-011a-SubnetPrivate1"
                    },
                    {
                        "OutputKey": "SubnetPrivate2",
                        "OutputValue": "subnet-xxxxxxxxxxxxxxxxx",
                        "ExportName": "ex-011a-SubnetPrivate2"
                    },
                    {
                        "OutputKey": "VPC",
                        "OutputValue": "vpc-xxxxxxxxxxxxxxxxx",
                        "ExportName": "ex-011a-VPC"
                    },
                    {
                        "OutputKey": "SecurityGroupLoadBalancer",
                        "OutputValue": "sg-xxxxxxxxxxxxxxxxx",
                        "ExportName": "ex-011a-SecurityGroupLoadBalancer"
                    },
                    {
                        "OutputKey": "SecurityGroupWebInstances",
                        "OutputValue": "sg-xxxxxxxxxxxxxxxxx",
                        "ExportName": "ex-011a-SecurityGroupWebInstances"
                    },
                    {
                        "OutputKey": "SubnetPublic1",
                        "OutputValue": "subnet-xxxxxxxxxxxxxxxxx",
                        "ExportName": "ex-011a-SubnetPublic1"
                    },
                    {
                        "OutputKey": "SubnetPublic2",
                        "OutputValue": "subnet-xxxxxxxxxxxxxxxxx",
                        "ExportName": "ex-011a-SubnetPublic2"
                    }
                ],

Create the second Stack
------------------------
Use the following awscli command to create a new CloudFormation **'Stack'** based on the template.

Notice we are using the parameters option to pass in the name of the first stack.

.. code-block::

    aws cloudformation create-stack \
        --stack-name ex-011b \
        --template-body file://templates/ex-011b_template.yaml \
        --parameters ParameterKey=StackName,ParameterValue=ex-011a

Output:

.. code-block::

    {
        "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-011b/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }


Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this command until **'StackStatus'** is **'CREATE_COMPLETE'**.

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-011b

Output:

.. code-block::

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-011b/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "StackName": "ex-011b",
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

Environment variable
~~~~~~~~~~~~~~~~~~~~
Create the following environment variable.

.. code-block::

    export EX011_WEB_LB=$(aws cloudformation describe-stack-resources --stack-name ex-011b --output text --query 'StackResources[?LogicalResourceId==`AppLoadBalancer`].PhysicalResourceId')

    export EX011_WEB_TG=$(aws cloudformation describe-stack-resources --stack-name ex-011b --output text --query 'StackResources[?LogicalResourceId==`WebServerTargetGroup`].PhysicalResourceId')

    export EX011_WEB_LIS=$(aws cloudformation describe-stack-resources --stack-name ex-011b --output text --query 'StackResources[?LogicalResourceId==`WebServerListener`].PhysicalResourceId')

    export EX011_WEB_LTEMP=$(aws cloudformation describe-stack-resources --stack-name ex-011b --output text --query 'StackResources[?LogicalResourceId==`LaunchTemplate`].PhysicalResourceId')

    export EX011_PRI_SUBNET1=$(aws cloudformation list-exports --query 'Exports[?Name==`ex-011a-SubnetPrivate1`].Value' --output text)

    export EX011_PRI_SUBNET2=$(aws cloudformation list-exports --query 'Exports[?Name==`ex-011a-SubnetPrivate2`].Value' --output text)

Sanity check
------------

.. code-block::
    
    echo -e '\n'$EX011_WEB_LB'\n'$EX011_WEB_TG'\n'$EX011_WEB_LIS'\n'$EX011_WEB_LTEMP'\n'$EX011_PRI_SUBNET1'\n'$EX011_PRI_SUBNET2


Check Load-balancer status
--------------------------
Use the following awscli command to check the **'State:Code'** of the Load-balancer.

Rerun this command until **'State:Code'** is **'active'**.

.. code-block::

    aws elbv2 describe-load-balancers --load-balancer-arns $EX011_WEB_LB

Output:

.. code-block::

    {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:loadbalancer/app/elb-app-ex011/xxxxxxxxxxxxxxxx",
                "DNSName": "elb-app-ex011-xxxxxxxxxx.us-east-1.elb.amazonaws.com",
                "CanonicalHostedZoneId": "XXXXXXXXXXXXXX",
                "CreatedTime": "2018-07-10T17:03:19.470Z",
                "LoadBalancerName": "elb-app-ex011",
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

Check Target Group status
--------------------------

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX011_WEB_TG

Output:

.. code-block::

    {
        "TargetHealthDescriptions": []
    }

Notice that the Target Group is empty. Instances will be added to the Target Group by Auto Scale.

Check Listener status
---------------------

.. code-block::

     aws elbv2 describe-listeners --listener-arns $EX011_WEB_LIS

Output:

.. code-block::

    {
        "Listeners": [
            {
                "ListenerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:listener/app/elb-app-ex011/xxxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxx",
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:loadbalancer/app/elb-app-ex011/xxxxxxxxxxxxxxxx",
                "Port": 80,
                "Protocol": "HTTP",
                "DefaultActions": [
                    {
                        "Type": "forward",
                        "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:targetgroup/ex-011-tg-app-lb/xxxxxxxxxxxxxxxx"
                    }
                ]
            }
        ]
    }

Create Auto Scaling Group
-------------------------
First, we need to be able to pass the Subnets that will be leveraged by the Auto Scale group as a string, so we will create a new environment variable that meets are needs.

.. code-block::

    export EX011_PRI_SUBNETS=$EX011_PRI_SUBNET1','$EX011_PRI_SUBNET2
    echo $EX011_PRI_SUBNETS

Now we create the Auto Scaling group.

.. code-block::

    aws autoscaling create-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --launch-template LaunchTemplateId=$EX011_WEB_LTEMP \
        --min-size 2 \
        --max-size 2 \
        --target-group-arns $EX011_WEB_TG \
        --health-check-type ELB \
        --health-check-grace-period 300 \
        --vpc-zone-identifier $EX011_PRI_SUBNETS

Additional information for the above parameters:

.. list-table::
   :widths: 50, 50
   :header-rows: 0

   * - **Parameter**
     - **Description**
   * - '--auto-scaling-group-name ex-011-asg '
     - Specifies a name for the Auto Scaling group.
   * - '--launch-template LaunchTemplateId=$EX011_WEB_LTEMP'
     - 
   * - '--min-size 2'
     - 
   * - '--max-size 2'
     - 
   * - '--target-group-arns $EX011_WEB_TG'
     - 
   * - '--health-check-type ELB'
     - 
   * - '--health-check-grace-period 300'
     - 
   * - '--vpc-zone-identifier $EX011_PRI_SUBNETS'
     - 

Check the status
----------------

.. code-block::

    aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names ex-011-asg

Output:

.. code-block::

    {
        "AutoScalingGroups": [
            {
                "AutoScalingGroupName": "ex-011-asg",
                "AutoScalingGroupARN": "arn:aws:autoscaling:us-east-1:xxxxxxxxxxxx:autoScalingGroup:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:autoScalingGroupName/ex-011-asg",
                "LaunchTemplate": {
                    "LaunchTemplateId": "lt-xxxxxxxxxxxxxxxxx",
                    "LaunchTemplateName": "launch_template_ex011"
                },
                "MinSize": 2,
                "MaxSize": 2,
                "DesiredCapacity": 2,
                "DefaultCooldown": 300,
                "AvailabilityZones": [
                    "us-east-1a",
                    "us-east-1b"
                ],
                "LoadBalancerNames": [],
                "TargetGroupARNs": [
                    "arn:aws:elasticloadbalancing:us-east-1:xxxxxxxxxxxx:targetgroup/ex-011-tg-app-lb/xxxxxxxxxxxxxxxx"
                ],
                "HealthCheckType": "ELB",
                "HealthCheckGracePeriod": 300,
                "Instances": [],
                "CreatedTime": "2018-07-13T16:50:11.108Z",
                "SuspendedProcesses": [],
                "VPCZoneIdentifier": "subnet-xxxxxxxxxxxxxxxxx,subnet-xxxxxxxxxxxxxxxxx",
                "EnabledMetrics": [],
                "Tags": [],
                "TerminationPolicies": [
                    "Default"
                ],
                "NewInstancesProtectedFromScaleIn": false,
                "ServiceLinkedRoleARN": "arn:aws:iam::xxxxxxxxxxxx:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"
            }
        ]
    }

Describe Target Group health
----------------------------

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX011_WEB_TG

    Rerun this command until 'State' is 'healthy'.

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-08063fc4fba5e79f2",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "initial",
                    "Reason": "Elb.RegistrationInProgress",
                    "Description": "Target registration is in progress"
                }
            },
            {
                "Target": {
                    "Id": "i-056bbe9be8a44ea8e",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "initial",
                    "Reason": "Elb.RegistrationInProgress",
                    "Description": "Target registration is in progress"
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
      --load-balancer-arns $EX011_WEB_LB \
      --output text \
      --query LoadBalancers[*].DNSName

Output:

.. code-block::

    elb-app-ex011-xxxxxxxxxx.us-east-1.elb.amazonaws.com

Test connectivity
~~~~~~~~~~~~~~~~~
Using 'curl' or your browser test connectivity. Rerun/refresh a few times to make sure you see the host name of both Web Servers.

**Expected result:** Success

.. code-block::

    curl http://ex-006-app-lb-xxxxxxxxxx.us-east-1.elb.amazonaws.com


Expand Auto Scaling Group
-------------------------

Max Size
~~~~~~~~
First, we will increase the max size of the auto scaling group.

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --max-size 4 

Min Size
~~~~~~~~
Next, we will increase the min size. This will trigger Auto Scaling to deploy more Instances.

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --min-size 4 

Describe Target Group health
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX011_WEB_TG

    Rerun this command until you see the new targets and they reach a 'State' of 'healthy'.

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-0468a03221b50a9b2",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "initial",
                    "Reason": "Elb.RegistrationInProgress",
                    "Description": "Target registration is in progress"
                }
            },
            {
                "Target": {
                    "Id": "i-0f84e9f2f965b7ae1",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "initial",
                    "Reason": "Elb.RegistrationInProgress",
                    "Description": "Target registration is in progress"
                }
            },
            {
                "Target": {
                    "Id": "i-056bbe9be8a44ea8e",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            },
            {
                "Target": {
                    "Id": "i-08063fc4fba5e79f2",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            }
        ]
    }

Re-verify Application Load-balancer
-----------------------------------

DNS Name
~~~~~~~~
.. code-block::

    aws elbv2 describe-load-balancers \
      --load-balancer-arns $EX011_WEB_LB \
      --output text \
      --query LoadBalancers[*].DNSName

Output:

.. code-block::

    elb-app-ex011-xxxxxxxxxx.us-east-1.elb.amazonaws.com

Test connectivity
~~~~~~~~~~~~~~~~~
Using 'curl' or your browser test connectivity. Rerun/refresh a few times to make sure you see the host name of both Web Servers.

**Expected result:** Success

.. code-block::

    curl http://ex-006-app-lb-xxxxxxxxxx.us-east-1.elb.amazonaws.com

Reduce Auto Scaling Group
-------------------------

Min Size
~~~~~~~~
First, we will increase the max size of the auto scaling group.

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --min-size 2 

Min Size
~~~~~~~~
Next, we will increase the min size. This will trigger Auto Scaling to deploy more Instances.

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --max-size 2 

Describe Target Group health
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX011_WEB_TG

    Rerun this command until you two of the targets have completed draining and only two healthy' targets remain.

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-0468a03221b50a9b2",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            },
            {
                "Target": {
                    "Id": "i-0f84e9f2f965b7ae1",
                    "Port": 80
                },
                "HealthCheckPort": "80",
                "TargetHealth": {
                    "State": "healthy"
                }
            },
            {
                "Target": {
                    "Id": "i-056bbe9be8a44ea8e",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "draining",
                    "Reason": "Target.DeregistrationInProgress",
                    "Description": "Target deregistration is in progress"
                }
            },
            {
                "Target": {
                    "Id": "i-08063fc4fba5e79f2",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "draining",
                    "Reason": "Target.DeregistrationInProgress",
                    "Description": "Target deregistration is in progress"
                }
            }
        ]
    }

Empty Auto Scaling Group
------------------------

Min Size
~~~~~~~~
First, we will increase the max size of the auto scaling group.

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --min-size 0 

Max Size
~~~~~~~~
Next, we will increase the min size. This will trigger Auto Scaling to deploy more Instances.

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --max-size 0

Describe Target Group health
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Rerun this command until all the targets have completed draining and the Target Group is empty

.. code-block::

    aws elbv2 describe-target-health --target-group-arn $EX011_WEB_TG

Output:

.. code-block::

    {
        "TargetHealthDescriptions": [
            {
                "Target": {
                    "Id": "i-0468a03221b50a9b2",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "draining",
                    "Reason": "Target.DeregistrationInProgress",
                    "Description": "Target deregistration is in progress"
                }
            },
            {
                "Target": {
                    "Id": "i-0f84e9f2f965b7ae1",
                    "Port": 80
                },
                "TargetHealth": {
                    "State": "draining",
                    "Reason": "Target.DeregistrationInProgress",
                    "Description": "Target deregistration is in progress"
                }
            }
        ]
    }

Cleanup
-------

Delete Auto Scaling Group
~~~~~~~~~~~~~~~~~~~~~~~~~
Rerun the following command until it lets you delete the group. 

.. code-block::

    aws autoscaling delete-auto-scaling-group --auto-scaling-group-name ex-011-asg


Delete the second Stack
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws cloudformation delete-stack --stack-name ex-011b 


Check the status
~~~~~~~~~~~~~~~~
Rerun the following command until you check the error below. 

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-011b 

Output:

.. code-block::

    An error occurred (ValidationError) when calling the DescribeStacks operation: Stack with id ex-011b does not exist

Delete the first Stack
~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    aws cloudformation delete-stack --stack-name ex-011a 

Check the status
~~~~~~~~~~~~~~~~
Rerun the following command until you check the error below. 

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-011a

Output:

.. code-block::

    An error occurred (ValidationError) when calling the DescribeStacks operation: Stack with id ex-011a does not exist

Summary
-------
- To be added

Next steps
----------
To be added.

