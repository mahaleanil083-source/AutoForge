import os
import csv
import datetime
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox, filedialog, Menu
from send2trash import send2trash


class DuplicateWindow(ctk.CTkToplevel):

    def __init__(self, parent, duplicates):

        super().__init__(parent)

        parent.withdraw()

        

        # ==========================================
        # Data
        # ==========================================

        self.parent = parent

        self.all_duplicates = duplicates.copy()
        self.duplicates = duplicates.copy()

        self.selected_files = []
        self.checkboxes = []

        # ==========================================
        # Window
        # ==========================================
    
        self.title("🔍 Duplicate Manager")
        self.geometry("1300x900")
        self.resizable(False, False)

        # self.state("zoomed")
        # self.grab_set()

        # ==========================================
        # Title
        # ==========================================

        self.title_label = ctk.CTkLabel(
            self,
            text="🔍 Duplicate Manager",
            font=("Segoe UI", 28, "bold")
        )

        self.title_label.pack(
            pady=(15, 5)
        )

        # ==========================================
        # Count Label
        # ==========================================

        self.count_label = ctk.CTkLabel(
            self,
            text=f"Found {len(self.duplicates)} Duplicate Files",
            font=("Segoe UI", 15)
        )

        # -----------------------------
        # Statistics Panel
        # -----------------------------

        
        self.stats_frame = ctk.CTkFrame(self)

        self.stats_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.total_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total: 0",
            font=("Segoe UI", 14, "bold")
        )

        self.total_label.pack(
            side="left",
            padx=20,
            pady=10
        )

        self.selected_label = ctk.CTkLabel(
            self.stats_frame,
            text="Selected: 0",
            font=("Segoe UI", 14, "bold")
        )

        self.selected_label.pack(
            side="left",
            padx=20
        )

        self.size_label = ctk.CTkLabel(
            self.stats_frame,
            text="Size: 0 MB",
            font=("Segoe UI", 14, "bold")
        )

        self.size_label.pack(
            side="left",
            padx=20
        )

        # ==========================================
        # Toolbar
        # ==========================================

        self.toolbar = ctk.CTkFrame(self)

        self.toolbar.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # Search

        self.search_entry = ctk.CTkEntry(
            self.toolbar,
            width=320,
            placeholder_text="Search duplicate..."
        )

        self.search_entry.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_duplicates
        )

        # Sort

        self.sort_option = ctk.CTkOptionMenu(
            self.toolbar,
            values=[
                "Name",
                "Size",
                "Extension"
            ],
            width=170,
            command=self.sort_duplicates
        )

        self.sort_option.pack(
            side="right",
            padx=10
        )

        # ==========================================
        # Action Buttons
        # ==========================================

        self.action_frame = ctk.CTkFrame(self)

        self.action_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.select_btn = ctk.CTkButton(
            self.action_frame,
            text="☑ Select All",
            width=150,
            command=self.select_all
        )

        self.select_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.clear_btn = ctk.CTkButton(
            self.action_frame,
            text="❎ Clear Selection",
            width=150,
            command=self.clear_selection
        )

        self.clear_btn.pack(
            side="left",
            padx=10
        )

        self.auto_select_btn = ctk.CTkButton(
            self.action_frame,
            text="⚡ Auto Select",
            width=150,
            command=self.auto_select_duplicates
)

        self.auto_select_btn.pack(
            side="left",
            padx=10
        )


        # -----------------------------
        # Progress Section
        # -----------------------------

        self.progress_frame = ctk.CTkFrame(self)

        self.progress_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready"
        )

        self.progress_label.pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame
        )

        self.progress_bar.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.progress_bar.set(0)

        # ==========================================
        # Scroll Area
        # ==========================================

        self.content_frame = ctk.CTkFrame(self)

        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=500
        )

        self.progress_bar.pack(
            pady=(5, 0)
        )

        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(
            self,
            text="Ready"
        )

        self.progress_label.pack(
            pady=(0, 10)
        )

        self.scroll = ctk.CTkScrollableFrame(
            self.content_frame,
            width=650,
            height=360
        )

        self.scroll.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0,10)
        )

        self.preview_frame = ctk.CTkFrame(
            self.content_frame,
            width=260
        )

        self.preview_frame.pack(
            side="right",
            fill="y"
        )

        self.preview_title = ctk.CTkLabel(
            self.preview_frame,
            text="Preview",
            font=("Segoe UI", 18, "bold")
        )

        self.preview_title.pack(
            pady=(20,10)
        )

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Select a file",
            width=220,
            height=220
        )

        self.preview_info = ctk.CTkLabel(
            self.preview_frame,
            text="",
            justify="left",
            anchor="nw"
        )

        self.preview_info.pack(
            fill="x",
            padx=10,
            pady=(5, 10)
        )

        self.preview_label.pack(
            padx=20,
            pady=20
        )

        # ==========================================
        # Status Bar
        # ==========================================

        self.status_label = ctk.CTkLabel(
            self,
            text="Total: 0    Selected: 0    Size: 0 MB",
            font=("Segoe UI", 13),
            anchor="w"
        )

        self.status_label.pack(
            fill="x",
            padx=20,
            pady=(5, 5)
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
            width=120,
            command=self.delete_selected,
            state="disabled"
        )

        self.delete_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.export_btn = ctk.CTkButton(
            self.bottom_frame,
            text="📄 Export CSV",
            width=120,
            command=self.export_csv
        )

        self.export_btn.pack(
            side="left",
            padx=10
        )

        self.close_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Close",
            width=120,
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

        # -----------------------------
        # Right Click Menu
        # -----------------------------

        self.context_menu = Menu(
            self,
            tearoff=0
        )
        self.context_menu.add_command(
            label="📂 Open File",
            command=self.open_file
        )

        self.context_menu.add_command(
            label="📁 Open Folder",
            command=self.open_folder
        )

        self.context_menu.add_separator()

        self.context_menu.add_command(
                label="📋 Copy Full Path",
                command=self.copy_full_path
        )

        self.context_menu.add_separator()

        self.context_menu.add_command(
            label="🗑 Delete File",
            command=self.delete_context_file
        )

        self.update_progress(5, 10)

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    def shorten_text(self, text, max_length=35):

        if len(text) <= max_length:
            return text

        return text[:max_length] + "..."
    
    def show_tooltip(self, event, text):

        self.tooltip = ctk.CTkToplevel(self)

        self.tooltip.overrideredirect(True)

        self.tooltip.geometry(
            f"+{event.x_root+10}+{event.y_root+10}"
        )

        label = ctk.CTkLabel(
            self.tooltip,
            text=text,
            corner_radius=6
        )

        label.pack(padx=5, pady=5)

    def hide_tooltip(self, event):

        if hasattr(self, "tooltip"):

            self.tooltip.destroy()    


    def refresh_list(self):

        # ==========================================
        # Clear Old Rows
        # ==========================================

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.checkboxes.clear()

        if len(self.duplicates) == 0:

            empty_icon = ctk.CTkLabel(
                self.scroll,
                text="🎉",
                font=("Segoe UI", 60)
            )

            empty_icon.pack(
                pady=(60, 10)
            )

            empty_title = ctk.CTkLabel(
                self.scroll,
                text="No Duplicate Files Found",
                font=("Segoe UI", 22, "bold")
            )

            empty_title.pack()

            empty_subtitle = ctk.CTkLabel(
                self.scroll,
                text="Your folder is clean.",
                font=("Segoe UI", 14)
            )

            empty_subtitle.pack(
                pady=(5, 20)
            )

            self.count_label.configure(
                text="Found 0 Duplicate Files"
            )

            return

        # ==========================================
        # Header
        # ==========================================

        header = ctk.CTkFrame(self.scroll)
        header.pack(fill="x", pady=(0, 8))

        columns = [
            ("", 40),
            ("Original File", 260),
            ("Duplicate File", 260),
            ("Size", 90),
            ("Type", 80),
            ("Open", 60)
        ]

        for text, width in columns:

            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                anchor="w",
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=2)

        # ==========================================
        # Duplicate Rows
        # ==========================================

        for original, duplicate in self.duplicates:

            row = ctk.CTkFrame(self.scroll)
            image_extensions = {
                ".png",
                ".jpg",
                ".jpeg",
                ".bmp",
                ".gif",
                ".webp"
            }

            row.bind(
                "<Button-1>",
                lambda e, p=duplicate: (
                    self.show_image_preview(p)
                    if p.suffix.lower() in image_extensions
                    else self.preview_label.configure(
                        image=None,
                        text="Preview not available"
                    )
                )
            )
            row.pack(fill="x", pady=3)

            row.bind(
                "<Button-1>",
                lambda e: print("ROW CLICKED")
            )
            
            # Hover
            row.bind(
                "<Enter>",
                lambda e, r=row:
                    None if getattr(r, "is_selected", False)
                    else r.configure(fg_color=("gray80", "gray25"))
            )

            row.bind(
                "<Leave>",
                lambda e, r=row: r.configure(
                    fg_color="transparent"
            )
        )

            # Checkbox
            checkbox = ctk.CTkCheckBox(
                row,
                text="",
                width=20,
                command=lambda d=duplicate, r=row:
                    self.toggle_selection(d, r)
            )

            checkbox.pack(side="left", padx=5)

            self.checkboxes.append((checkbox, duplicate))

            checkbox.bind(
                "<Button-3>",
                lambda e, p=duplicate: self.show_context_menu(e, p)
            )

            # Original File

            ctk.CTkLabel(
                row,
                text=self.shorten_text(original.name),
                width=260,
                anchor="w"
            ).pack(side="left", padx=2)

            # Duplicate File

            duplicate_label = ctk.CTkLabel(
                row,
                text=self.shorten_text(duplicate.name),
                width=260,
                anchor="w"
            )

            duplicate_label.pack(
                side="left",
                padx=2
            )

            duplicate_label.bind(
                "<Button-1>",
                lambda e, p=duplicate: (
                print("PREVIEW BIND:", p),
                self.show_image_preview(p)
            )
        )

            duplicate_label.bind(
                "<Button-3>",
                lambda e, p=duplicate: self.show_context_menu(e, p)
            )

            # Size

            try:
                size_mb = os.path.getsize(duplicate) / (1024 * 1024)
                size_text = f"{size_mb:.2f} MB"

            except Exception:
                size_text = "-"

            ctk.CTkLabel(
                row,
                text=size_text,
                width=90
            ).pack(side="left")

            # Extension

            ctk.CTkLabel(
                row,
                text=duplicate.suffix.replace(".", "").upper(),
                width=80
            ).pack(side="left")

            # Open Folder

            ctk.CTkButton(
                row,
                text="📂",
                width=40,
                command=lambda p=duplicate: os.startfile(str(p.parent))
            ).pack(side="left", padx=5)

        # ==========================================
        # Update Count
        # ==========================================

        self.count_label.configure(
            text=f"Found {len(self.duplicates)} Duplicate Files"
        )

        self.update_status()

        total_size = 0

        for _, duplicate in self.duplicates:

            try:
                total_size += os.path.getsize(duplicate)

            except:
                pass

        if len(self.selected_files) == 0:

            self.delete_btn.configure(
                text="🗑 Delete Selected",
                state="normal"
            )

        else:

            self.delete_btn.configure(
                text=f"🗑 Delete ({len(self.selected_files)})",
                state="normal"
            )    

        total_size = total_size / (1024 * 1024)

    def update_progress(self, current, total):

        if total <= 0:
            self.progress_bar.set(0)
            self.progress_label.configure(text="Ready")
            return

        progress = current / total

        self.progress_bar.set(progress)

        self.progress_label.configure(
            text=f"{len(self.duplicates)} Duplicates Found"
        )

        self.update()    

           
    # ==========================
    # Show Right Click Menu
    # ==========================

    def show_context_menu(self, event, file_path):

        self.current_file = file_path

        self.context_menu.post(
            event.x_root,
            event.y_root
        )

    def open_file(self):

        try:
            os.startfile(str(self.current_file))

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
        )

    def open_folder(self):

        try:

            os.startfile(
                str(self.current_file.parent)
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def copy_full_path(self):

        try:

            self.clipboard_clear()

            self.clipboard_append(
                str(self.current_file)
            )

            self.update()

            messagebox.showinfo(
                "Copied",
                "File path copied to clipboard."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )
            
    def delete_context_file(self):

        confirm = messagebox.askyesno(
            "Delete File",
            f"Delete:\n\n{self.current_file.name} ?"
        )

        if not confirm:
            return

        try:

            send2trash(str(self.current_file))

            self.duplicates = [
                pair
                for pair in self.duplicates
                if pair[1] != self.current_file
            ]

            self.refresh_list()

            messagebox.showinfo(
                "Deleted",
                "File deleted successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )                        

    # ==========================================
    # Toggle Selection
    # ==========================================

    def toggle_selection(self, file_path, row):

        if file_path in self.selected_files:

            self.selected_files.remove(file_path)

        else:

            self.selected_files.append(file_path)

        print("Selected Files:", len(self.selected_files))

        self.update_status()
    # ==========================================
    # Select All
    # ==========================================

    def select_all(self):

        self.selected_files.clear()

        for checkbox, file_path in self.checkboxes:
            checkbox.select()

            if file_path not in self.selected_files:
                self.selected_files.append(file_path)

        self.update_status()        

    # ==========================================
    # Clear Selection
    # ==========================================

    def clear_selection(self):

        self.selected_files.clear()

        for checkbox, _ in self.checkboxes:
            checkbox.deselect()

        self.update_status()    

    # ==========================
    # Update Status
    # ==========================

    def update_status(self):

        total = len(self.duplicates)
        selected = len(self.selected_files)

        total_size = 0
        selected_size = 0

        for _, duplicate in self.duplicates:

            try:
                size = os.path.getsize(duplicate)

                total_size += size

                if duplicate in self.selected_files:
                    selected_size += size

            except:
                pass

        self.total_label.configure(
            text=f"Total: {total}"
        )

        self.selected_label.configure(
            text=f"Selected: {selected}"
        )

        self.size_label.configure(
            text=f"Size: {total_size / (1024*1024):.2f} MB"
        )    

        self.status_label.configure(
            text=(
                f"Total: {total}    "
                f"Selected: {selected}    "
                f"Size: {total_size / (1024*1024):.2f} MB    "
                f"Selected Size: {selected_size / (1024*1024):.2f} MB"
            )
        )

        if selected == 0:

            self.delete_btn.configure(
                text="🗑 Delete Selected",
                state="disabled"
            )

        else:

            self.delete_btn.configure(
                text=f"🗑 Delete ({selected})",
                state="normal"
            )

            print(
                f"UI -> Total:{total}, Selected:{selected}"
        )
    # ==========================================
    # Search
    # ==========================================

    def search_duplicates(self, event=None):

        keyword = self.search_entry.get().lower().strip()

        if keyword == "":
            self.duplicates = self.all_duplicates.copy()

        else:
            self.duplicates = [
                pair
                for pair in self.all_duplicates
                if keyword in pair[0].name.lower()
                or keyword in pair[1].name.lower()
            ]

        self.refresh_list()

    # ==========================================
    # Sort
    # ==========================================

    def sort_duplicates(self, option):

        if option == "Name":

            self.duplicates.sort(
                key=lambda x: x[1].name.lower()
            )

        elif option == "Size":

            self.duplicates.sort(
                key=lambda x: os.path.getsize(x[1])
            )

        elif option == "Extension":

            self.duplicates.sort(
                key=lambda x: x[1].suffix.lower()
            )

        self.refresh_list()

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
            "Move to Recycle Bin",
            f"Are you sure you want to move\n\n"
            f"{len(self.selected_files)} selected duplicate file(s)\n\n"
            f"to Recycle Bin?"
)

        if not confirm:
            return

        deleted = 0
        deleted_files = []

        for file_path in self.selected_files:

            try:

                send2trash(str(file_path))

                deleted += 1
                deleted_files.append(file_path)

            except Exception as e:

                messagebox.showerror(
                    "Delete Error",
                    str(e)
                )

        self.selected_files.clear()

        self.duplicates = [
            pair
            for pair in self.duplicates
            if pair[1] not in deleted_files
        ]

        self.all_duplicates = [
            pair
            for pair in self.all_duplicates
            if pair[1] not in deleted_files
        ]

        self.refresh_list()

        messagebox.showinfo(
            "Completed",
            f"Successfully moved {deleted} file(s) to Recycle Bin."
)

        # ==========================================
        # Export CSV
        # ==========================================

    def export_csv(self):

        if not self.duplicates:

            messagebox.showwarning(
                "No Data",
                "No duplicate files to export."
            )
            return

        file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ],
            initialfile="Duplicate_Report.csv"
        )

        if not file:
            return

        try:

            with open(
                file,
                "w",
                newline="",
                encoding="utf-8"
            ) as csvfile:

                writer = csv.writer(csvfile)

                writer.writerow([
                    "Original File",
                    "Duplicate File",
                    "Size (MB)",
                    "Extension"
                ])

                for original, duplicate in self.duplicates:

                    try:
                        size = os.path.getsize(duplicate)
                        size = round(size / (1024 * 1024), 2)

                    except Exception:
                        size = "-"

                    writer.writerow([
                        original,
                        duplicate,
                        size,
                        duplicate.suffix
                    ])

            messagebox.showinfo(
                "Export Complete",
                "Duplicate report exported successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Export Failed",
                str(e)
            )

    def show_image_preview(self, file_path):

        print("PREVIEW CLICKED:", file_path)

        try:

            image = Image.open(file_path)

            width, height = image.size

            size_mb = os.path.getsize(file_path) / (1024 * 1024)

            file_type = file_path.suffix.upper()

            modified = datetime.datetime.fromtimestamp(
                os.path.getmtime(file_path)
            ).strftime("%d-%b-%Y %H:%M")

            image.thumbnail((220, 220))

            preview = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )

            self.preview_label.configure(
                image=preview,
                text=""
            )

            self.preview_label.image = preview

            self.preview_info.configure(
                text=
                f"File: {file_path.name}\n\n"
                f"Size: {size_mb:.2f} MB\n"
                f"Type: {file_type}\n"
                f"Resolution: {width} × {height}\n"
                f"Modified: {modified}"
            )

        except Exception as e:

            print("PREVIEW ERROR:", e)

            self.preview_label.configure(
                image=None,
                text="Preview not available"
            )

            self.preview_info.configure(text="")

    def auto_select_duplicates(self):

        self.selected_files.clear()

        for checkbox, duplicate in self.checkboxes:

            checkbox.select()

            if duplicate not in self.selected_files:
                self.selected_files.append(duplicate)

        self.update_status()

        self.delete_btn.configure(
            text=f"🗑 Delete ({len(self.selected_files)})",
            state="normal"
        )

    def get_largest_duplicate(self):

        largest = 0

        for _, duplicate in self.duplicates:

            try:
                size = os.path.getsize(duplicate)

                if size > largest:
                    largest = size

            except:
                pass

        return largest / (1024 * 1024)

    def get_file_statistics(self):

        images = 0
        documents = 0
        videos = 0

        image_ext = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
        doc_ext = {".pdf", ".doc", ".docx", ".txt"}
        video_ext = {".mp4", ".avi", ".mkv", ".mov"}

        for _, duplicate in self.duplicates:

            ext = duplicate.suffix.lower()

            if ext in image_ext:
                images += 1

            elif ext in doc_ext:
                documents += 1

            elif ext in video_ext:
                videos += 1

        return images, documents, videos 

    def on_close(self):

        self.parent.deiconify()
        self.destroy()   