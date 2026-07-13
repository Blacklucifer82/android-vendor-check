def print_report(blobs):

    ok = 0
    missing = 0
    mismatch = 0
    fixup = 0

    for b in blobs:

        if not b.expected_sha:
            continue

        if not b.exists:
            missing += 1
            print(f"[MISSING] {b.path}")
            continue

        valid = False

        if b.actual_sha == b.expected_sha:
            valid = True

        if b.fixed_sha and b.actual_sha == b.fixed_sha:
            valid = True

        if valid:
            ok += 1
            continue

        if b.has_fixup:
            fixup += 1

            print(f"\n[FIXUP] {b.path}")

            for f in b.fixups:
                print(f"  {f.operation}{f.args}")

            print(f"Expected : {b.expected_sha}")
            print(f"Actual   : {b.actual_sha}")

            continue

        mismatch += 1

        print(f"\n[MISMATCH] {b.path}")
        print(f"Expected : {b.expected_sha}")

        if b.fixed_sha:
            print(f"Fixed    : {b.fixed_sha}")

        print(f"Actual   : {b.actual_sha}")

    print("\n========================")

    print(f"OK        : {ok}")
    print(f"FIXUP     : {fixup}")
    print(f"Mismatch  : {mismatch}")
    print(f"Missing   : {missing}")
