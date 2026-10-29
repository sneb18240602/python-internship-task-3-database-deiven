"""
Task 4: Database-Driven Management System
Author: sneb18240602
Description: Replaces file storage with an SQLite relational database.
             Manages Users and Records with SQL queries and relational linking.
"""

import sqlite3

DATABASE_NAME = "management_system.db"


def init_db():
    """Initializes the SQLite database with Users and Records relational tables."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'Active'
        )
    """)

    # Create Records table with a foreign key to users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            record_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL,
            user_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # Seed initial sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO users (user_id, name, role, status)
            VALUES (?, ?, ?, ?)
        """, [
            ("U001", "Arun", "Donor", "Active"),
            ("U002", "Priya", "Volunteer", "Active")
        ])

    cursor.execute("SELECT COUNT(*) FROM records")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO records (record_id, name, quantity, status, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("FD001", "Vegetable Rice", 20, "Available", "U001"),
            ("FD002", "Bread", 10, "Claimed", "U002")
        ])

    conn.commit()
    conn.close()


class DatabaseManager:
    """Handles CRUD operations using SQLite."""
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        print("Database Connected")
        return conn

    def display_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, role FROM users")
        rows = cursor.fetchall()
        conn.close()

        print("\nUsers")
        print("-----")
        for r in rows:
            print(f"{r[0]} | {r[1]} | {r[2]}")

    def display_records(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT record_id, name, quantity, status FROM records")
        rows = cursor.fetchall()
        conn.close()

        print("\nRecords")
        print("-------")
        for r in rows:
            print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")

    def display_status_summary(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM records WHERE LOWER(status) = 'available'")
        avail_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM records WHERE LOWER(status) = 'claimed'")
        claimed_count = cursor.fetchone()[0]
        conn.close()

        print(f"\nAvailable Records: {avail_count}")
        print(f"Claimed Records: {claimed_count}")

    def add_record(self, record_id, name, quantity, status, user_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO records (record_id, name, quantity, status, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (record_id, name, quantity, status, user_id))
        conn.commit()
        conn.close()
        print(f"Record {record_id} inserted successfully.")


def main():
    init_db()
    db = DatabaseManager()

    # Show matching sample output from the challenge prompt
    db.display_users()
    db.display_records()
    db.display_status_summary()

    while True:
        print("\n=== Database Record Management ===")
        print("1. View Users")
        print("2. View Records")
        print("3. View Summary Counts")
        print("4. Add Record")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            db.display_users()
        elif choice == "2":
            db.display_records()
        elif choice == "3":
            db.display_status_summary()
        elif choice == "4":
            r_id = input("Enter Record ID (e.g., FD003): ").strip()
            name = input("Enter Item Name: ").strip()
            qty = int(input("Enter Quantity: ").strip() or "0")
            stat = input("Enter Status (Available/Claimed): ").strip()
            db.add_record(r_id, name, qty, stat)
        elif choice == "5":
            print("Exiting application.")
            break
        else:
            print("Invalid option. Please choose between 1 and 5.")


if __name__ == "__main__":
    main()
