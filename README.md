# Appointment Management System

> [!IMPORTANT]
> This system is currently **UNDER PRODUCTION**.
> Added proper error handling.

A robust desktop application for managing appointments, developed using Python and Tkinter.

## Developer
Developed by: **Sonjeev C. Cabardo**

## Features
- **Appointment Entry**: Easily add new client appointments with real-time date and time defaults.
- **Record Management**: 
    - **Update**: Modify existing appointments.
    - **Delete**: Remove cancelled or completed appointments.
    - **Clear Fields**: Quickly reset the form for new entries.
- **Search Functionality**: Search for records by client name, service type, or contact number.
- **Data Validation**:
    - Ensures all fields are filled.
    - Validates contact number format (strictly 11 digits).
    - Prevents duplicate entries based on name, date, and contact.
- **Database Integration**: Uses SQLite for persistent storage.

## Tech Stack
- **Language**: Python 3
- **GUI Framework**: Tkinter / ttk
- **Database**: SQLite3

## Getting Started

### Prerequisites
- Python installed on your system.

### Installation & Running
1. Clone or download the project files.
2. Navigate to the project directory.
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure
- `main.py`: The entry point of the application containing the UI logic.
- `database.py`: Handles all database operations and connections.
- `appointments.db`: SQLite database file (created automatically on first run).
