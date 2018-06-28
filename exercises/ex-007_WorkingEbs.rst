ex-007: Working with EBS
========================

Status
------
Draft

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
   * - EBS (storage)
     - 
        + gp2: Between $0.10 and $0.19 per GB-month of provisioned storage, depending on your region.
        + io1: Between $0.125 and $0.238 per GB-month of provisioned storage, depending on your region.
        + st1: Between $0.045 and $0.086 per GB-month of provisioned storage, depending on your region.
        + sc1: Between $0.025 and $0.048 per GB-month of provisioned storage, depending on your region.
     -
        + Amazon EBS General Purpose SSD (gp2) volumes
        + Amazon EBS Provisioned IOPS SSD (io1) volumes
        + Amazon EBS Throughput Optimized HDD (st1) volumes
        + Amazon EBS Cold HDD (sc1) volumes
   * - EBS (iops)
     - 
        + io1: Between $0.065 and $0.091 per provisioned IOPS-month
     -
        + Amazon EBS Provisioned IOPS SSD (io1) volumes

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

Create Stack
------------
Use the following awscli command to create a new CloudFormation **'Stack'** based on the template.

Note: If you are using the **'acpkey1'** Key Pair, you can leave off the **'--parameters'** option all together.

.. code-block::

    aws cloudformation create-stack \
        --stack-name ex-007 \
        --template-body file://templates/ex-007_template.yaml \
        --parameters ParameterKey=KeyPairName,ParameterValue=acpkey1

Output:

.. code-block::

    {
        "StackId": "arn:aws:cloudformation:us-east-1:xxxxxxxxxxxx:stack/ex-006/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }




Summary
-------
- To be added

Next steps
----------
To be added, in 
`ex-xxx <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/<name-of-file>>`_

