"""Show regions and availability zones."""

import boto3
from botocore.exceptions import ClientError
import scripts


def showregions(avail_zones=False):
    """Show region data."""
    try:
        ec2 = boto3.client('ec2')
        all_regions = [d['RegionName'] for d in
                       ec2.describe_regions()['Regions']]
        all_regions.sort()
    except ClientError as err:
        raise scripts.ScriptError("Boto ClientError: {}".format(err))
    except KeyError as err:
        raise scripts.ScriptError("Key not found: {}".format(err))

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
            raise scripts.ScriptError("Boto ClientError: {}".format(err))
        except KeyError as err:
            raise scripts.ScriptError("Key not found: {}".format(err))
    else:
        print("Regions")
        print("-------")
        for region in all_regions:
            print(region)
