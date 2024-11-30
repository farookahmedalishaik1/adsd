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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_name TEXT NOT NULL,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER,
                    last_service_date TEXT
                )
            """)

            # MaintenanceRecords table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    service_date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    cost REAL NOT NULL,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
                )
            """)
            conn.commit()
