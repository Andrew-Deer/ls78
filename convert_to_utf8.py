from collections import Counter
from pathlib import Path
import re
import sys


CHARSET_RE = re.compile(rb'charset=([^"]+)')


def eprint(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def convert_to_utf8(path: Path, from_enc: str | None = None):
    eprint(f"Converting {path}... ", end="")
    if from_enc is None:
        bytes = path.read_bytes()
        charset_match = CHARSET_RE.search(bytes)
        if charset_match is None:
            eprint("No charset found, skipping.")
            return
        from_enc = charset_match.group(1).decode("ascii")
        bytes = CHARSET_RE.sub(rb"charset=utf-8", bytes)
        txt = bytes.decode(from_enc)
    else:
        txt = path.read_text(encoding=from_enc)
    eprint(f"from {from_enc} to utf-8.")
    path.write_text(txt, encoding="utf-8")


def main():
    paths = sorted(
        p
        for p in Path(".").rglob("*")
        if p.is_file() and p.parts[0] not in {".git", ".nojekyll", ".vscode"}
    )
    extensions = Counter(p.suffix for p in paths if p.is_file() if p.suffix)
    eprint(f"Found {len(paths)} files with extensions: {extensions.most_common()}")

    for path in paths:
        if path.suffix in {".htm", ".html"}:
            convert_to_utf8(path)
        elif path.suffix == ".txt":
            convert_to_utf8(path, "windows-1250")


if __name__ == "__main__":
    main()
