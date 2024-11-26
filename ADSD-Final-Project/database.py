import sqlite3

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')  # SQLite database file
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

# Function to initialize the database (create tables if they don't exist)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Vehicles table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        owner TEXT NOT NULL
    )
    ''')

    # Create MaintenanceRecords table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maintenance_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        service_date TEXT NOT NULL,
        service_type TEXT NOT NULL,
        cost REAL NOT NULL,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
    )
    ''')

    conn.commit()
    conn.close()

# Function to add a new vehicle to the vehicles table
def add_vehicle(make, model, owner):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO vehicles (make, model, owner) 
    VALUES (?, ?, ?)
    ''', (make, model, owner))
    conn.commit()
    conn.close()

# Function to get all vehicles from the vehicles table
def get_all_vehicles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles')
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles

# Function to get a specific vehicle by ID
def get_vehicle_by_id(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles WHERE id = ?', (vehicle_id,))
    vehicle = cursor.fetchone()
    conn.close()
    return vehicle

# Function to update vehicle details by ID
def update_vehicle(vehicle_id, make, model, owner):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE vehicles
    SET make = ?, model = ?, owner = ?
    WHERE id = ?
    ''', (make, model, owner, vehicle_id))
    conn.commit()
    conn.close()

# Function to delete a vehicle by ID
def delete_vehicle(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vehicles WHERE id = ?', (vehicle_id,))
    conn.commit()
    conn.close()

# Function to add a maintenance record for a specific vehicle
def add_maintenance_record(vehicle_id, service_date, service_type, cost):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO maintenance_records (vehicle_id, service_date, service_type, cost) 
    VALUES (?, ?, ?, ?)
    ''', (vehicle_id, service_date, service_type, cost))
    conn.commit()
    conn.close()

# Function to get all maintenance records for a specific vehicle
def get_maintenance_records_by_vehicle(vehicle_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM maintenance_records WHERE vehicle_id = ?
    ''', (vehicle_id,))
    records = cursor.fetchall()
    conn.close()
    return records

# Function to get all maintenance records
def get_all_maintenance_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM maintenance_records')
    records = cursor.fetchall()
    conn.close()
    return records
