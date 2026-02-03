import tkinter as tk
from tkinter import ttk, messagebox
import database
from datetime import datetime

class AppointmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Management Application")
        self.root.geometry("1000x650")
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
        self.date_var.set(now.strftime("%Y-%m-%d"))
        self.time_var.set(now.strftime("%H:%M"))

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="APPOINTMENT MANAGEMENT SYSTEM", font=("Segoe UI", 24, "bold"), bg="#2c3e50", fg="#ecf0f1", pady=20).pack()

        # Main Container
        main_frame = tk.Frame(self.root, bg="#f8f9fa", padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Frame: Input Form
        form_frame = tk.LabelFrame(main_frame, text=" Appointment Entry Form ", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2c3e50", padx=15, pady=15, relief=tk.RIDGE)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Input Fields
        tk.Label(form_frame, text="Client Name:", bg="#ffffff", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=self.name_var, font=("Segoe UI", 10), width=35, relief=tk.SOLID).grid(row=0, column=1, pady=10, padx=5)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#ffffff", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=self.date_var, font=("Segoe UI", 10), width=35, relief=tk.SOLID).grid(row=1, column=1, pady=10, padx=5)

        tk.Label(form_frame, text="Time (HH:MM):", bg="#ffffff", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=self.time_var, font=("Segoe UI", 10), width=35, relief=tk.SOLID).grid(row=2, column=1, pady=10, padx=5)

        tk.Label(form_frame, text="Service Type:", bg="#ffffff", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", pady=10)
        services = ["Consultation", "Repair", "Maintenance", "Consulting", "Check-up", "Follow-up", "Other"]
        self.service_combo = ttk.Combobox(form_frame, textvariable=self.service_var, values=services, font=("Segoe UI", 10), width=33, state="readonly")
        self.service_combo.grid(row=3, column=1, pady=10, padx=5)

        tk.Label(form_frame, text="Contact No. (11 digits):", bg="#ffffff", font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", pady=10)
        self.contact_entry = tk.Entry(form_frame, textvariable=self.contact_var, font=("Segoe UI", 10), width=35, relief=tk.SOLID)
        self.contact_entry.grid(row=4, column=1, pady=10, padx=5)
        # Add trace to contact_var for real-time validation
        self.contact_var.trace_add("write", self.validate_contact_input)

        # Buttons Frame
        btn_frame = tk.Frame(form_frame, bg="#ffffff", pady=20)
        btn_frame.grid(row=5, column=0, columnspan=2)

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)

        tk.Button(btn_frame, text="ADD RECORD", command=self.add_record, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), width=18, relief=tk.FLAT).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="UPDATE", command=self.update_record, bg="#2980b9", fg="white", font=("Segoe UI", 10, "bold"), width=18, relief=tk.FLAT).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="DELETE", command=self.delete_record, bg="#c0392b", fg="white", font=("Segoe UI", 10, "bold"), width=18, relief=tk.FLAT).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="CLEAR FIELDS", command=self.clear_fields, bg="#7f8c8d", fg="white", font=("Segoe UI", 10, "bold"), width=18, relief=tk.FLAT).grid(row=1, column=1, padx=5, pady=5)

        # Right Frame: Search and Table
        display_frame = tk.Frame(main_frame, bg="#f8f9fa")
        display_frame.grid(row=0, column=1, sticky="nsew")

        # Search Section
        search_frame = tk.Frame(display_frame, bg="#f8f9fa")
        search_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(search_frame, text="Search Record:", bg="#f8f9fa", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 10), width=25, relief=tk.SOLID).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="SEARCH", command=self.search_record, bg="#f39c12", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="SHOW ALL", command=self.refresh_table, bg="#2c3e50", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)

        # Table Section
        table_frame = tk.Frame(display_frame, bg="white", relief=tk.RIDGE, borderwidth=1)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "date", "time", "service", "contact")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Define Headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="CLIENT NAME")
        self.tree.heading("date", text="DATE")
        self.tree.heading("time", text="TIME")
        self.tree.heading("service", text="SERVICE")
        self.tree.heading("contact", text="CONTACT NO.")

        # Column settings
        self.tree.column("id", width=0, stretch=tk.NO) # Hidden
        self.tree.column("name", width=180, anchor="center")
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("time", width=80, anchor="center")
        self.tree.column("service", width=120, anchor="center")
        self.tree.column("contact", width=120, anchor="center")

        # Hide ID column completely
        self.tree["displaycolumns"] = ("name", "date", "time", "service", "contact")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.get_selected_row)

        # Grid configuration
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def validate_contact_input(self, *args):
        """Ensure contact number is numeric and limited to 11 digits."""
        value = self.contact_var.get()
        # Filter out non-numeric characters
        filtered_value = "".join(filter(str.isdigit, value))
        # Limit to 11 digits
        if len(filtered_value) > 11:
            filtered_value = filtered_value[:11]
        
        if value != filtered_value:
            self.contact_var.set(filtered_value)

    def get_selected_row(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        data = self.tree.item(selected_item)["values"]
        if data:
            self.selected_id = data[0]
            self.name_var.set(data[1])
            self.date_var.set(data[2])
            self.time_var.set(data[3])
            self.service_var.set(data[4])
            self.contact_var.set(data[5])

    def validate_inputs(self, is_update=False):
        name = self.name_var.get().strip()
        date = self.date_var.get().strip()
        time = self.time_var.get().strip()
        service = self.service_var.get().strip()
        contact = self.contact_var.get().strip()

        if not name or not date or not time or not service or not contact:
            messagebox.showwarning("Incomplete Form", "Please fill in all fields before submitting. Blank entries are not allowed.")
            return False
        
        if len(contact) != 11:
            messagebox.showwarning("Validation Error", "Contact number must be exactly 11 digits.")
            return False
            
        # Check for duplicates
        exclude_id = self.selected_id if is_update else None
        if database.is_duplicate(name, date, time, contact, exclude_id):
            messagebox.showwarning("Duplicate Entry", f"An appointment already exists for '{name}' on {date} at {time} with contact {contact}.")
            return False

        return True

    def add_record(self):
        if self.validate_inputs():
            try:
                success = database.add_appointment(
                    self.name_var.get().strip(),
                    self.date_var.get().strip(),
                    self.time_var.get().strip(),
                    self.service_var.get().strip(),
                    self.contact_var.get().strip()
                )
                if success:
                    messagebox.showinfo("Success", "Appointment successfully scheduled!")
                    self.clear_fields()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("System Error", f"An unexpected error occurred: {e}")

    def update_record(self):
        if not self.selected_id:
            messagebox.showwarning("Update Error", "Please select a record from the table to update.")
            return
        
        if self.validate_inputs(is_update=True):
            if messagebox.askyesno("Confirm Update", "Modify this appointment record?"):
                success = database.update_appointment(
                    self.selected_id,
                    self.name_var.get().strip(),
                    self.date_var.get().strip(),
                    self.time_var.get().strip(),
                    self.service_var.get().strip(),
                    self.contact_var.get().strip()
                )
                if success:
                    messagebox.showinfo("Success", "Record successfully updated!")
                    self.refresh_table()

    def delete_record(self):
        if not self.selected_id:
            messagebox.showwarning("Delete Error", "Please select a record from the table to delete.")
            return
        
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to permanently remove this record?"):
            success = database.delete_appointment(self.selected_id)
            if success:
                messagebox.showinfo("Success", "Record successfully deleted!")
                self.clear_fields()
                self.refresh_table()

    def search_record(self):
        query = self.search_var.get().strip()
        if not query:
            self.refresh_table()
            return
        
        rows = database.search_appointments(query)
        self.populate_table(rows)

    def refresh_table(self):
        rows = database.view_appointments()
        self.populate_table(rows)

    def populate_table(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_fields(self):
        self.name_var.set("")
        self.set_defaults() # Reset to real-time date/time
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
