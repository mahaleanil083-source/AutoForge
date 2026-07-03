import customtkinter as ctk
from tkinter import filedialog, messagebox
from app.organizer import organize_folder


# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AutoForgeApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🚀 AutoForge Desktop v1.0")
        self.geometry("800x500")
        self.resizable(False, False)

        self.selected_folder = ""

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="🚀 AutoForge",
            font=("Segoe UI", 28, "bold")
        )
        self.title_label.pack(pady=20)

        # Folder Path
        self.folder_label = ctk.CTkLabel(
            self,
            text="No Folder Selected",
            font=("Segoe UI", 14),
            wraplength=700
        )
        self.folder_label.pack(pady=10)

        # Select Folder Button
        self.select_btn = ctk.CTkButton(
            self,
            text="📂 Select Folder",
            width=250,
            height=45,
            command=self.select_folder
        )
        self.select_btn.pack(pady=10)

        # Organize Button
        self.organize_btn = ctk.CTkButton(
            self,
            text="📁 Organize Files",
            width=250,
            height=45,
            command=self.organize_files
        )
        self.organize_btn.pack(pady=10)

        # Status
        self.status = ctk.CTkLabel(
            self,
            text="Status : Waiting...",
            font=("Segoe UI", 14)
        )
        self.status.pack(pady=20)

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=folder)
            self.status.configure(text="Folder Selected ✅")

    def organize_files(self):

        if not self.selected_folder:
            messagebox.showwarning(
                "Warning",
                "Please Select Folder First."
            )
            return

        try:
            organize_folder(self.selected_folder)

            self.status.configure(
                text="Files Organized Successfully ✅"
            )

            messagebox.showinfo(
                "Success",
                "Files Organized Successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            self.status.configure(
                text="Something Went Wrong ❌"
            )


if __name__ == "__main__":
    app = AutoForgeApp()
    app.mainloop()