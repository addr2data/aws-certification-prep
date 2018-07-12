ex-011: Getting started with Auto Scaling
=========================================

Status
------
Draft

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - to be added or none
   * - Prerequisite for exercise(s)
     - to be added or none

Objectives
----------
- Explore **Fleet Management** by **Auto Scaling** EC2 instances.

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
   * - To be added
     - 
        + To be added
     -
        + To be added

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

Create network Stack
--------------------
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


Create application Stack
------------------------
Use the following awscli command to create a new CloudFormation **'Stack'** based on the template.

Note: If you are using the **'acpkey1'** Key Pair, you can leave off the **'--parameters'** option all together.

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

Review the Stack details
------------------------
Use the following awscli command to display the **'LogicalResourceId'** and **'PhysicalResourceId'** for all the components in the **Stack**

Notice the format of this portion of the query string **'{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'**, it adds a header to each column.** 

.. code-block::

    aws cloudformation describe-stack-resources \
        --stack-name ex-011b \
        --output table \
        --query 'StackResources[*].{"Logical Resource Id": LogicalResourceId,"Physical Resource Id": PhysicalResourceId}'

Output:

.. code-block::

    ----------------------------------------------------------------------------------------------------------------------------------------------
    |                                                           DescribeStackResources                                                           |
    +----------------------+---------------------------------------------------------------------------------------------------------------------+
    |  Logical Resource Id |                                                Physical Resource Id                                                 |
    +----------------------+---------------------------------------------------------------------------------------------------------------------+
    |  AppLoadBalancer     |  arn:aws:elasticloadbalancing:us-east-1:926075045128:loadbalancer/app/elb-app-ex011/49242b54aff9c5d7                |
    |  LaunchTemplate      |  lt-08c8daf3c20dda004                                                                                               |
    |  WebServerListener   |  arn:aws:elasticloadbalancing:us-east-1:926075045128:listener/app/elb-app-ex011/49242b54aff9c5d7/3229575d2db3c508   |
    |  WebServerTargetGroup|  arn:aws:elasticloadbalancing:us-east-1:926075045128:targetgroup/ex-011-tg-app-lb/87b1fd3363f55470                  |
    +----------------------+---------------------------------------------------------------------------------------------------------------------+





Environment variable
~~~~~~~~~~~~~~~~~~~~
Create the following environment variable.

.. code-block::

    export EX011_WEB_LB=$(aws cloudformation describe-stack-resources --stack-name ex-011b --output text --query 'StackResources[?LogicalResourceId==`AppLoadBalancer`].PhysicalResourceId')

    export EX011_WEB_TG=$(aws cloudformation describe-stack-resources --stack-name ex-011b --output text --query 'StackResources[?LogicalResourceId==`WebServerTargetGroup`].PhysicalResourceId')

    export EX011_WEB_LIS=$(aws cloudformation describe-stack-resources --stack-name ex-011b --output text --query 'StackResources[?LogicalResourceId==`WebServerListener`].PhysicalResourceId')

    export EX011_WEB_LTEMP=$(aws cloudformation describe-stack-resources --stack-name ex-011b --output text --query 'StackResources[?LogicalResourceId==`LaunchTemplate`].PhysicalResourceId')

Sanity check
------------

