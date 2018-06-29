ex-003: Testing basic connectivity from the AWS Management Console
==================================================================

Status
------
Version 1.1 (6/29/18)

Dependencies
------------
.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - Depends on exercise(s)
     - ex-001, ex-002
   * - Prerequisite for exercise(s)
     - None

Objectives
----------
- Become familiar with launching and connecting to on-demand Instances.
- Test connectivity for the VPC configuration we created in ex-002.

Expected Costs
--------------
The activities in this exercise may result in charges to your AWS account.

.. list-table::
   :widths: 20, 40, 50
   :header-rows: 0

   * - **Component**
     - **Applicable Costs**
     - **Notes**
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
        + During this exercise there will be short periods of time where an EIP is not associated with a running Instance, so you might incur a very small charge.
   * - Elastic IPs
     - 
        + $0.00 per EIP address remap for the first 100 remaps per month.
        + $0.10 per EIP address remap for additional remaps over 100 per month
     - 
        + During this exercise we will remap an EIP a couple of times.  

Limits
------
The following table shows the default limits for the components utilized in this exercise.

.. list-table::
   :widths: 25, 25
   :header-rows: 0

   * - **Component**
     - **Limit**
   * - Security Groups
     - 500 per VPC
   * - Security Groups per Elastic Network Interface
     - 5
   * - Rules per Security Group
     - 50
   * - On-demand Instances
     - 20 per region
   * - Elastic IP addresses
     - 5 per region

Preparation
-----------
Login to your AWS account and navigate to the AWS Management console.

Create a Security Group
-----------------------
We'll create a Security Group that will be applied to the Instances created later in this exercise.

1. Under the **Services** menu, select **EC2**, under *Compute*.
2. From the navigation pane, under **NETWORK & SECURITY**, select **Security Groups**.
3. Click **Create Security Group**.
4. In the 'Create Security Group' window, enter the following values:

      * Security Group Name: Int2Public.
      * Description: Security Group for Instances.
      * VPC: Select the EX002_VPC.
5. Under **Security Group Rules**, select the **Inbound** tab.
6. Click **Add Rule**.
6. In the Rule definition row, set the following values:

      * Type: SSH (this sets protocol to TCP and port to 22)
      * Source: Anywhere (or My IP)
      * Description: Allow SSH inbound
7. Click **Create**.
   
Launch an Instance
-------------------
1. From the navigation pane, under **INSTANCES**, select **Instances**.
2. Click **Launch Instance**.
3. Under **Step 1: Choose an Amazon Machine Image (AMI)**, in the left pane, check the **Free tier only** and select the **Quick Start** tab.
4. Next to **Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type**, click **select**.
5. Under **Step 2: Choose an Instance**, select **t2.micro**.
6. Click **Next: Configure Instance Details**.
7. Under **Step 3: Configure Instance Details**, set the following values:

      * Network: EX002_VPC
      * Subnet: public
      * Everything else: default
8. Click **Next: Add Storage**
9. Under **Step 4: Add Storage**, At the 'Add Storage' step, make no changes.
10. Click **Next: Add Tags**.
11. Under **Step 5: Add Tags**, click **Add Tag** and enter the following:

      * Key: Name
      * Value: public
12. Click **Next: Configure Security Group**.
13. Under **Step 6: Configure Security Group**, 
14. At the Configure Security Group step, select **Select and existing Security Group**, then select the **Int2Public** security group.

    Its inbound rules, allowing SSH are displayed.
15. Click **Review and Launch**.
16. Under **Step 7: Review Instance Launch**, click **Launch**.
17. At the **Select and existing key pair or create a new key pair** window, select your **Key Pair** and check the **'I acknowledge...'**' box.
18. Click **Launch Instances**.
19. Click **View Instances** to watch the creation status.
      
Launch another Instance
-------------------
1. While stil in the Instances console
2. Click **Launch Instance**.
3. Under **Step 1: Choose an Amazon Machine Image (AMI)**, in the left pane, check the **Free tier only** and select the **Quick Start** tab.
4. Next to **Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type**, click **select**.
5. Under **Step 2: Choose an Instance**, select **t2.micro**.
6. Click **Next: Configure Instance Details**.
7. Under **Step 3: Configure Instance Details**, set the following values:

      * Network: EX002_VPC
      * Subnet: private
      * Everything else: default
8. Click **Next: Add Storage**
9. Under **Step 4: Add Storage**, At the 'Add Storage' step, make no changes.
10. Click **Next: Add Tags**.
11. Under **Step 5: Add Tags**, click **Add Tag** and enter the following:

      * Key: Name
      * Value: private
12. Click **Next: Configure Security Group**.
13. Under **Step 6: Configure Security Group**, 
14. At the Configure Security Group step, select **Select and existing Security Group**, then select the **Int2Public** security group.

    Its inbound rules, allowing SSH are displayed.
15. Click **Review and Launch**.
16. Under **Step 7: Review Instance Launch**, click **Launch**.
17. At the **Select and existing key pair or create a new key pair** window, select your **Key Pair** and check the **'I acknowledge...'**' box.
18. Click **Launch Instances**.
19. Click **View Instances** to watch the creation status.

