import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self._connect() as conn:
            cursor = conn.cursor()

            # Vehicles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicles (
                    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_name TEXT NOT NULL,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    last_service_date TEXT
                )
            """)

            # MaintenanceRecords table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    service_date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    cost REAL NOT NULL,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
                )
            """)
            conn.commit()

    def add_vehicle(self, owner_name, make, model, year):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vehicles (owner_name, make, model, year)
                VALUES (?, ?, ?, ?)
            """, (owner_name, make, model, year))
            conn.commit()

    def get_all_vehicles(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles")
            return cursor.fetchall()

    def get_vehicle(self, vehicle_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles WHERE vehicle_id = ?", (vehicle_id,))
            return cursor.fetchone()

    def update_vehicle(self, vehicle_id, owner_name, make, model, year):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE vehicles
                SET owner_name = ?, make = ?, model = ?, year = ?
                WHERE vehicle_id = ?
            """, (owner_name, make, model, year, vehicle_id))
            conn.commit()

    def delete_vehicle(self, vehicle_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vehicles WHERE vehicle_id = ?", (vehicle_id,))
            conn.commit()

    def add_maintenance_record(self, vehicle_id, service_date, description, cost):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO maintenance_records (vehicle_id, service_date, description, cost)
                VALUES (?, ?, ?, ?)
            """, (vehicle_id, service_date, description, cost))
            cursor.execute("""
                UPDATE vehicles
                SET last_service_date = ?
                WHERE vehicle_id = ?
            """, (service_date, vehicle_id))
            conn.commit()

    def get_maintenance_history(self, vehicle_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT service_date, description, cost
                FROM maintenance_records
                WHERE vehicle_id = ?
            """, (vehicle_id,))
            return cursor.fetchall()
