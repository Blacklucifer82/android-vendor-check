import os

from vendorcheck.utils import sha1


def check_hashes(blobs, vendor_root):
    """
    Verify SHA1 hashes for all blobs.
    """

    for blob in blobs:

        full = os.path.join(
            vendor_root,
            blob.path,
        )

        #
        # Blob missing
        #
        if not os.path.exists(full):

            blob.exists = False
            blob.actual_sha1 = None
            blob.verified = False

            continue

        blob.exists = True

        #
        # Calculate SHA1
        #
        blob.actual_sha1 = sha1(full)

        #
        # Verification
        #
        if not blob.sha1:
            blob.verified = True

        elif blob.actual_sha1 == blob.sha1:
            blob.verified = True

        elif getattr(blob, "fixed_sha", None) and blob.actual_sha1 == blob.fixed_sha:
            blob.verified = True

        else:
            blob.verified = False