Once both instances are in the 'running' state, proceed to the next steps


Allocate and associate an Elastic IP
----------------------
In order to connect to our instance, we'll need a public IPv4 address (a.k.a Elastic IP).  First, we'll allocate an IP for our account, then we'll associate it with our 'public' instance.

1. Under the **Services** menu, select **EC2** under *Compute*
2. On the left-side menu, select **Elastic IPs** under NETWORK & SECURITY
3. Click **Allocate new address**, then **Allocate**, then **Close**
4. Select the new Elastic IP from the list and choose **Associate Address** from the 'Actions' menu
5. On the 'Associate Address; step, set the following, click **Associate** and then **Close**
      * Resource type: Instance
      * Instance: 'public'
      * Private IP: <private IP> (10.0.0.x)
6. Notice now that the Elastic IP has additional information regarding the instance and Private IP address
7. Make a note of the Elastic IP address


Test inbound connectivity
-------------------------
Use the following commands to test 'inbound' connectivity to the **public** Instance.
**Expected results:** 'ping' should fail and 'ssh' should succeed.

On your local workstation, open a terminal session or command prompt to run these connectivity tests:
*  If you are using a different Key Pair, then replace 'acpkey1.pem' with your '<your-pem-file>'
*  Replace '<Elastic IP address>' with the actual public IP for the Elastic IP address

.. code-block::

    ping <Elastic IP address>
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<Elastic IP address>

Note: If you are prompted with **"Are you sure you want to continue connecting (yes/no)?"**, that's a good thing! Enter 'y' and you'll be connected.

*So, why did ssh work but ping did not?*
Earlier, we created the Int2Public security group and assigned it to both instances.  This security group included one inbound rule that allowed SSH connections.  Everything else is blocked.  In addition, the public instance is attached to the 'public' subnet, which is associated with the 'public' route table.  The 'public' route table includes a default route that sends all non-local traffic to the Internet Gateway


Test outbound connectivity
--------------------------
While still connect via ssh to the Elastic IP (assigned to the public instance), use the following command to test 'outbound' connectivity from the **public** Instance.

**Expected results:** 'apt update' should succeed.

.. code-block::

    sudo apt update

Type 'exit' to close the ssh session to this instance

*So, why did the apt update work?*  The Int2Public security group has a default Outbound rule that allows all traffic.

Re-associate the Elastic IP
---------------------------
Let's move the Elastic IP to the 'private' instance and see the diferences

1. Under the **Services** menu, select **EC2** under *Compute*
2. On the left-side menu, select **Elastic IPs** under NETWORK & SECURITY
3. Select the Elastic IP from the list and choose **Disassociate Address** from the 'Actions' menu, then click the **Disassociate address** button on the window that appears.
3. Select the Elastic IP from the list and choose **Associate Address** from the 'Actions' menu
5. On the 'Associate Address; step, set the following, click **Associate** and then **Close**
      * Resource type: Instance
      * Instance: 'private'
      * Private IP: <private IP> (10.0.2.x)
6. Notice now that the Elastic IP shows the 10.0.2.x Private IP address
7. Make a note of the Elastic IP address - it should be the same as before since we did not release it


Test inbound connectivity
-------------------------
Use the following commands to test connectivity to the **private** Instance.
**Expected results:** Both 'ping' and 'ssh' should be fail.

On your local workstation, open a terminal session or command prompt to run these connectivity tests:
*  Replace '<Elastic IP address>' with the actual public IP for the Elastic IP address

.. code-block::

    ping <Elastic IP address>
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<Elastic IP address>

*Ok, so why does this instance not connect at all?*
Although this instance is in the same security group with the same rules as the public instance, it is in the 'private' subnet, which is not associated with the 'public' route table.  As a result, there is no route for non-local traffic to reach this instance.


Re-re-associate the Elastic IP
---------------------------
Let's re-associate the Elastic IP back to the 'public' instance so we can connect again.
Use the following awscli command to re-associate the Elastic IP with the **public** Instance.

1. Under the **Services** menu, select **EC2** under *Compute*
2. On the left-side menu, select **Elastic IPs** under NETWORK & SECURITY
3. Select the Elastic IP from the list and choose **Disassociate Address** from the 'Actions' menu, then click the **Disassociate address** button on the window that appears.
3. Select the Elastic IP from the list and choose **Associate Address** from the 'Actions' menu
5. On the 'Associate Address; step, set the following, click **Associate** and then **Close**
      * Resource type: Instance
      * Instance: 'public'
      * Private IP: <private IP> (10.0.0.x)
6. Notice now that the Elastic IP shows the 10.0.0.x Private IP address
7. Make a note of the Elastic IP address - it should be the same as before since we did not release it



Reconnect via SSH
-----------------
Next, we need to reconnect to the public instance, but we also want to reach the private instance.  To reach the private instance, we'll 'hop' from the public instance - that is, we'll ssh from our local workstation to the public instance, then from the public instance to the private instance.  Just like you have to have the key pair on your local workstation in order to connect ssh to the public instance, the same key pair must be present on the public instance in order for it to connect to the private instance.

