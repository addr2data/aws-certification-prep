"""
awscertprep_cli - Interact with the aws api for learning purposes.

Usage:
    awscertprep_cli show_regions [--avail_zones]
    awscertprep_cli create_vpc --cidr CIDR [--region REGION] [--name NAME]


Arguments:
    show_regions
    create_vpc


Options:
    --avail_zones       		Also show availibity zones.
    --region REGION             If not specified, default region is used.
    --name NAME                 Add a value to the tag labeled 'Name'
    --cidr CIDR                 Cidr address

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

if __name__ == '__main__':
    main()
