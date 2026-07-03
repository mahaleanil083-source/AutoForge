from pathlib import Path
import shutil

from app.logger import log_info, log_error

FILE_TYPES = {
    ".pdf": "PDF",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".xlsx": "Excel",
    ".xls": "Excel",
    ".docx": "Word",
    ".doc": "Word",
    ".mp4": "Videos",
    ".mp3": "Audio",
}


def organize_folder(folder_path: str):

    # Remove extra spaces and quotes
    folder_path = folder_path.strip().strip('"')

    folder = Path(folder_path)

    # Debug
    print("\n========== DEBUG ==========")
    print(f"Input Path    : {folder_path}")
    print(f"Resolved Path : {folder.resolve()}")
    print(f"Exists        : {folder.exists()}")
    print("===========================\n")

    # Folder Check
    if not folder.exists():
        log_error("Folder does not exist.")
        print("❌ Folder does not exist.")
        return

    # Organize Files
    for file in folder.iterdir():

        if file.is_dir():
            continue

        category = FILE_TYPES.get(file.suffix.lower(), "Others")

        destination = folder / category
        destination.mkdir(exist_ok=True)

        shutil.move(str(file), str(destination / file.name))

        message = f"Moved: {file.name} -> {category}"

        print(message)
        log_info(message)

    print("\n🎉 File organization completed successfully.")

    log_info("File organization completed successfully.")