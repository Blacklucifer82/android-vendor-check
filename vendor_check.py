#!/usr/bin/env python3

import argparse

from vendorcheck.parser import parse_proprietary
from vendorcheck.hashcheck import check_hashes
from vendorcheck.report import print_report

parser = argparse.ArgumentParser()

parser.add_argument("--proprietary", required=True)

parser.add_argument("--vendor", required=True)

args = parser.parse_args()

blobs = parse_proprietary(args.proprietary)

check_hashes(blobs, args.vendor)

print_report(blobs)
