class ResolverDB:
    def __init__(self):
        self.libs = {}

    def add(self, name, provider):
        if not name:
            return

        self.libs.setdefault(name, []).append(provider)

    def find(self, name):
        return self.libs.get(name, [])

    def has(self, name):
        return name in self.libs


def build_library_db(blobs, modules):
    db = ResolverDB()

    # Register vendor blobs
    for blob in blobs:

        if not blob.is_elf:
            continue

        if blob.soname:
            db.add(blob.soname, blob)

    # Register Android.bp modules
    for module in modules.values():

        name = module.get("name")

        if not name:
            continue

        db.add(name + ".so", module)
        db.add(name, module)

    return db
