EXERCISE 002: SETTING UP A VPC
===============================
This exercise covers the basic setup for a VPC.


VPC Limits
----------
.. list-table::
   :widths: 10, 15, 65
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


