"""Create a VPC."""

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
import scripts
from ipaddress import IPv4Network, AddressValueError, NetmaskValueError


def create_vpc(cidr, region=None, name=None):
    """Create vpc."""
    try:
        IPv4Network(cidr)
    except (AddressValueError, NetmaskValueError, ValueError) as err:
        raise scripts.ScriptError("{}".format(err))
    if IPv4Network(cidr).prefixlen > 28:
        raise scripts.ScriptError("Prefix length is not valid")

    # Dry run to check permissions
    try:
        ec2 = boto3.client('ec2', region)
        response = ec2.create_vpc(
            CidrBlock=cidr,
            AmazonProvidedIpv6CidrBlock=False,
            DryRun=True,
            InstanceTenancy='default')
    except (EndpointConnectionError) as err:
        raise scripts.ScriptError(str(err))
    except ClientError as err:
        if 'DryRunOperation' not in str(err):
            raise scripts.ScriptError(str(err))

    # Create VPC
    try:
        response = ec2.create_vpc(
            CidrBlock=cidr,
            AmazonProvidedIpv6CidrBlock=False,
            DryRun=False,
            InstanceTenancy='default')
        print("Successfully created VPC.\n"
              "VpcId:        {}\n"
              "CidrBlock:    {}\n"
              "State:        {}".format(response['Vpc']['VpcId'],
                                        response['Vpc']['CidrBlock'],
                                        response['Vpc']['State']))
    except ClientError as err:
        raise scripts.ScriptError(str(err))
    except KeyError as err:
        raise scripts.ScriptError(
            "Expected 'key' not found in response: {}".format(err))

    if name is not None:
        # Set tag called 'Name' to some value.
        # Must be added after 'create' for VPCs.
        try:
            response = ec2.create_tags(
                Resources=[response['Vpc']['VpcId']],
                Tags=[{'Key': 'Name', 'Value': name}])
            print(".....Set tag called 'Name' to {}".format(name))
        except ClientError as err:
            raise scripts.ScriptError(str(err))
