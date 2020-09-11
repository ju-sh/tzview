"""
__main__.py for tzview
"""

import sys
import tzview.cli

if __name__ == '__main__':
    parser = tzview.cli.create_parser()
    args = parser.parse_args()
    sys.exit(tzview.cli.main(args))
