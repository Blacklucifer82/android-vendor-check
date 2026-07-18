from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass(frozen=True)
class Fixup:
    """
    One blob_fixup operation parsed from extract-files.py.

    Example:
        .replace_needed("libfoo.so", "libbar.so")

    becomes

        Fixup(
            op="replace_needed",
            args=("libfoo.so", "libbar.so"),
        )
    """

    op: str
    args: Tuple[str, ...] = field(default_factory=tuple)

    def __str__(self):
        if self.args:
            return f"{self.op}({', '.join(self.args)})"
        return self.op

    def __repr__(self):
        return str(self)


@dataclass
class Blob:
    """
    Represents one proprietary blob.
    """

    # Path relative to proprietary root
    path: str

    # Optional SHA1 from proprietary-files.txt
    sha1: Optional[str] = None

    # Actual SHA1
    actual_sha1: Optional[str] = None
    fixed_sha: Optional[str] = None

    # Verification
    verified: bool = False

    # extract-files.py fixups
    has_fixup: bool = False
    fixups: List[str] = field(default_factory=list)

    #
    # ELF Information
    #
    is_elf: bool = False

    soname: Optional[str] = None

    needed: Set[str] = field(default_factory=set)

    exports: Set[str] = field(default_factory=set)

    undefined: Set[str] = field(default_factory=set)

    #
    # Dependency analysis
    #
    missing_libs: List[str] = field(default_factory=list)

    #
    # Suggestions
    #
    suggestions: List[str] = field(default_factory=list)

    #
    # Resolver
    #
    provider_map: Dict[str, List["Blob"]] = field(default_factory=dict)

    #
    # Android.bp
    #
    module_name: Optional[str] = None

    compatibility_score: int = 100

    #
    # Runtime references
    #
    library_db = None

    #
    # Helpers
    #
    @property
    def filename(self) -> str:
        return self.path.split("/")[-1]

    @property
    def dirname(self) -> str:
        return "/".join(self.path.split("/")[:-1])

    @property
    def is_library(self) -> bool:
        return self.filename.endswith(".so")

    @property
    def is_binary(self) -> bool:
        return "/bin/" in self.path

    @property
    def is_firmware(self) -> bool:
        return "/firmware/" in self.path

    def add_needed(self, lib: str):
        self.needed.add(lib)

    def add_export(self, symbol: str):
        self.exports.add(symbol)

    def add_undefined(self, symbol: str):
        self.undefined.add(symbol)

    def add_fixup(self, fixup: str):
        if fixup not in self.fixups:
            self.fixups.append(fixup)

    def add_suggestion(self, text: str):
        if text not in self.suggestions:
            self.suggestions.append(text)

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"Blob({self.path})"
