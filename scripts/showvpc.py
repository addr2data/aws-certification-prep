"""Show VPC data."""

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
import scripts


def show_vpc(region=None, vpc_id=None):
    """Show vpc data."""
    # Dry run to check permissions
    try:
        ec2 = boto3.client('ec2', region)
        ec2.describe_vpcs(DryRun=True)
    except (EndpointConnectionError) as err:
        raise scripts.ScriptError(str(err))
    except ClientError as err:
        if 'DryRunOperation' not in str(err):
            raise scripts.ScriptError(str(err))

    # Show vpc data
    try:
        all_vpcs = ec2.describe_vpcs()['Vpcs']
        print("Name                     "
              "VpcId                         "
              "CidrBlock           "
              "State          "
              "IsDefault ")
        print("----                     "
              "-----                         "
              "---------           "
              "-----          "
              "--------- ")
        for vpc in all_vpcs:
            if vpc_id is None or vpc['VpcId'] == vpc_id:
                vpc_name = " "
                if 'Tags' in vpc.keys():
                    for tag in vpc['Tags']:
                        if tag['Key'] == 'Name':
                            vpc_name = tag['Value']
                print("{:25}{:30}{:20}{:15}{:10}".format(
                    vpc_name, vpc['VpcId'], vpc['CidrBlock'],
                    vpc['State'], str(vpc['IsDefault'])))
    except ClientError as err:
        raise scripts.ScriptError(str(err))
    except KeyError as err:
        raise scripts.ScriptError(
            "Expected 'key' not found in response: {}".format(err))
