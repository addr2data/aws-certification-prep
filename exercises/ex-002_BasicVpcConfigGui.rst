ex-002: Basic VPC configuration from the AWS Management Console
===============================================================

Status
------
Version 1.0 (6/28/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001
   * - Prerequisite for exercise(s)
     - ex-003

Objectives
----------
- Become familiar with basic VPC configuration (we'll be leaving this configuration in place to support ex-003)

Expected Costs
--------------
The activities in this exercise are NOT expected to result in any charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
   * - VPC (including Subnets, Route Tables and IntenetGateways)
     - 
        + None
     - 
        + AWS does NOT charge for the basic VPC building blocks used in this exercise.
        + AWS does charge for other VPC components, you will use these components in future exercises.   
    
Limits
------
The following table shows the default limits for the components utilized in this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - VPC
     - 5 per region
   * - Route Tables
     - 200 per VPC
   * - Entries per Route Table
     - 50
   * - Subnets
     - 200 per VPC

Preparation
-----------
Logon to the AWS Management console using your AWS account

Create a VPC
------------

- From the left-side *Virtual Private Cloud* menu, select 'Your VPCs'
- Click 'Create VPC'
- On the 'Create VPC' Step, enter the following values, then click 'Yes, Create':
    
    + Name tag: EX002_VPC
    + IPv4 CIDR Block: 10.0.0.0/16
    + IPv6 CIDR Block: 'No IPv6 CIDR Block'
    + Tenancy: Default

Create and attach an Internet Gateway
--------------------------
1. From the left-side *Virtual Private Cloud* menu, select 'Internet Gateways'
2. Click **Create internet gateway**
3. Enter 'InternetGateway' for the Name tag and click **Create**, then click **Close**
4. Notice that the Internet Gateway has been created, but its state is **detached**.  Select 'InternetGateway".
5. From the 'Actions' menu, select 'Attach to VPC'
6. In the 'Attach to VPC' Step, select the EX002_VPC and click **Attach**

At this point, we've created the Internet Gateway, but no traffic is routed to it.

Examine and tag the main Route Table
-------------------------------
1. From the left-side *Virtual Private Cloud* menu, select 'Route Tables'
2. Select the route table entry where the VPC value is "EX002_VPC", it was created automatically for the VPC
3. In the bottom portion of the page, select the 'Routes' tab, you can see a single entry. This entry allows for the routing of local traffic for all Subnets associated with the main Route Table. If you don't explicitly associate a subnet with another Route Table, it is implicitly associated with the main Route Table.
4. Select the 'Tags' tab.  You'll notice there's already a "Name" key with an empty value. Click 'Edit'
5. On the row where the Key is "Name", enter *private* as the Value and click 'Save'

We won't be modifying the main Route Table, just applying a tag to help identify it. We will use it to provide routing for the **'private'** Subnet we will create later. 
Since all subnets are implicitly associated with the main Route Table, it is a good practice to provide reachability to/from the Internet via a separate Route Table. 

Create Public Route Table
---------------------------
1. While still in the Route Tables section of the VPC management console, click **Create Route Table**

2. On the 'Create Route Table' windows, enter the following, then click **Yes Create**:
    - Name tag: public
    - VPC: Select the EX002_VPC VPC
3. Now, you should see at least two route tables associated with the EX002_VPC, one with a Name of 'private' and one with the Name of 'public'.  Select the 'public' route table
4. In the bottom part of the page, select the 'Routes' tab, click **Edit**
5. Click **Add another route**, in the new row, enter the following, then click **Save**:
    - Destination: 0.0.0.0/0
    - Target: select 'InternetGateway'
6. Now, you should have two routes in the public route table, make a note of the route table ID of the 'public' route table

Create Subnets
---------------
In AWS Subnets, the first address is the network address, the last address is the broadcast address and the second through fourth addresses are reserved by AWS

1. From the left-side *Virtual Private Cloud* menu, select 'Subnets'
2. Click **Create subnet**
3. In the 'Create Subnet' step, set the following values, click **Create**, then click **Close**
    - Name tag: public
    - VPC: Select EX002_VPC
    - Availability Zone: No Preference
    - IPv4 CIDR Block: 10.0.0.0/23
4. Click **Create subnet** again
5. In the 'Create Subnet' step, set the following values, click **Create**, then click **Close**
    - Name tag: private
    - VPC: Select EX002_VPC
    - Availability Zone: No Preference
    - IPv4 CIDR Block: 10.0.2.0/23
6. Notice that both subnets use the 'private' route table.  This is because we simply tagged the main route table as 'private' and it encompasses all subnets in the VPC

Associate a Subnet with the Route Table
---------------------------------------
1. While still in the Subnets dashboard, select the 'public' subnet.  That is, the subnet with the Name of 'public'.
2. In the bottom part of the page, select the 'Route Table' tab
3. Click **Edit route table association**
4. On the 'Edit route table association' step, select the route table ID of the 'public' route table, click **save**, then **Close**. Unfortunatly, the Name does not apear on the dropdownlist for selection.  But you'll know you have the right one because there will be a route that uses the internet gateway.
5. Now, you'll see that the 'private' subnet remains associated with the 'private' route table and the 'public' subnet is associated with the 'public' route table.

Summary
-------
- We created a VPC.
- We tagged the main route table 'private'
- We created a second Route Table and Tagged it 'public'
- We created an Internet Gateway.
- We attached the Internet Gateway to the VPC.
- We created a Default Route that targeted the Internet Gateway in the 'public' Route Table.
- We created two Subnets and Tagged them 'public' and 'private', respectively.
- We associated the 'public' Subnet with the 'public' Route Table.

Next steps
----------
We will test that our VPC configuration actually works as expected in 
`ex-003 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-003_TestingBasicConnectivity.rst>`_
