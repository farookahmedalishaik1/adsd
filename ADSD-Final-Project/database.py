import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def _connect(self):
        """Establish a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # This allows us to access rows by column name
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    service_date TEXT NOT NULL,
                    service_type TEXT NOT NULL,
                    cost REAL NOT NULL,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
                )
            """)
            conn.commit()

    def get_all_vehicles(self):
        """Fetch all vehicles from the database."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles")
            return cursor.fetchall()

    def add_vehicle(self, make, model, owner):
        """Add a new vehicle to the database."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vehicles (make, model, owner) 
                VALUES (?, ?, ?)
            """, (make, model, owner))
            conn.commit()

    def get_vehicle_by_id(self, vehicle_id):
        """Fetch a vehicle by its ID."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
            return cursor.fetchone()

    def update_vehicle(self, vehicle_id, make, model, owner):
        """Update the details of an existing vehicle."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE vehicles 
                SET make = ?, model = ?, owner = ? 
                WHERE id = ?
            """, (make, model, owner, vehicle_id))
            conn.commit()

    def delete_vehicle(self, vehicle_id):
        """Delete a vehicle from the database."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
            conn.commit()

    def get_maintenance_records_by_vehicle(self, vehicle_id):
        """Fetch all maintenance records for a specific vehicle."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM maintenance WHERE vehicle_id = ?", (vehicle_id,))
            return cursor.fetchall()

    def add_maintenance_record(self, vehicle_id, service_date, service_type, cost):
        """Add a maintenance record for a specific vehicle."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO maintenance (vehicle_id, service_date, service_type, cost) 
                VALUES (?, ?, ?, ?)
            """, (vehicle_id, service_date, service_type, cost))
            conn.commit()

# Create a Database instance
db = Database()
