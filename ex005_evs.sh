#!/bin/bash

##################################
# Public address for Elastic IPs #
##################################
export EX005_IP_PUBLIC=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`FloatingIpAddressInstance`].PhysicalResourceId')
export EX005_IP_NAT=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`FloatingIpAddressNatGateway`].PhysicalResourceId')

#####################################
# InstanceId for 'private' Instance #
#####################################
export EX005_INST_PRIV=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`PrivateInstance`].PhysicalResourceId')

##########################################
# RouteTableId for 'private' Route Table #
##########################################
export EX005_RTB_PRIV=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`RouteTablePrivate`].PhysicalResourceId')

#################################################
# SecurityGroupId for 'endpoint' Security Group #
#################################################
export EX005_SG_ENDPOINT=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`SecurityGroupEndpoint`].PhysicalResourceId')

#############################
# SubnetId for both Subnets #
#############################
export EX005_SUBNET_PUB=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`SubnetPublic`].PhysicalResourceId')
export EX005_SUBNET_PRIV=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`SubnetPrivate`].PhysicalResourceId')

#################
# VpcId for VPC #
#################
export EX005_VPC=$(aws cloudformation describe-stack-resources --stack-name ex-005 --output text --query 'StackResources[?LogicalResourceId==`VPC`].PhysicalResourceId')


echo $EX005_IP_PUBLIC
echo $EX005_IP_NAT
echo $EX005_INST_PRIV
echo $EX005_RTB_PRIV
echo $EX005_SG_ENDPOINT
echo $EX005_SUBNET_PUB
echo $EX005_SUBNET_PRIV
echo $EX005_VPC