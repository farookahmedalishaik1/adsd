import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def _connect(self):
        """Establish a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Allow access to rows by column name
        return conn

    def init_db(self):
        """Initialize the database with necessary tables."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    owner TEXT NOT NULL
                )
            """)
            conn.commit()

    def get_all_vehicles(self):
        """Fetch all vehicles."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles")
            return cursor.fetchall()

    def add_vehicle(self, make, model, owner):
        """Add a new vehicle."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vehicles (make, model, owner) 
                VALUES (?, ?, ?)
            """, (make, model, owner))
            conn.commit()

    def get_vehicle_by_id(self, vehicle_id):
        """Fetch a vehicle by ID."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
            return cursor.fetchone()

    def update_vehicle(self, vehicle_id, make, model, owner):
        """Update an existing vehicle."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE vehicles
                SET make = ?, model = ?, owner = ?
                WHERE id = ?
            """, (make, model, owner, vehicle_id))
            conn.commit()

    def delete_vehicle(self, vehicle_id):
        """Delete a vehicle."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
            conn.commit()
