import customtkinter as ctk

class DuplicateWindow(ctk.CTkToplevel):

    def __init__(self, parent, duplicates):

        super().__init__(parent)

        self.title("Duplicate Manager")
        self.geometry("900x550")

        self.duplicates = duplicates

        self.grab_set()

        # ==========================
        # Title
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="🔍 Duplicate Manager",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(pady=15)

        # ==========================
        # Count
        # ==========================

        count = ctk.CTkLabel(
            self,
            text=f"Found {len(duplicates)} Duplicate Files",
            font=("Segoe UI", 16)
        )

        count.pack(pady=5)

        # ==========================
        # Scrollable Frame
        # ==========================

        self.scroll = ctk.CTkScrollableFrame(
            self,
            width=820,
            height=330
        )

        self.scroll.pack(padx=20, pady=20, fill="both", expand=True)

        # ==========================
        # Heading
        # ==========================

        header = ctk.CTkLabel(
            self.scroll,
            text="Original File                              Duplicate File",
            font=("Consolas", 14, "bold")
        )

        header.pack(anchor="w", pady=(0, 10))

        # ==========================
        # Duplicate List
        # ==========================

        for original, duplicate in duplicates:

            frame = ctk.CTkFrame(self.scroll)

            frame.pack(fill="x", pady=4)

            original_label = ctk.CTkLabel(
                frame,
                text=original.name,
                width=320,
                anchor="w"
            )

            original_label.pack(
                side="left",
                padx=10,
                pady=8
            )

            duplicate_label = ctk.CTkLabel(
                frame,
                text=duplicate.name,
                width=320,
                anchor="w"
            )

            duplicate_label.pack(
                side="left",
                padx=10
            )

        # ==========================
        # Buttons
        # ==========================

        button_frame = ctk.CTkFrame(self)

        button_frame.pack(pady=15)

        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑 Delete Selected",
            width=180,
            state="disabled"
        )

        self.delete_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        self.export_btn = ctk.CTkButton(
            button_frame,
            text="📄 Export CSV",
            width=180,
            state="disabled"
        )

        self.export_btn.grid(
            row=0,
            column=1,
            padx=10
        )

        self.close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            width=150,
            command=self.destroy
        )

        self.close_btn.grid(
            row=0,
            column=2,
            padx=10
        )