"""
awscertprep_cli - Interact with the aws api for learning purposes.

Usage:
    awscertprep_cli create_vpc --cidr CIDR [--region REGION] [--name NAME]
    awscertprep_cli show_regions [--avail_zones]
    awscertprep_cli show_vpc [--region REGION] [--vpcid VPC_ID]

Arguments:
    create_vpc
    show_regions
    show_vpc

Options:
    --avail_zones       		Also show availibity zones.
    --region REGION             If not specified, default region is used.
    --name NAME                 Set tag called Name to some value'
    --cidr CIDR                 The cidr address to use.
    --vpcid VPC_ID              The id number for a VPC

"""

import sys
import scripts
from docopt import docopt


def main():
    """Interact with aws api."""
    args = docopt(__doc__)

    if args['show_regions']:
        try:
            scripts.show_regions(avail_zones=args['--avail_zones'])
        except scripts.ScriptError as err:
            sys.exit(err)
    elif args['create_vpc']:
        try:
            scripts.create_vpc(
                args['--cidr'], args['--region'], args['--name'])
        except scripts.ScriptError as err:
            sys.exit(err)
    elif args['show_vpc']:
        try:
            scripts.show_vpc(args['--region'], args['--vpcid'])
        except scripts.ScriptError as err:
            sys.exit(err)

if __name__ == '__main__':
    main()
