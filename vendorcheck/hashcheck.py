import os

from vendorcheck.utils import sha1


def check_hashes(blobs, vendor_root):

    for blob in blobs:

        full = os.path.join(vendor_root, blob.path)

        if not os.path.exists(full):
            blob.exists = False
            continue

        blob.exists = True

        blob.actual_sha = sha1(full)
