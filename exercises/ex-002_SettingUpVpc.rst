ex-002: Basic configuration your VPC environment
================================================

Introduction
------------
The primary purpose of this exercise is to get you familiar with basic VPC concepts and to configure a VPC for basic IPv4 connectivity.


VPC
---
VPC stands for Virtual Private Cloud and provides significant control over how you configure your AWS cloud network environment.

See the following for detailed information on VPC:
https://aws.amazon.com/vpc/


Default VPC
-----------
Even is you have just created your AWS account and haven't configured anything (other than the IAM user account you created in ex-001), you will still have a default VPC.

Let's take a look at the default VPC with the **describe-vpcs** command and using the **'--filter'** option to select only the default VPC.  

.. code-block::
    
    aws ec2 describe-vpcs --filter Name=isDefault,Values=true

  


VPC Limits
----------
.. list-table::
   :widths: 20, 20, 40
   :header-rows: 1

   * - Resource
     - Default limit
     - Comments
   * - VPCs per region
     - 5
     - The limit for internet gateways per region is directly correlated to this one. Increasing this limit increases the limit on internet gateways per region by the same amount. The number of VPCs in the region multiplied by the number of security groups per VPC cannot exceed 5000.
   * - Subnets per VPC
     - 200
     - 
   * - IPv4 CIDR blocks per VPC
     - 5
     - This limit is made up of your primary CIDR block plus 4 secondary CIDR blocks.
   * - IPv6 CIDR blocks per VPC
     - 1
     - This limit cannot be increased.

*Note: These limits are valid as of 06/13/18. Please you the following link to see the most up to data limits*
https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Appendix_Limits.html

