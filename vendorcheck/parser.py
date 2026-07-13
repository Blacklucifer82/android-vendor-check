from vendorcheck.models import Blob


def parse_proprietary(path: str) -> list[Blob]:
    blobs = []

    with open(path) as f:
        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            # Ignore extraction args (;PRESIGNED etc.)
            line = line.split(";")[0]

            parts = line.split("|")

            blob = Blob(path=parts[0])

            if len(parts) >= 2:
                blob.expected_sha = parts[1]

            if len(parts) >= 3:
                blob.fixed_sha = parts[2]

            blobs.append(blob)

    return blobs
