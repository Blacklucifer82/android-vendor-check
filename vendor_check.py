#!/usr/bin/env python3

import argparse

from vendorcheck.parser import parse_proprietary
from vendorcheck.report import print_report
from vendorcheck.analyzer import Analyzer


def main():
    parser = argparse.ArgumentParser(
        description="Android Vendor Sanity Checker"
    )

    parser.add_argument(
        "--proprietary",
        required=True,
        help="Path to proprietary-files.txt",
    )

    parser.add_argument(
        "--vendor",
        required=True,
        help="Path to extracted proprietary blobs",
    )

    parser.add_argument(
        "--extract",
        required=True,
        help="Path to extract-files.py",
    )

    parser.add_argument(
        "--bp",
        required=True,
        help="Path to Android.bp",
    )

    parser.add_argument(
        "--elf",
        action="store_true",
        help="Analyze ELF files",
    )

    args = parser.parse_args()

    # Parse proprietary-files.txt
    blobs = parse_proprietary(args.proprietary)

    # Run analyzer
    analysis = Analyzer(
    blobs=blobs,
    vendor=args.vendor,
    extract=args.extract,
    bp=args.bp,
    elf=args.elf,
    ).run()

    # SHA/Fixup report
    print_report(blobs)

    # ELF-specific output
    if args.elf:

        print("\n=== ELF Summary ===")
        print(f"ELF blobs : {sum(b.is_elf for b in blobs)}")
        print(f"SONAMEs   : {sum(1 for b in blobs if b.soname)}")

        print("\n=== Missing DT_NEEDED ===")

        missing = False

        for blob, libs in analysis.missing_libs.items():

            if not libs:
                continue

            missing = True

            print(blob)

            for lib in libs:
                print(f"    {lib}")

        if not missing:
            print("None")

        print("\n=== Compatibility ===")

        for result in analysis.compatibility:

            if result["module"] is None:
                continue

            if result["score"] != 100:
                print(
                    f'{result["module"]}: '
                    f'{result["score"]}%'
                )

        print("\n=== Symbol Resolver ===")

        x = analysis.symbol_map.get(
            "vendor/bin/xtra-daemon",
            {},
        )

        for symbol in sorted(x):

            providers = x[symbol]

            if providers:
                print(
                    f"{symbol} -> {providers[0].path}"
                )


if __name__ == "__main__":
    main()
