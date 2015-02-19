#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    OpenDig
    ~~~~~

    :copyright: (c) 2014 by OpenNameSystem.org
    :license: MIT, see LICENSE for more details.
"""

import json
import sys
import time
import datetime
import argparse

from opendig import dns_resolver, ons_resolver
from .config import VERSION, DNS_SERVERS, ONS_SERVERS


# -------------------------
def run_cli():
    """ run cli
    """

    parser = argparse.ArgumentParser(
        description='OpenDig: Command-line client for Openname \
         (http://Openname.org)')

    parser.add_argument("options", help="+USERNAME will get the user info, \
        DOMAIN will get domain info", type=str)
    
    parser.add_argument("--get", help="Optional argument for getting \
        specific information (twitter, bitcoin, github) about ONENAME user", type=str)

    # Print default help message, if no argument is given
    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    """
    Check if its onename username or a domain name
    """
    if str(args.options[0]) == '+':             # username

        username = args.options[1:]
        print_header(username)

        try:
            data, elapsed_time = get_ons_data(username)
        except:
            pass
        else:
            s = "\n;; Got answer:\n\n;; QUESTION SECTION:\n;+%s\n\n;; \
                ANSWER SECTION:\n" % (username)
            sys.stdout.write(s)

        if len(sys.argv) == 2:
            sys.stdout.write(pretty_dump(data))
        elif len(sys.argv) > 2:

            if str(args.get) == "github":
                
                if 'github' in data:
                    sys.stdout.write(pretty_dump(data['github']))
                else:
                    sys.stdout.write(pretty_dump({}))

            elif str(args.get) == "bitcoin":

                if 'bitcoin' in data:
                    sys.stdout.write(pretty_dump(data['bitcoin']))
                else:
                    sys.stdout.write(pretty_dump({}))

            elif str(args.get) == "twitter":
                if 'twitter' in data:
                    sys.stdout.write(pretty_dump(data['twitter']))
                else:
                    sys.stdout.write(pretty_dump({}))
            else:
                parser.print_help()
                exit(1)

        print_ons_footer(elapsed_time)

    else:                                       # domain

        domain = args.options
        print_header(domain)
        start_time = time.time()

        try:
            data = dns_resolver(domain)
        except:
            pass
        else:
            s = "\n;; Got answer:\n\n;; QUESTION SECTION:\n;%s\n\n;; \
                ANSWER SECTION:\n" % (domain + ".")
            sys.stdout.write(s)

        elapsed_time = round(time.time() - start_time, 3)
        elapsed_time = int(1000 * elapsed_time)     # msecs
        for reply in data.answer:
            sys.stdout.write(reply.to_text() + '\n')

        print_dns_footer(elapsed_time)

# -------------------------


def pretty_dump(input):

    return json.dumps(input, sort_keys=False, indent=4, separators=(',', ': '))

# -------------------------


def print_header(query):

    sys.stdout.write("\n;; <<>> OpenDig %s <<>> %s" % (VERSION, query))

# -------------------------


def print_dns_footer(elapsed_time):

    sys.stdout.write("\n;; Query time: %s msec\n" % elapsed_time)
    sys.stdout.write(";; SERVER: %s \n" % DNS_SERVERS[0])
    sys.stdout.write(";; WHEN: %s\n\n" % datetime.datetime.now().strftime(
        "%a %b %d %H:%M:%S %Y"))

# -------------------------


def print_ons_footer(elapsed_time):

    sys.stdout.write("\n\n;; Query time: %s msec\n" % elapsed_time)
    sys.stdout.write(";; SERVERS: ")
    for server in ONS_SERVERS:
        sys.stdout.write("%s " % server)
    sys.stdout.write("\n;; WHEN: %s\n\n" % datetime.datetime.now().strftime(
        "%a %b %d %H:%M:%S %Y"))

# -------------------------


def get_ons_data(username):
    start_time = time.time()

    try:
        data = ons_resolver(username)
    except:
        pass
    else:
        elapsed_time = round(time.time() - start_time, 3)
        elapsed_time = int(1000 * elapsed_time)   # msecs

    return data, elapsed_time

# ----------------------------------------


if __name__ == '__main__':
    run_cli()
