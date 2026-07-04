import threading
import customtkinter as ctk
from tkinter import filedialog

from app.organizer import organize_folder


# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🚀 AutoForge v1.0")
        self.geometry("900x650")
        self.resizable(False, False)

        self.selected_folder = ""

        # ---------------- Title ----------------
        self.title_label = ctk.CTkLabel(
            self,
            text="🚀 AutoForge",
            font=("Segoe UI", 30, "bold")
        )
        self.title_label.pack(pady=20)

        # ---------------- Folder ----------------
        self.folder_label = ctk.CTkLabel(
            self,
            text="No Folder Selected",
            font=("Segoe UI", 14),
            wraplength=800
        )
        self.folder_label.pack(pady=10)

        # ---------------- Browse Button ----------------
        self.browse_btn = ctk.CTkButton(
            self,
            text="📂 Browse Folder",
            width=250,
            command=self.select_folder
        )
        self.browse_btn.pack(pady=10)

        # ---------------- Buttons Frame ----------------
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        # Organize Button
        self.organize_btn = ctk.CTkButton(
            self.button_frame,
            text="📁 Organize Files",
            width=180,
            command=self.start_organize
        )
        self.organize_btn.grid(row=0, column=0, padx=10)

        # Duplicate Button
        self.duplicate_btn = ctk.CTkButton(
            self.button_frame,
            text="🔍 Find Duplicates",
            width=180
        )
        self.duplicate_btn.grid(row=0, column=1, padx=10)

        # ---------------- Progress ----------------
        self.progress_label = ctk.CTkLabel(
            self,
            text="Progress"
        )
        self.progress_label.pack()

        self.progress = ctk.CTkProgressBar(
            self,
            width=600
        )
        self.progress.pack(pady=10)
        self.progress.set(0)

        # ---------------- Activity Log ----------------
        self.log_label = ctk.CTkLabel(
            self,
            text="Activity Log"
        )
        self.log_label.pack()

        self.log_box = ctk.CTkTextbox(
            self,
            width=700,
            height=220
        )
        self.log_box.pack(pady=10)

        self.log_box.insert("end", "🚀 AutoForge Started...\n")

    # -------------------------------------------------

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.selected_folder = folder

            self.folder_label.configure(text=folder)

            self.add_log(f"📂 Folder Selected:\n{folder}")

    # -------------------------------------------------

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

    # -------------------------------------------------

    def run_organizer(self):

        try:

            organize_folder(
                self.selected_folder,
                progress_callback=self.update_progress,
                log_callback=self.add_log
            )

            self.add_log("✅ Completed Successfully.")

        except Exception as e:

            self.add_log(f"❌ Error : {e}")

    # -------------------------------------------------

    def update_progress(self, value):

        self.after(
            0,
            lambda: self.progress.set(value)
        )

    # -------------------------------------------------

    def add_log(self, message):

        def update():

            self.log_box.insert(
                "end",
                message + "\n"
            )

            self.log_box.see("end")

        self.after(0, update)