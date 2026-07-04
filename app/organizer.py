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


def organize_folder(folder_path, progress_callback=None, log_callback=None):

    folder_path = folder_path.strip().strip('"')
    folder = Path(folder_path)

    # Debug
    print("\n========== DEBUG ==========")
    print(f"Input Path    : {folder_path}")
    print(f"Resolved Path : {folder.resolve()}")
    print(f"Exists        : {folder.exists()}")
    print("===========================\n")

    if not folder.exists():
        log_error("Folder does not exist.")
        print("❌ Folder does not exist.")
        return

    # फक्त Files घ्या
    files = [f for f in folder.iterdir() if f.is_file()]
    total_files = len(files)
    print(f"Total Files: {total_files}")

    if total_files == 0:
        log_info("No files found.")
        return

    # प्रत्येक File Process करा
    for index, file in enumerate(files, start=1):

        category = FILE_TYPES.get(file.suffix.lower(), "Others")

        destination = folder / category
        destination.mkdir(exist_ok=True)

        shutil.move(
            str(file),
            str(destination / file.name)
        )

        message = f"Moved: {file.name} -> {category}"

        print(message)
        log_info(message)

        if log_callback:
            log_callback(message)

        if progress_callback:
            progress_callback(index / total_files)

    print("\n🎉 File organization completed successfully.")
    log_info("File organization completed successfully.")