from dataclasses import dataclass, field


@dataclass
class Blob:
    path: str

    expected_sha: str | None = None
    fixed_sha: str | None = None
    actual_sha: str | None = None

    exists: bool = False

    has_fixup: bool = False

    needed: list[str] = field(default_factory=list)
    undefined: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
