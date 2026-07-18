import os


class ResolverDB:
    """
    Database of libraries provided by the vendor.
    """

    def __init__(self):
        self.libs = {}

    def add(self, name, provider):
        """
        Register a library provider.
        """
        if not name:
            return

        self.libs.setdefault(name, []).append(provider)

    def has(self, name):
        return name in self.libs

    def find(self, name):
        return self.libs.get(name, [])

    def __contains__(self, name):
        return self.has(name)

    def __len__(self):
        return len(self.libs)


def build_library_db(blobs, modules):
    """
    Build a database of every library supplied by the vendor.

    Libraries are indexed by:
        - SONAME
        - filename
        - Android.bp module name
    """

    db = ResolverDB()

    #
    # Index every ELF blob
    #
    for blob in blobs:

        if not blob.is_elf:
            continue

        #
        # SONAME
        #
        if blob.soname:
            db.add(blob.soname, blob)

        #
        # filename fallback
        #
        filename = os.path.basename(blob.path)

        if filename.endswith(".so"):
            db.add(filename, blob)

    #
    # Index Android.bp module names
    #
    if isinstance(modules, dict):

        iterable = modules.values()

    else:

        iterable = modules

    for module in iterable:

        if not isinstance(module, dict):
            continue

        name = module.get("name")

        if not name:
            continue

        db.add(name + ".so", module)

    return db
