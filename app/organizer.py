from pathlib import Path
import shutil

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

    # Input मधील extra spaces आणि quotes काढून टाका
    folder_path = folder_path.strip().strip('"')

    folder = Path(folder_path)

    # Debug Information
    print("\n========== DEBUG ==========")
    print(f"Input Path    : {folder_path}")
    print(f"Resolved Path : {folder.resolve()}")
    print(f"Exists        : {folder.exists()}")
    print("===========================\n")

    if not folder.exists():
        print("❌ Folder does not exist.")
        return

    for file in folder.iterdir():

        if file.is_dir():
            continue

        category = FILE_TYPES.get(file.suffix.lower(), "Others")

        destination = folder / category
        destination.mkdir(exist_ok=True)

        shutil.move(str(file), str(destination / file.name))

        print(f"✅ Moved: {file.name} -> {category}")

    print("\n🎉 File organization completed successfully.")