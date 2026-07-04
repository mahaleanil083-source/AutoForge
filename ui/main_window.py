import threading
import customtkinter as ctk
from tkinter import filedialog

from app.organizer import organize_folder
from app.duplicate import find_duplicates
from ui.duplicate_window import DuplicateWindow


# ---------------- Theme ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window
        self.title("🚀 AutoForge v2.0")
        self.geometry("950x700")
        self.resizable(False, False)

        self.selected_folder = ""

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="🚀 AutoForge",
            font=("Segoe UI", 30, "bold")
        )
        self.title_label.pack(pady=20)

        # Folder Label
        self.folder_label = ctk.CTkLabel(
            self,
            text="No Folder Selected",
            font=("Segoe UI", 14),
            wraplength=850
        )
        self.folder_label.pack(pady=10)

        # Browse Button
        self.browse_btn = ctk.CTkButton(
            self,
            text="📂 Browse Folder",
            width=250,
            command=self.select_folder
        )
        self.browse_btn.pack(pady=10)

        # Button Frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        # Organize Button
        self.organize_btn = ctk.CTkButton(
            self.button_frame,
            text="📁 Organize Files",
            width=180,
            command=self.start_organize
        )

        self.organize_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        # Duplicate Button
        self.duplicate_btn = ctk.CTkButton(
            self.button_frame,
            text="🔍 Find Duplicates",
            width=180,
            command=self.start_duplicate_scan
        )

        self.duplicate_btn.grid(
            row=0,
            column=1,
            padx=10
        )

        # Progress Label
        self.progress_title = ctk.CTkLabel(
            self,
            text="Progress"
        )

        self.progress_title.pack()

        # Progress Bar
        self.progress = ctk.CTkProgressBar(
            self,
            width=700
        )

        self.progress.pack(pady=10)
        self.progress.set(0)

        # Log Label
        self.log_title = ctk.CTkLabel(
            self,
            text="Activity Log"
        )

        self.log_title.pack()

        # Log Box
        self.log_box = ctk.CTkTextbox(
            self,
            width=800,
            height=250
        )

        self.log_box.pack(pady=10)

        self.add_log("🚀 AutoForge Started...")
        # =====================================================
    # Folder Selection
    # =====================================================

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=folder)
            self.add_log(f"📂 Folder Selected:\n{folder}")

    # =====================================================
    # Organize Files
    # =====================================================

    def start_organize(self):

        if not self.selected_folder:
            self.add_log("❌ Please select a folder first.")
            return

        self.progress.set(0)

        thread = threading.Thread(
            target=self.run_organizer,
            daemon=True
        )

        thread.start()

    def run_organizer(self):

        self.add_log("📂 Organizing Files...")

        try:

            organize_folder(
                self.selected_folder,
                progress_callback=self.update_progress,
                log_callback=self.add_log
            )

            self.update_progress(1)

            self.add_log("✅ File Organization Completed.")

        except Exception as e:

            self.add_log(f"❌ Error: {e}")
        # =====================================================
    # Duplicate Scanner
    # =====================================================

    def start_duplicate_scan(self):

        if not self.selected_folder:
            self.add_log("❌ Please select a folder first.")
            return

        self.progress.set(0)

        thread = threading.Thread(
            target=self.run_duplicate_scan,
            daemon=True
        )

        thread.start()

    def run_duplicate_scan(self):

        self.add_log("🔍 Scanning Duplicate Files...")

        try:

            duplicates = find_duplicates(self.selected_folder)

            self.update_progress(1)

            if duplicates:

                self.add_log(
                    f"✅ Found {len(duplicates)} Duplicate Files"
                )

                self.after(
                    0,
                    lambda: DuplicateWindow(
                        self,
                        duplicates
                    )
                )

            else:

                self.add_log("✅ No Duplicate Files Found.")

        except Exception as e:

            self.add_log(f"❌ Error: {e}")
        # =====================================================
    # Progress Bar
    # =====================================================

    def update_progress(self, value):

        self.after(
            0,
            lambda: self.progress.set(value)
        )

    # =====================================================
    # Activity Log
    # =====================================================

    def add_log(self, message):

        def update():

            self.log_box.insert(
                "end",
                message + "\n"
            )

            self.log_box.see("end")

        self.after(0, update)
if __name__ == "__main__":

    app = MainWindow()
    app.mainloop()                            