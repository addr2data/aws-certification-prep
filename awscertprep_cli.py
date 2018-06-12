"""
awscertprep_cli - Interact with the aws api for learning purposes.

Usage:
    awscertprep_cli show_regions [--avail_zones]


Arguments:


Options:
    --avail_zones       		Also show availibity zones.

"""

import sys
import scripts
from docopt import docopt


def main():
    """Interact with aws api."""
    args = docopt(__doc__)

    if args['show_regions']:
        try:
            scripts.showregions(avail_zones=args['--avail_zones'])
        except scripts.ScriptError as err:
            sys.exit(err)

if __name__ == '__main__':
    main()
