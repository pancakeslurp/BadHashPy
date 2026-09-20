# BadHashPy - dnd-toolkit version
# External requirement: https://github.com/pancakeslurp/BadHashPy/

"""
badhashpy_dnd-toolkit.py
==================
Rebuilt version of BadHashPy.py using dnd_toolkit.DragDropToolApp.

Drop a file -> shows MD5, SHA-1, and SHA-256 in one row. Use "Copy
Selected" to copy all three hashes for a row at once.

Improvement over the original: BadHashPy.py read the entire file into
memory at once (`f.read()`) before hashing. For forensic work that
often means multi-gigabyte evidence files, so this version hashes in
1 MB chunks instead -- same result, far less memory pressure.

Only `process_file()` below is tool-specific; everything else
(drag-and-drop, result display, copy button) comes from
dnd_toolkit.py.
"""

import hashlib
from pathlib import Path
from dnd_toolkit import DragDropToolApp

CHUNK_SIZE = 1024 * 1024  # 1 MB


class HashGeneratorApp(DragDropToolApp):
    def __init__(self):
        super().__init__(
            title="BadHashPy",
            instructions="Drop a file here to compute MD5 / SHA-1 / SHA-256",
            columns=("File", "MD5", "SHA-1", "SHA-256"),
            window_size=(700, 320),
        )

    def process_file(self, path: Path) -> tuple:
        hashers = {
            "MD5": hashlib.md5(),
            "SHA-1": hashlib.sha1(),
            "SHA-256": hashlib.sha256(),
        }
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                for hasher in hashers.values():
                    hasher.update(chunk)
        return tuple(h.hexdigest() for h in hashers.values())


if __name__ == "__main__":
    HashGeneratorApp().run()