# Appointment Management System

> [!IMPORTANT]
> This system is currently **UNDER PRODUCTION**.

A robust desktop application for managing appointments, developed using Python and Tkinter.

## Developer
Developed by: **Sonjeev C. Cabardo**

## Features

### 📅 Appointment Entry
- Add new client appointments with smart date and time defaults set to the current date and time.

### 📋 Record Management
- **Update** — Modify existing appointment records.
- **Delete** — Remove cancelled or completed appointments with confirmation.
- **Clear Fields** — Instantly reset the form for a new entry.

### 🔍 Search Functionality
- Search records by **client name**, **service type**, or **contact number**.
- Use **Show All** to restore the full record list.

### ✅ Data Validation
- All fields are required — blank entries are blocked.
- **Client name** must contain letters and spaces only (minimum 2 characters).
- **Contact number** must be exactly 11 digits and start with `0` (e.g. `09171234567`).
- Real-time input filtering prevents non-numeric characters in the contact field.

### 📆 Flexible Date Input & Auto-Translation
Dates are accepted in multiple formats and automatically displayed in full readable form:

| Input | Stored As | Displayed As |
|-------|-----------|--------------|
| `2/12/26` | `2026-02-12` | February 12, 2026 |
| `02/12/2026` | `2026-02-12` | February 12, 2026 |
| `2026-02-12` | `2026-02-12` | February 12, 2026 |

### 🕐 Flexible Time Input with AM/PM
Times are accepted in 12-hour or 24-hour format and always displayed with AM/PM:

| Input | Stored As | Displayed As |
|-------|-----------|--------------|
| `2:30 PM` | `14:30` | 2:30 PM |
| `07:10 AM` | `07:10` | 7:10 AM |
| `14:30` | `14:30` | 2:30 PM |
| `19:10` | `19:10` | 7:10 PM |

### 🚫 Duplicate Prevention
- Detects duplicates by matching **name + date + time + contact** (normalized before comparison).
- Displays a detailed warning showing the formatted date and time of the conflicting record.
- Update mode intelligently excludes the currently selected record from the duplicate check.

### 🛡️ Error Handling
- All database operations are wrapped with error handling and user-friendly messages.
- Invalid date or time formats show a popup listing all accepted formats.
- System-level errors are caught and reported without crashing the application.

### 💾 Database Integration
- Uses SQLite for lightweight, persistent local storage.
- Database and table are created automatically on first run.

---

## Tech Stack
| Layer | Technology |
|-------|------------|
| Language | Python 3 |
| GUI Framework | Tkinter / ttk |
| Database | SQLite3 |

---

## Getting Started

### Prerequisites
- Python 3 installed on your system.

### Installation & Running
1. Clone or download the project files.
2. Navigate to the project directory.
3. Run the application:
   ```bash
   python main.py
   ```

---

## Project Structure
| File | Description |
|------|-------------|
| `main.py` | Entry point — contains all UI logic, input parsing, and validation. |
| `database.py` | Handles all SQLite database operations (CRUD + duplicate checks). |
| `appointments.db` | SQLite database file — created automatically on first run. |
