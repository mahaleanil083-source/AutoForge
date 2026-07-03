from rich.console import Console
from app.organizer import organize_folder
from app.duplicate import find_duplicates

console = Console()


def main():

    console.rule("[bold green]AutoForge")

    folder = input("Enter Folder Path : ").strip().strip('"')

    console.print("\n📂 Organizing Files...\n", style="cyan")
    organize_folder(folder)

    console.print("\n🔍 Checking Duplicate Files...\n", style="cyan")

    duplicates = find_duplicates(folder)

    if duplicates:

        console.print("\n⚠ Duplicate Files Found:\n", style="bold red")

        for original, duplicate in duplicates:
            print(f"Original : {original}")
            print(f"Duplicate: {duplicate}")
            print("-" * 50)

    else:
        console.print("✅ No Duplicate Files Found.", style="bold green")

    console.print("\n🎉 Process Completed Successfully.", style="bold green")


if __name__ == "__main__":
    main()