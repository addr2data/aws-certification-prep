ex-012: Getting Started with Simple Queue Service
=================================================

Status
------
Draft 0.5 (07/24/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001
   * - Prerequisite for exercise(s)
     - none

Objectives
----------
- To be added

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

Create the first Stack
----------------------
Use the following awscli command to create a new CloudFormation **'Stack'** based on the template.

.. code-block::

    aws cloudformation create-stack \
        --stack-name ex-012a \
        --template-body file://templates/ex-012a_template.yaml

Output:

.. code-block::

    {
        "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-012a/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }

Check the status
----------------
Use the following awscli command to check the **'StackStatus'**.

Rerun this command until **'StackStatus'** is **'CREATE_COMPLETE'**.

.. code-block::

    aws cloudformation describe-stacks --stack-name ex-012a

Output:

.. code-block::

    {
        "Stacks": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-012a/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "StackName": "ex-012a",
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

    export EX012_INST_ID=$(aws cloudformation describe-stack-resources --stack-name ex-012a --output text --query 'StackResources[?LogicalResourceId==`PublicInstance`].PhysicalResourceId')

    export EX012_INST_EIP=$(aws ec2 describe-instances --instance-ids $EX012_INST_ID --output text --query 'Reservations[*].Instances[*].PublicIpAddress')

Sanity check
------------

.. code-block::
    
    echo -e '\n'$EX012_INST_ID'\n'$EX012_INST_EIP

Connect to Instance
-------------------

.. code-block::

    ssh -i acpkey1.pem ubuntu@$EX012_INST_EIP

Configure Instance
------------------

.. code-block::

    sudo apt update
    sudo apt dist-upgrade -y
    sudo apt install python3-pip -y
    pip3 install boto3




Summary
-------
- To be added

Next steps
----------
To be added, in 
`ex-xxx <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/<name-of-file>>`_

