from dataclasses import dataclass, field


@dataclass
class Fixup:
    operation: str
    args: tuple


@dataclass
class Blob:
    path: str

    soname: str | None = None

    # SHA information
    expected_sha: str | None = None
    fixed_sha: str | None = None
    actual_sha: str | None = None

    exists: bool = False

    # proprietary-files args
    args: list[str] = field(default_factory=list)

    # blob_fixup()
    has_fixup: bool = False
    fixups: list[Fixup] = field(default_factory=list)

    # ELF metadata
    is_elf: bool = False
    arch: str | None = None
    soname: str | None = None

    needed: set[str] = field(default_factory=set)
    undefined: set[str] = field(default_factory=set)
    exports: set[str] = field(default_factory=set)

    # Android.bp
    module: str | None = None
    allow_undefined: bool = False
    check_elf: bool = True

    subsystem: str | None = None
    
bp_module: dict | None = None

bp_shared_libs: set[str] = field(default_factory=set)

bp_static_libs: set[str] = field(default_factory=set)

bp_header_libs: set[str] = field(default_factory=set)
