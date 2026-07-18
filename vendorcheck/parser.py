from vendorcheck.models import Blob


def parse_proprietary(path):
    """
    Parse proprietary-files.txt.

    Supported formats:

        vendor/lib/libfoo.so

        vendor/lib/libfoo.so|SHA1

        vendor/lib/libfoo.so|OLD_SHA|NEW_SHA
    """

    blobs = []

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            #
            # Skip comments
            #
            if not line:
                continue

            if line.startswith("#"):
                continue

            #
            # Remove extraction flags
            #
            line = line.split(";")[0]

            parts = line.split("|")

            blob = Blob(
                path=parts[0],
            )

            #
            # Expected SHA
            #
            if len(parts) >= 2:
                blob.sha1 = parts[1]

            #
            # Fixed SHA
            #
            if len(parts) >= 3:
                blob.fixed_sha = parts[2]

            blobs.append(blob)

    return blobs