On your local workstation, open a terminal session or command prompt to run these connectivity tests:
*  If you are using a different Key Pair, then replace 'acpkey1.pem' with your '<your-pem-file>'
*  Replace '<Elastic IP address>' with the actual public IP for the Elastic IP address

.. code-block::

    scp -i acpkey1.pem acpkey1.pem ubuntu@<Elastic IP address>:/home/ubuntu
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<Elastic IP address>

    Do NOT 'exit'
    
On Windows, you may want to use WinSCP to transfer the pem and putty to connect.    

Test inbound connectivity
-----------------------
You should still be connected to the **public** instance via SSH to the Elastic IP.


**Expected results:** 'ping' should fail and 'ssh' should succeed.

.. code-block::

    ping <ip-addr-private-instance>
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<ip-addr-private-instance>

You are now connected to the **private** Instance, through the **public** instance.

Again, the security group is allowing SSH from anywhere and the private instance's route table has a default route for all traffic in our VPC.

Test outbound connectivity
--------------------------
While still in the ssh session on the 'private' instance, use the following command to test oubound connectivity from the Instance in the private Subnet.

**Expected results** 'apt update' should fail.

.. code-block::

    sudo apt update

    Type 'cntrl-c' to kill 'apt'

Type 'exit' twice to close the ssh session for both Instances.

So why did apt update fail?  Once again, the security group would allow the outbound traffic, but the private subnet has no inbound or outbound path to the Internet. In a later exercise, we will create a **NAT Gateway** to allow for outbound connectivity for private Subnet to the Internet.


Add a rule to the Security Group
--------------------------------
Use the following awscli command to create a new rule to the Int2Public security group. This rule enables the icmp protocol from anywhere.

1. Under the **Services** menu, select **EC2** under *Compute*
2. On the left-side menu, select **Security Groups** under NETWORK & SECURITY
3. From the list of security groups, select 'Int2Public'
4. In the bottom part of the page, select the 'Inbound' tab
5. On the 'inbound' tab, click the **Edit** button
6. On the 'Edit inbound rules', click **Add Rule**
7. In the new row, set the following:
      * Type: 'All ICMP - IPv4'  - this sets the protocol to ICP and the port range to 0-65535
      * Source: 'Anywhere'
      * Description: Allow ICMP
8. Click **Save**


Test inbound connectivity
-------------------------
Use the following commands to test connectivity to the **public** Instance.
**Expected results:** Both 'ping' and 'ssh' should be fail.
On your local workstation, open a terminal session or command prompt to run these connectivity tests:

.. code-block::

    ping <Elastic IP address>
    ssh -i acpkey1.pem -o ConnectTimeout=5 ubuntu@<Elastic IP address>

*Ok, so what's different?*
We've updated the security group to allow ICMP (ping)

Test public-to-private connectivity
-----------------------
You should still be connected via ssh to the **public** Instance.

Use the following command to test connectivity to the **private** Instance. 

**Expected results:** 'ping' should now succeed.

.. code-block::

    ping <ip-addr-private-instance>

Type 'exit' to disconnect to close the ssh session.

Clean up - Terminate Instances
------------------------------
1. Under the **Services** menu, select **EC2** under *Compute*
2. On the left-side menu, select **Instances**
3. Select the 'public' and 'private' instances, choose **Instance State | Terminate** from the 'Actions' menu, then **Yes Terminate**

Clean Up - Release Elastic IP
-----------------------------
1. On the left-side menu, select **Elastic IPs** under 'NETWORK & SECURITY'
2. Select the Elastic IP, choose **Release Address** from the 'Action' menu, then **Release**

Clean Up - Delete the Security Group
------------------------------------
1. On the left-side menu, select **Security Groups** under 'NETWORK & SECURITY'
2. Select the **Int2Public** security group, choose **Delete Security Group** from the 'Actions' menu
3. Select the 'EX002_VPC' VPC and choose **Delete VPC** from the 'Actions' menu, then **Yes, Delete**

Clean Up - Delete the VPC
-------------------------
1. Under the **Services** menu, select **VPC** under *Network & Content Delivery*
2. On the left-side menu, select **Your VPCs**
3. Select the **EX002_VPC** VPC, choose **Delete VPC** from the 'Actions' menu, then **Yes, Delete**


Summary
-------
- We created a Security Group.
- We added rules to the Security Group.
- We create two Instances.
- We allocated a Elastic IP.
- We map/re-mapped that Elastic IP to Instances.
- We tested connectivity to/from both the 'public' and 'private' Instances.
- We terminated both Instances, released the Elastic IP, deleted the Security Group and the VPC (and associated components).

**Note: we did NOT delete the Key Pair, keep the '.pem' file safe** 

Next steps
----------
We will recreate the configuration built in ex-002 and ex-003, using CloudFormation, in 
`ex-004 <https://github.com/addr2data/aws-certification-prep/blob/master/exercises/ex-004_GettingStartedCloudFormation.rst>`_
