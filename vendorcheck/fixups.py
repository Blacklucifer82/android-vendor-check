import re

from vendorcheck.models import Fixup


def parse_fixups(path):
    result = {}

    current_blob = None

    with open(path) as f:

        for line in f:

            # New blob_fixup block
            m = re.match(r"\s*'([^']+)':\s*blob_fixup", line)

            if m:
                current_blob = m.group(1)
                result[current_blob] = []
                continue

            # No active blob
            if current_blob is None:
                continue

            stripped = line.strip()

            # End of blob_fixup dictionary
            if stripped.startswith("}"):
                current_blob = None
                continue

            # Ignore empty lines
            if not stripped:
                continue

            # Ignore anything that isn't part of the fluent API
            if not stripped.startswith("."):
                continue

            m = re.match(r"\.([A-Za-z0-9_]+)\((.*)\)", stripped)

            if not m:
                continue

            op = m.group(1)

            args = tuple(x.strip().strip("'\"") for x in m.group(2).split(",") if x.strip())

            result[current_blob].append(Fixup(op, args))

    return result
