def print_report(blobs):
    """
    Print SHA verification report.
    """

    ok = 0
    missing = 0
    mismatch = 0
    fixup = 0

    for blob in blobs:

        #
        # Blob not pinned by SHA
        #
        if not blob.sha1:
            continue

        #
        # Blob missing from vendor
        #
        if not getattr(blob, "exists", True):
            missing += 1
            print(f"[MISSING] {blob.path}")
            continue

        #
        # SHA matches
        #
        if blob.actual_sha1 == blob.sha1:
            ok += 1
            continue

        #
        # Blob has extract-files.py fixup
        #
        if blob.has_fixup:

            fixup += 1

            print(f"\n[FIXUP] {blob.path}")

            for f in blob.fixups:
                print(f"  {f}")

            print(f"Expected : {blob.sha1}")
            print(f"Actual   : {blob.actual_sha1}")

            continue

        #
        # SHA mismatch
        #
        mismatch += 1

        print(f"\n[MISMATCH] {blob.path}")
        print(f"Expected : {blob.sha1}")
        print(f"Actual   : {blob.actual_sha1}")

    print("\n========================")
    print(f"OK        : {ok}")
    print(f"FIXUP     : {fixup}")
    print(f"Mismatch  : {mismatch}")
    print(f"Missing   : {missing}")
