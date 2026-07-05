import os
import csv
import customtkinter as ctk
from tkinter import messagebox, filedialog


class DuplicateWindow(ctk.CTkToplevel):

    def __init__(self, parent, duplicates):

        super().__init__(parent)

        self.parent = parent
        self.duplicates = duplicates

        self.selected_files = []
        self.checkboxes = []

        self.title("🔍 Duplicate Manager")
        self.geometry("950x600")
        self.resizable(False, False)

        self.grab_set()

        # ==========================================
        # Title
        # ==========================================

        self.title_label = ctk.CTkLabel(
            self,
            text="🔍 Duplicate Manager",
            font=("Segoe UI", 24, "bold")
        )

        self.title_label.pack(pady=(15, 5))

        # ==========================================
        # Count Label
        # ==========================================

        self.count_label = ctk.CTkLabel(
            self,
            text=f"Found {len(self.duplicates)} Duplicate Files",
            font=("Segoe UI", 15)
        )

        self.count_label.pack(pady=(0, 10))

        # ==========================================
        # Top Buttons
        # ==========================================

        self.top_frame = ctk.CTkFrame(self)

        self.top_frame.pack(fill="x", padx=20)

        self.select_all_btn = ctk.CTkButton(
            self.top_frame,
            text="☑ Select All",
            width=140,
            command=self.select_all
        )

        self.select_all_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.clear_btn = ctk.CTkButton(
            self.top_frame,
            text="❎ Clear",
            width=140,
            command=self.clear_selection
        )

        self.clear_btn.pack(
            side="left",
            padx=10
        )

        # ==========================================
        # Scroll Area
        # ==========================================

        self.scroll = ctk.CTkScrollableFrame(
            self,
            width=880,
            height=330
        )

        self.scroll.pack(
            padx=20,
            pady=15,
            fill="both",
            expand=True
        )

        # ==========================================
        # Bottom Buttons
        # ==========================================

        self.bottom_frame = ctk.CTkFrame(self)

        self.bottom_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.delete_btn = ctk.CTkButton(
            self.bottom_frame,
            text="🗑 Delete Selected",
            width=170,
            command=self.delete_selected
        )

        self.delete_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.export_btn = ctk.CTkButton(
            self.bottom_frame,
            text="📄 Export CSV",
            width=170,
            command=self.export_csv
        )

        self.export_btn.pack(
            side="left",
            padx=10
        )

        self.close_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Close",
            width=150,
            command=self.destroy
        )

        self.close_btn.pack(
            side="right",
            padx=10
        )

        # ==========================================
        # Load Duplicate List
        # ==========================================

        self.refresh_list()

        # ==========================================
        # Refresh Duplicate List
        # ==========================================

    def refresh_list(self):

        # Clear old widgets
        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.checkboxes.clear()

        # Header
        header = ctk.CTkFrame(self.scroll)
        header.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            header,
            text="",
            width=40
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Original File",
            width=350,
            anchor="w",
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            header,
            text="Duplicate File",
            width=350,
            anchor="w",
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=5)

        # Duplicate rows
        for original, duplicate in self.duplicates:

            row = ctk.CTkFrame(self.scroll)
            row.pack(fill="x", pady=3)

            checkbox = ctk.CTkCheckBox(
                row,
                text="",
                width=20,
                command=lambda d=duplicate: self.toggle_selection(d)
            )

            checkbox.pack(side="left", padx=10)

            self.checkboxes.append((checkbox, duplicate))

            ctk.CTkLabel(
                row,
                text=original.name,
                width=350,
                anchor="w"
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                row,
                text=duplicate.name,
                width=350,
                anchor="w"
            ).pack(side="left", padx=5)

        # Update Count
        self.count_label.configure(
            text=f"Found {len(self.duplicates)} Duplicate Files"
        )

        # ==========================================
        # Toggle Selection
        # ==========================================

    def toggle_selection(self, file_path):

        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
        else:
            self.selected_files.append(file_path)

        # ==========================================
        # Select All
        # ==========================================

    def select_all(self):

        self.selected_files.clear()

        for checkbox, file_path in self.checkboxes:

            checkbox.select()

            if file_path not in self.selected_files:
                self.selected_files.append(file_path)

        # ==========================================
        # Clear Selection
        # ==========================================

    def clear_selection(self):

        self.selected_files.clear()

        for checkbox, _ in self.checkboxes:
            checkbox.deselect()

        # ==========================================
        # Delete Selected Files
        # ==========================================

    def delete_selected(self):

        if not self.selected_files:
            messagebox.showwarning(
                "No Selection",
                "Please select at least one duplicate file."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete "
            f"{len(self.selected_files)} selected duplicate file(s)?"
        )

        if not confirm:
            return

        deleted = 0

        deleted_files = self.selected_files.copy()

        for file_path in deleted_files:

            try:

                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted += 1

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Unable to delete\n{file_path}\n\n{e}"
                )

        # Remove deleted files from duplicate list
        self.duplicates = [
            pair
            for pair in self.duplicates
            if pair[1] not in deleted_files
        ]

        self.selected_files.clear()

        self.refresh_list()

        messagebox.showinfo(
            "Completed",
            f"Successfully deleted {deleted} duplicate file(s)."
        )

        # ==========================================
        # Export CSV
        # ==========================================

    def export_csv(self):

        if not self.duplicates:

            messagebox.showwarning(
                "Nothing to Export",
                "Duplicate list is empty."
            )
            return

        file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV File", "*.csv")
            ],
            initialfile="duplicate_report.csv"
        )

        if not file:
            return

        try:

            with open(file, "w", newline="", encoding="utf-8") as csvfile:

                writer = csv.writer(csvfile)

                writer.writerow([
                    "Original File",
                    "Duplicate File"
                ])

                for original, duplicate in self.duplicates:

                    writer.writerow([
                        str(original),
                        str(duplicate)
                    ])

            messagebox.showinfo(
                "Export Completed",
                f"CSV exported successfully.\n\n{file}"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Failed",
                str(e)
            )        