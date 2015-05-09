#
# Copyright (c) 2014-2015 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

__author__="Rick Salevsky"
__version__="3.0.0"

import argparse
from docmanager import action
from docmanager.logmanager import log
import logging


def parsecli(cliargs=None):
    """Parse command line arguments

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed arguments
    :rtype: argparse.Namespace
    """
    filesargs = dict(nargs='+',
                     metavar="FILE",
                     help='One or more DocBook XML or DC files.'
                )
    propargs = dict(action='append',
                    # metavar="PROP[[=VALUE],PROP[=VALUE]...]
                    help='One or more properties to get, set, or delete. '
                         'Syntax of PROPERTIES: PROP[[=VALUE],PROP[=VALUE]...] '
                         'Example (get/del): -p foo or -p foo,bar or -p foo -p bar '
                         'Example (set): -p foo=a or -p foo=a,bar=b or -p foo=a -p bar=b'
               )

    parser = argparse.ArgumentParser(
        prog="docmanager",
        usage="%(prog)s COMMAND [OPTIONS] FILE [FILE ...]",
        description="Docmanager sets, gets, delets, or queries "
                    "meta-information for DocBook5 XML files.")
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__
                        )
    parser.add_argument('-v', '--verbose',
                action='count',
                help="Increase verbosity level"
            )

    # Create a subparser for all of our subcommands,
    # save the subcommand in 'dest'
    subparsers = parser.add_subparsers(
        dest='action',
        title="Available subcommands",
        # metavar="COMMAND"
        )

    # 'get' subparser
    pget = subparsers.add_parser('get',
                        aliases=['g'],
                        help='Get key and returns value'
                    )
    pget.add_argument('-p', '--properties', **propargs)
    pget.add_argument("files", **filesargs)

    # 'set' subparser
    pset = subparsers.add_parser('set',
                        aliases=['s'],
                        help='Set key=value property (one or more) to '
                             'delete the key let the value blank.'
                    )
    pset.add_argument('-p', '--properties', **propargs)
    pset.add_argument("files", **filesargs)

    # 'del' subparser
    pdel = subparsers.add_parser('del',
                        aliases=['d'],
                        help='Delete properties from XML documents'
                    )
    pdel.add_argument('-p', '--properties', **propargs)
    pdel.add_argument("files", **filesargs)

    # analyze subparser
    panalyze = subparsers.add_parser('query',
                                     aliases=['q', 'analyze'],
                                     help='Similar to get, but query can be given as pseudo SQL syntax. '  \
                                        'allowed keywords are SELECT, WHERE, and SORTBY. ' \
                                        'Output is formatted as table.'
                                    )
    panalyze.add_argument("files",
                nargs='+',
                metavar="FILES",
                help='One or more DocBook XML or DC files.'
                )

    ## -----
    args = parser.parse_args(args=cliargs)

    # Fix properties
    # Handle the different styles with -p foo and -p foo,bar
    # Needed to split the syntax 'a,b', 'a;b' or 'a b' into a list
    # regardless of the passed arguments
    _props=[ ]
    # Use an empty list when args.properties = None
    args.properties = [] if args.properties is None else args.properties
    for item in args.properties:
        _props.extend(re.split("[ ,;]", item))
    args.properties = _props

    args.arguments = args.properties
    loglevel = {
        None: logging.NOTSET,
        1: logging.INFO,
        2: logging.DEBUG
    }

    log.setLevel(loglevel.get(args.verbose, logging.DEBUG))
    return args


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    """
    action.Actions( parsecli(cliargs) )
