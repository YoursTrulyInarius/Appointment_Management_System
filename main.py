import tkinter as tk
from tkinter import ttk, messagebox
import database
from datetime import datetime

class AppointmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Management Application")
        self.root.geometry("1100x660")
        self.root.configure(bg="#f8f9fa")

        # Variables
        self.name_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.service_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.selected_id = None

        # Set real-time defaults
        self.set_defaults()

        self.setup_ui()
        self.refresh_table()

    def set_defaults(self):
        now = datetime.now()
        self.date_var.set(now.strftime("%m/%d/%Y"))   # e.g. 02/28/2026
        self.time_var.set(now.strftime("%I:%M %p"))   # e.g. 07:10 PM

    # ─────────────────────────────────────────────
    # Parsing helpers
    # ─────────────────────────────────────────────
    def parse_date(self, date_str):
        """
        Accept multiple input formats and return (datetime_obj, None) or (None, error_msg).
        Accepted: M/D/YY, M/D/YYYY, MM/DD/YY, MM/DD/YYYY, YYYY-MM-DD
        """
        date_str = date_str.strip()
        formats = [
            "%m/%d/%Y",   # 02/28/2026
            "%m/%d/%y",   # 02/28/26
            "%-m/%-d/%Y", # 2/28/2026  (non-padded on Linux)
            "%Y-%m-%d",   # 2026-02-28
        ]
        # Normalise slashed shorthand (handles 2/12/26 or 2/12/2026)
        parts = date_str.split("/")
        if len(parts) == 3:
            m, d, y = parts[0].zfill(2), parts[1].zfill(2), parts[2]
            if len(y) == 2:
                y = "20" + y
            date_str = f"{m}/{d}/{y}"
            formats = ["%m/%d/%Y"]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt), None
            except ValueError:
                continue
        return None, (
            "Invalid date format.\n\n"
            "Accepted formats:\n"
            "  • M/D/YY  (e.g. 2/12/26)\n"
            "  • MM/DD/YYYY  (e.g. 02/12/2026)\n"
            "  • YYYY-MM-DD  (e.g. 2026-02-12)"
        )

    def parse_time(self, time_str):
        """
        Accept 12-h or 24-h strings and return (datetime_obj, None) or (None, error_msg).
        Accepted: H:MM, HH:MM (24-h), H:MM AM/PM, HH:MM AM/PM
        """
        time_str = time_str.strip()
        formats = [
            "%I:%M %p",  # 07:10 PM
            "%I:%M%p",   # 07:10PM
            "%H:%M",     # 19:10
        ]
        for fmt in formats:
            try:
                return datetime.strptime(time_str.upper(), fmt), None
            except ValueError:
                continue
        return None, (
            "Invalid time format.\n\n"
            "Accepted formats:\n"
            "  • H:MM AM/PM  (e.g. 2:30 PM)\n"
            "  • HH:MM AM/PM  (e.g. 07:10 AM)\n"
            "  • HH:MM  24-h  (e.g. 14:30)"
        )

    # ─────────────────────────────────────────────
    # Display formatters (for the table)
    # ─────────────────────────────────────────────
    @staticmethod
    def format_date_display(date_db):
        """YYYY-MM-DD  →  Month DD, YYYY"""
        try:
            dt = datetime.strptime(date_db, "%Y-%m-%d")
            return dt.strftime("%B %d, %Y")   # February 12, 2026
        except ValueError:
            return date_db

    @staticmethod
    def format_time_display(time_db):
        """HH:MM (24-h)  →  H:MM AM/PM"""
        try:
            dt = datetime.strptime(time_db, "%H:%M")
            return dt.strftime("%I:%M %p").lstrip("0")  # e.g. 7:10 PM
        except ValueError:
            return time_db

    # ─────────────────────────────────────────────
    # UI setup
    # ─────────────────────────────────────────────
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="APPOINTMENT MANAGEMENT SYSTEM",
            font=("Segoe UI", 24, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            pady=20
        ).pack()

        # Main Container
        main_frame = tk.Frame(self.root, bg="#f8f9fa", padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Frame: Input Form
        form_frame = tk.LabelFrame(
            main_frame,
            text=" Appointment Entry Form ",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            padx=15, pady=15,
            relief=tk.RIDGE
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Input Fields
        tk.Label(form_frame, text="Client Name:", bg="#ffffff", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=self.name_var, font=("Segoe UI", 10),
                 width=35, relief=tk.SOLID).grid(row=0, column=1, pady=10, padx=5)

        tk.Label(form_frame, text="Date (M/D/YY or MM/DD/YYYY):", bg="#ffffff",
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=self.date_var, font=("Segoe UI", 10),
                 width=35, relief=tk.SOLID).grid(row=1, column=1, pady=10, padx=5)

        tk.Label(form_frame, text="Time (e.g. 2:30 PM or 14:30):", bg="#ffffff",
                 font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=self.time_var, font=("Segoe UI", 10),
                 width=35, relief=tk.SOLID).grid(row=2, column=1, pady=10, padx=5)

        tk.Label(form_frame, text="Service Type:", bg="#ffffff",
                 font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", pady=10)
        services = ["Consultation", "Repair", "Maintenance", "Consulting",
                    "Check-up", "Follow-up", "Other"]
        self.service_combo = ttk.Combobox(
            form_frame, textvariable=self.service_var,
            values=services, font=("Segoe UI", 10), width=33, state="readonly"
        )
        self.service_combo.grid(row=3, column=1, pady=10, padx=5)

        tk.Label(form_frame, text="Contact No. (11 digits):", bg="#ffffff",
                 font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", pady=10)
        self.contact_entry = tk.Entry(
            form_frame, textvariable=self.contact_var,
            font=("Segoe UI", 10), width=35, relief=tk.SOLID
        )
        self.contact_entry.grid(row=4, column=1, pady=10, padx=5)
        self.contact_var.trace_add("write", self.validate_contact_input)

        # Buttons Frame
        btn_frame = tk.Frame(form_frame, bg="#ffffff", pady=20)
        btn_frame.grid(row=5, column=0, columnspan=2)

        tk.Button(btn_frame, text="ADD RECORD",   command=self.add_record,
                  bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"),
                  width=18, relief=tk.FLAT).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="UPDATE",       command=self.update_record,
                  bg="#2980b9", fg="white", font=("Segoe UI", 10, "bold"),
                  width=18, relief=tk.FLAT).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="DELETE",       command=self.delete_record,
                  bg="#c0392b", fg="white", font=("Segoe UI", 10, "bold"),
                  width=18, relief=tk.FLAT).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="CLEAR FIELDS", command=self.clear_fields,
                  bg="#7f8c8d", fg="white", font=("Segoe UI", 10, "bold"),
                  width=18, relief=tk.FLAT).grid(row=1, column=1, padx=5, pady=5)

        # Right Frame: Search and Table
        display_frame = tk.Frame(main_frame, bg="#f8f9fa")
        display_frame.grid(row=0, column=1, sticky="nsew")

        # Search Section
        search_frame = tk.Frame(display_frame, bg="#f8f9fa")
        search_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(search_frame, text="Search Record:", bg="#f8f9fa",
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 10),
                 width=25, relief=tk.SOLID).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="SEARCH",   command=self.search_record,
                  bg="#f39c12", fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="SHOW ALL", command=self.refresh_table,
                  bg="#2c3e50", fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)

        # Table Section
        table_frame = tk.Frame(display_frame, bg="white", relief=tk.RIDGE, borderwidth=1)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "date", "time", "service", "contact")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("id",      text="ID")
        self.tree.heading("name",    text="CLIENT NAME")
        self.tree.heading("date",    text="DATE")
        self.tree.heading("time",    text="TIME")
        self.tree.heading("service", text="SERVICE")
        self.tree.heading("contact", text="CONTACT NO.")

        self.tree.column("id",      width=0,   stretch=tk.NO)
        self.tree.column("name",    width=180, anchor="center")
        self.tree.column("date",    width=160, anchor="center")
        self.tree.column("time",    width=100, anchor="center")
        self.tree.column("service", width=120, anchor="center")
        self.tree.column("contact", width=120, anchor="center")

        self.tree["displaycolumns"] = ("name", "date", "time", "service", "contact")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.get_selected_row)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    # ─────────────────────────────────────────────
    # Validation helpers
    # ─────────────────────────────────────────────
    def validate_contact_input(self, *args):
        """Ensure contact number is numeric and capped at 11 digits."""
        value = self.contact_var.get()
        filtered = "".join(filter(str.isdigit, value))[:11]
        if value != filtered:
            self.contact_var.set(filtered)

    def validate_inputs(self, is_update=False):
        """Return (date_db, time_db) tuple on success, or (None, None) on failure."""
        name    = self.name_var.get().strip()
        date_in = self.date_var.get().strip()
        time_in = self.time_var.get().strip()
        service = self.service_var.get().strip()
        contact = self.contact_var.get().strip()

        # ── required fields ──
        if not all([name, date_in, time_in, service, contact]):
            messagebox.showwarning(
                "Incomplete Form",
                "Please fill in all fields before submitting.\nBlank entries are not allowed."
            )
            return None, None

        # ── name: letters and spaces only ──
        if not all(c.isalpha() or c.isspace() for c in name):
            messagebox.showwarning(
                "Validation Error",
                "Client name must contain letters and spaces only.\nNumbers and special characters are not allowed."
            )
            return None, None

        # ── name length ──
        if len(name) < 2:
            messagebox.showwarning(
                "Validation Error",
                "Client name must be at least 2 characters long."
            )
            return None, None

        # ── contact ──
        if len(contact) != 11:
            messagebox.showwarning(
                "Validation Error",
                "Contact number must be exactly 11 digits."
            )
            return None, None

        if not contact.startswith("0"):
            messagebox.showwarning(
                "Validation Error",
                "Contact number must start with 0 (e.g. 09171234567)."
            )
            return None, None

        # ── date ──
        date_obj, date_err = self.parse_date(date_in)
        if date_err:
            messagebox.showwarning("Invalid Date", date_err)
            return None, None

        # ── time ──
        time_obj, time_err = self.parse_time(time_in)
        if time_err:
            messagebox.showwarning("Invalid Time", time_err)
            return None, None

        # Normalised DB values
        date_db = date_obj.strftime("%Y-%m-%d")
        time_db = time_obj.strftime("%H:%M")

        # ── duplicate check ──
        exclude_id = self.selected_id if is_update else None
        try:
            if database.is_duplicate(name, date_db, time_db, contact, exclude_id):
                messagebox.showwarning(
                    "Duplicate Entry",
                    f"An appointment already exists for:\n\n"
                    f"  Name:    {name}\n"
                    f"  Date:    {self.format_date_display(date_db)}\n"
                    f"  Time:    {self.format_time_display(time_db)}\n"
                    f"  Contact: {contact}\n\n"
                    "Please change at least one of these values."
                )
                return None, None
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not check for duplicates:\n{e}")
            return None, None

        return date_db, time_db

    # ─────────────────────────────────────────────
    # CRUD operations
    # ─────────────────────────────────────────────
    def add_record(self):
        date_db, time_db = self.validate_inputs()
        if date_db is None:
            return
        try:
            name    = self.name_var.get().strip()
            service = self.service_var.get().strip()
            contact = self.contact_var.get().strip()
            success = database.add_appointment(name, date_db, time_db, service, contact)
            if success:
                messagebox.showinfo("Success", "Appointment successfully scheduled!")
                self.clear_fields()
                self.refresh_table()
        except Exception as e:
            messagebox.showerror("System Error", f"An unexpected error occurred:\n{e}")

    def update_record(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Update Error",
                "Please select a record from the table to update."
            )
            return

        date_db, time_db = self.validate_inputs(is_update=True)
        if date_db is None:
            return

        if messagebox.askyesno("Confirm Update", "Modify this appointment record?"):
            try:
                success = database.update_appointment(
                    self.selected_id,
                    self.name_var.get().strip(),
                    date_db, time_db,
                    self.service_var.get().strip(),
                    self.contact_var.get().strip()
                )
                if success:
                    messagebox.showinfo("Success", "Record successfully updated!")
                    self.clear_fields()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("System Error", f"An unexpected error occurred:\n{e}")

    def delete_record(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Delete Error",
                "Please select a record from the table to delete."
            )
            return

        if messagebox.askyesno("Confirm Deletion",
                                "Are you sure you want to permanently remove this record?"):
            try:
                success = database.delete_appointment(self.selected_id)
                if success:
                    messagebox.showinfo("Success", "Record successfully deleted!")
                    self.clear_fields()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("System Error", f"An unexpected error occurred:\n{e}")

    # ─────────────────────────────────────────────
    # Table population
    # ─────────────────────────────────────────────
    def get_selected_row(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        data = self.tree.item(selected_item)["values"]
        if not data:
            return

        # data columns: id, name, date_display, time_display, service, contact
        self.selected_id = data[0]
        self.name_var.set(data[1])

        # Convert display date (February 12, 2026) → editable (02/12/2026)
        try:
            dt = datetime.strptime(str(data[2]), "%B %d, %Y")
            self.date_var.set(dt.strftime("%m/%d/%Y"))
        except ValueError:
            self.date_var.set(str(data[2]))

        # Convert display time (7:10 PM) → editable (07:10 PM)
        try:
            t = datetime.strptime(str(data[3]).strip(), "%I:%M %p")
            self.time_var.set(t.strftime("%I:%M %p"))
        except ValueError:
            self.time_var.set(str(data[3]))

        self.service_var.set(data[4])
        self.contact_var.set(data[5])

    def search_record(self):
        query = self.search_var.get().strip()
        if not query:
            self.refresh_table()
            return
        rows = database.search_appointments(query)
        self.populate_table(rows)

    def refresh_table(self):
        try:
            rows = database.view_appointments()
            self.populate_table(rows)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load records:\n{e}")

    def populate_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            # row = (id, name, date_db, time_db, service, contact)
            rid, name, date_db, time_db, service, contact = row
            date_display = self.format_date_display(date_db)
            time_display = self.format_time_display(time_db)
            self.tree.insert("", tk.END, values=(rid, name, date_display, time_display, service, contact))

    def clear_fields(self):
        self.name_var.set("")
        self.set_defaults()          # Reset to real-time date/time
        self.service_var.set("")
        self.contact_var.set("")
        self.search_var.set("")
        self.service_combo.set("")
        self.selected_id = None
        self.tree.selection_remove(self.tree.selection())


if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentApp(root)
    root.mainloop()
