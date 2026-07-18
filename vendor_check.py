#!/usr/bin/env python3

import argparse

from vendorcheck.parser import parse_proprietary
from vendorcheck.report import print_report
from vendorcheck.analyzer import Analyzer
from vendorcheck.group import group_missing
from vendorcheck.jsonreport import export_json


def main():

    parser = argparse.ArgumentParser(description="Android Vendor Sanity Checker")

    parser.add_argument(
        "--proprietary",
        required=True,
        help="Path to proprietary-files.txt",
    )

    parser.add_argument(
        "--vendor",
        required=True,
        help="Path to extracted vendor blobs",
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
        help="Enable ELF analysis",
    )

    parser.add_argument(
        "--json",
        help="Write JSON report",
    )

    args = parser.parse_args()

    #
    # Parse proprietary-files.txt
    #
    blobs = parse_proprietary(
        args.proprietary,
    )

    #
    # Run analysis
    #
    analysis = Analyzer(
        blobs=blobs,
        vendor=args.vendor,
        extract=args.extract,
        bp=args.bp,
        elf=args.elf,
    ).run()

    #
    # SHA report
    #
    print_report(blobs)

    if not args.elf:

        if args.json:
            export_json(
                args.json,
                analysis,
            )

        return

    #
    # --------------------------------------------------
    # ELF Summary
    # --------------------------------------------------
    #
    print("\n=== ELF Summary ===")

    print(f"ELF blobs : " f"{sum(b.is_elf for b in blobs)}")

    print(f"SONAMEs   : " f"{sum(1 for b in blobs if b.soname)}")

    #
    # --------------------------------------------------
    # Missing DT_NEEDED
    # --------------------------------------------------
    #
    print("\n=== Missing DT_NEEDED ===")

    groups = group_missing(
        blobs,
    )

    if not groups:

        print("None")

    else:

        for lib in sorted(groups):

            print(lib)

            for path in groups[lib]:

                print(f"    {path}")

    #
    # --------------------------------------------------
    # Compatibility
    # --------------------------------------------------
    #
    print("\n=== Compatibility ===")

    for result in analysis.compatibility:

        if result["module"] is None:
            continue

        if result["score"] == 100:
            continue

        print(f'{result["module"]}: ' f'{result["score"]}%')

    #
    # --------------------------------------------------
    # Suggestions
    # --------------------------------------------------
    #
    print("\n=== Suggestions ===")

    for blob in blobs:

        if not blob.suggestions:
            continue

        print(f"\n{blob.path}")

        for suggestion in blob.suggestions:

            if suggestion == "":
                print()
            else:
                print(f"  - {suggestion}")

    #
    # --------------------------------------------------
    # Symbol Resolver
    # --------------------------------------------------
    #
    print("\n=== Symbol Resolver ===")

    for binary in sorted(
        analysis.symbol_map,
    ):

        print(f"\n{binary}")

        symbols = analysis.symbol_map[binary]

        for symbol in sorted(symbols):

            providers = symbols[symbol]

            if not providers:
                continue

            print(f"    {symbol}" f" -> " f"{providers[0].path}")

    #
    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------
    #
    print("\n=== Statistics ===")

    for key in sorted(
        analysis.stats,
    ):

        print(f"{key:24}" f": " f"{analysis.stats[key]}")

    #
    # --------------------------------------------------
    # Health
    # --------------------------------------------------
    #
    print("\n=== Vendor Health ===")

    print(f"{analysis.health}%")

    #
    # --------------------------------------------------
    # JSON
    # --------------------------------------------------
    #
    if args.json:

        export_json(
            args.json,
            analysis,
        )

    #
    # --------------------------------------------------
    # Summary
    # --------------------------------------------------
    #
    print("\n========== SUMMARY ==========")

    print(f"Total blobs        : {len(blobs)}")

    print(f"ELF blobs          : " f"{sum(b.is_elf for b in blobs)}")

    compatible = [x["score"] for x in analysis.compatibility if x["module"] is not None]

    if compatible:

        avg = round(sum(compatible) / len(compatible))

    else:

        avg = 100

    print(f"Compatibility avg  : {avg}%")

    missing = 0

    for blob in blobs:

        missing += len(blob.missing_libs)

    print(f"Missing DT_NEEDED  : {missing}")

    print(f"Blob fixups        : " f"{sum(b.has_fixup for b in blobs)}")

    print(f"Suggestions        : " f"{sum(len(b.suggestions) for b in blobs)}")

    print("============================")


if __name__ == "__main__":
    main()
