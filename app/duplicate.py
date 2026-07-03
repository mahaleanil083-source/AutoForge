from pathlib import Path
import hashlib


def get_file_hash(file_path: Path) -> str:
    """Return SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()
def find_duplicates(folder_path: str):

    folder = Path(folder_path)

    hashes = {}

    duplicates = []

    for file in folder.rglob("*"):

        if file.is_dir():
            continue

        file_hash = get_file_hash(file)

        if file_hash in hashes:
            duplicates.append((hashes[file_hash], file))
        else:
            hashes[file_hash] = file

    return duplicates