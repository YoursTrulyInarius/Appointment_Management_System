import sqlite3
from tkinter import messagebox

DB_NAME = "appointments.db"

def connect_db():
    """Connect to the SQLite database and create the table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                service TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        """)
        conn.commit()
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

def add_appointment(name, date, time, service, contact):
    """Add a new appointment record."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointments (name, date, time, service, contact)
                VALUES (?, ?, ?, ?, ?)
            """, (name, date, time, service, contact))
            conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding record: {e}")
            return False
        finally:
            conn.close()
    return False

def view_appointments():
    """Retrieve all appointment records."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointments")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching records: {e}")
            return []
        finally:
            conn.close()
    return []

def update_appointment(record_id, name, date, time, service, contact):
    """Update an existing appointment record."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE appointments
                SET name = ?, date = ?, time = ?, service = ?, contact = ?
                WHERE id = ?
            """, (name, date, time, service, contact, record_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error updating record: {e}")
            return False
        finally:
            conn.close()
    return False

def delete_appointment(record_id):
    """Delete an appointment record."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM appointments WHERE id = ?", (record_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting record: {e}")
            return False
        finally:
            conn.close()
    return False

def is_duplicate(name, date, time, contact, exclude_id=None):
    """Check if an appointment with the same name, date, and time already exists."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT id FROM appointments WHERE name = ? AND date = ? AND time = ? AND contact = ?"
            params = [name, date, time, contact]
            if exclude_id:
                query += " AND id != ?"
                params.append(exclude_id)
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error checking for duplicates: {e}")
            return False
        finally:
            conn.close()
    return False

def search_appointments(query):
    """Search for appointments by name or service."""
    if not query.strip():
        return view_appointments()
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # searching by name or service (case-insensitive)
            search_query = f"%{query.strip()}%"
            cursor.execute("""
                SELECT * FROM appointments 
                WHERE name LIKE ? OR service LIKE ? OR contact LIKE ?
            """, (search_query, search_query, search_query))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error searching records: {e}")
            return []
        finally:
            conn.close()
    return []

# Initialize DB on import
if __name__ == "__main__":
    connect_db()
