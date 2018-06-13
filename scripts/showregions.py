"""Show regions and availability zones."""

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
import scripts


def show_regions(avail_zones=False):
    """Show region and availability zone data."""
    # Dry run to check permissions
    try:
        ec2 = boto3.client('ec2')
        ec2.describe_regions(DryRun=True)
    except (EndpointConnectionError) as err:
        raise scripts.ScriptError(str(err))
    except ClientError as err:
        if 'DryRunOperation' not in str(err):
            raise scripts.ScriptError(str(err))

    # Collect region data
    try:
        all_regions = [d['RegionName'] for d in
                       ec2.describe_regions()['Regions']]
        all_regions.sort()
    except ClientError as err:
        raise scripts.ScriptError(str(err))
    except KeyError as err:
        raise scripts.ScriptError(
            "Expected 'key' not found in response: {}".format(err))

    # Collect availability zone data per region
    if avail_zones:
        print("Regions                  Availability Zones")
        print("-------                  ------------------")
        try:
            for region in all_regions:
                ec2 = boto3.client('ec2', region_name=region)
                avail_zones = [d['ZoneName'] for d in
                               ec2.describe_availability_zones()
                               ['AvailabilityZones']]
                print("{:25}({})".format(region, ", ".join(avail_zones)))
        except ClientError as err:
            raise scripts.ScriptError(str(err))
        except KeyError as err:
            raise scripts.ScriptError(
                "Expected 'key' not found in response: {}".format(err))
    else:
        print("Regions")
        print("-------")
        for region in all_regions:
            print(region)