.. code-block::
    
    echo -e '\n'$EX011_WEB_LB'\n'$EX011_WEB_TG'\n'$EX011_WEB_LIS'\n'$EX011_WEB_LTEMP


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
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:loadbalancer/app/elb-app-ex011/49242b54aff9c5d7",
                "DNSName": "elb-app-ex011-1978133642.us-east-1.elb.amazonaws.com",
                "CanonicalHostedZoneId": "Z35SXDOTRQ7X7K",
                "CreatedTime": "2018-07-10T17:03:19.470Z",
                "LoadBalancerName": "elb-app-ex011",
                "Scheme": "internet-facing",
                "VpcId": "vpc-0a2153af261fac0e5",
                "State": {
                    "Code": "active"
                },
                "Type": "application",
                "AvailabilityZones": [
                    {
                        "ZoneName": "us-east-1a",
                        "SubnetId": "subnet-0111ef965b30b7104"
                    },
                    {
                        "ZoneName": "us-east-1b",
                        "SubnetId": "subnet-0fc5ae8b83f219d32"
                    }
                ],
                "SecurityGroups": [
                    "sg-00f7a265bda667453"
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

Check Listener status
---------------------

.. code-block::

     aws elbv2 describe-listeners --listener-arns $EX011_WEB_LIS

Output:

.. code-block::

    {
        "Listeners": [
            {
                "ListenerArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:listener/app/elb-app-ex011/49242b54aff9c5d7/3229575d2db3c508",
                "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:loadbalancer/app/elb-app-ex011/49242b54aff9c5d7",
                "Port": 80,
                "Protocol": "HTTP",
                "DefaultActions": [
                    {
                        "Type": "forward",
                        "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:926075045128:targetgroup/ex-011-tg-app-lb/87b1fd3363f55470"
                    }
                ]
            }
        ]
    }


export EX011_PRI_SUBNET1=$(aws cloudformation list-exports --query 'Exports[?Name==`ex-011a-SubnetPrivate1`].Value' --output text)

export EX011_PRI_SUBNET2=$(aws cloudformation list-exports --query 'Exports[?Name==`ex-011a-SubnetPrivate2`].Value' --output text)

echo -e '\n'$EX011_PRI_SUBNET1'\n'$EX011_PRI_SUBNET2

export SUBNETS=$EX011_PRI_SUBNET1','$EX011_PRI_SUBNET2


Create Auto Scaling Group
-------------------------

.. code-block::

    aws autoscaling create-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --launch-template LaunchTemplateId=$EX011_WEB_LTEMP \
        --min-size 2 \
        --max-size 2 \
        --target-group-arns $EX011_WEB_TG \
        --health-check-type ELB \
        --health-check-grace-period 300 \
        --vpc-zone-identifier $SUBNETS


Modify Auto Scaling Group
-------------------------

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --max-size 4 

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --min-size 4 

.. code-block::

    aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names ex-011-asg


Modify Auto Scaling Group
-------------------------

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --min-size 2 

.. code-block::

    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name ex-011-asg \
        --max-size 2 


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

    curl http://elb-app-ex011-1384793920.us-east-1.elb.amazonaws.com

.. code-block::

    aws autoscaling create-auto-scaling-group \
        --auto-scaling-group-name ex-011_asg \
        --instance-id $EX011_INST_WEB1 \
        --min-size 2 --max-size 2


.. code-block::

    aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names ex-011_asg 

Output:

.. code-block::

    {
        "AutoScalingGroups": [
            {
                "AutoScalingGroupName": "ex-011_asg",
                "AutoScalingGroupARN": "arn:aws:autoscaling:us-east-1:926075045128:autoScalingGroup:c090af35-5286-418b-acba-5d1ea2d0a2b1:autoScalingGroupName/ex-011_asg",
                "LaunchConfigurationName": "ex-011_asg",
                "MinSize": 2,
                "MaxSize": 2,
                "DesiredCapacity": 2,
                "DefaultCooldown": 300,
                "AvailabilityZones": [
                    "us-east-1b"
                ],
                "LoadBalancerNames": [],
                "TargetGroupARNs": [],
                "HealthCheckType": "EC2",
                "HealthCheckGracePeriod": 0,
                "Instances": [
                    {
                        "InstanceId": "i-04030facca4770151",
                        "AvailabilityZone": "us-east-1b",
                        "LifecycleState": "InService",
                        "HealthStatus": "Healthy",
                        "LaunchConfigurationName": "ex-011_asg",
                        "ProtectedFromScaleIn": false
                    },
                    {
                        "InstanceId": "i-0d9056944b03f5aad",
                        "AvailabilityZone": "us-east-1b",
                        "LifecycleState": "InService",
                        "HealthStatus": "Healthy",
                        "LaunchConfigurationName": "ex-011_asg",
                        "ProtectedFromScaleIn": false
                    }
                ],
                "CreatedTime": "2018-07-10T02:37:33.399Z",
                "SuspendedProcesses": [],
                "VPCZoneIdentifier": "subnet-0cdeb38c31c380beb",
                "EnabledMetrics": [],
                "Tags": [],
                "TerminationPolicies": [
                    "Default"
                ],
                "NewInstancesProtectedFromScaleIn": false,
                "ServiceLinkedRoleARN": "arn:aws:iam::926075045128:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"
            }
        ]
    }

Summary
-------
- To be added

Next steps
----------
To be added.

