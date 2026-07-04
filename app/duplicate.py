from pathlib import Path
import hashlib


def get_file_hash(file_path, chunk_size=8192):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(folder_path):

    folder = Path(folder_path)

    if not folder.exists():
        return []

    hashes = {}

    duplicates = []

    for file in folder.rglob("*"):

        if not file.is_file():
            continue

        try:

            file_hash = get_file_hash(file)

            if file_hash in hashes:

                duplicates.append((hashes[file_hash], file))

            else:

                hashes[file_hash] = file

        except Exception as e:

            print(f"Error hashing {file}: {e}")

    return duplicates