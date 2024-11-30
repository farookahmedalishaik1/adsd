from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    """Create and return a database connection"""
    connection = sqlite3.connect("database.db", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection

# List of vehicles
@app.route("/")
@app.route("/list")
def list_vehicles():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch vehicles with their maintenance count
    cursor.execute("""
        SELECT 
            vehicles.id, 
            vehicles.owner_name, 
            vehicles.make, 
            vehicles.model, 
            vehicles.year,
            COUNT(maintenance.id) as maintenance_count
        FROM 
            vehicles 
        LEFT JOIN 
            maintenance ON vehicles.id = maintenance.vehicle_id
        GROUP BY 
            vehicles.id
    """)
    vehicles = cursor.fetchall()
    connection.close()
    
    return render_template("list.html", vehicles=vehicles)

# Create a new vehicle
@app.route("/add", methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        # Extract and validate form data
        data = dict(request.form)
        
        try:
            # Ensure year is an integer
            data['year'] = int(data['year'])
        except ValueError:
            # Handle invalid year input
            data['year'] = None
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Parameterized insert to prevent SQL injection
        cursor.execute("""
            INSERT INTO vehicles (owner_name, make, model, year) 
            VALUES (?, ?, ?, ?)
        """, (
            data['owner_name'], 
            data['make'], 
            data['model'], 
            data['year']
        ))
        
        connection.commit()
        connection.close()
        
        return redirect(url_for('list_vehicles'))
    
    return render_template("create.html")

# Update vehicle details
@app.route("/update/<int:vehicle_id>", methods=['GET', 'POST'])
def update_vehicle(vehicle_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    if request.method == 'GET':
        # Retrieve specific vehicle for update
        cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        vehicle = cursor.fetchone()
        
        if vehicle is None:
            connection.close()
            return "Vehicle not found", 404
        
        connection.close()
        return render_template("update.html", vehicle=vehicle)
    
    if request.method == 'POST':
        data = dict(request.form)
        
        try:
            data['year'] = int(data['year'])
        except ValueError:
            data['year'] = None
        
        # Parameterized update
        cursor.execute("""
            UPDATE vehicles 
            SET owner_name=?, make=?, model=?, year=? 
            WHERE id=?
        """, (
            data['owner_name'], 
            data['make'], 
            data['model'], 
            data['year'], 
            vehicle_id
        ))
        
        connection.commit()
        connection.close()
        
        return redirect(url_for('list_vehicles'))

# Delete a vehicle
@app.route("/delete/<int:vehicle_id>")
def delete_vehicle(vehicle_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Delete vehicle and its associated maintenance records
        cursor.execute("DELETE FROM maintenance WHERE vehicle_id = ?", (vehicle_id,))
        cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
        connection.commit()
    except sqlite3.Error as e:
        # Basic error handling
        print(f"An error occurred: {e}")
    finally:
        connection.close()
    
    return redirect(url_for('list_vehicles'))

# View maintenance history
@app.route("/vehicle/<int:vehicle_id>/maintenance")
def view_maintenance_history(vehicle_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch vehicle details
    cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
    vehicle = cursor.fetchone()
    
    if vehicle is None:
        connection.close()
        return "Vehicle not found", 404

    # Fetch maintenance records with sorting
    cursor.execute("""
        SELECT * FROM maintenance 
        WHERE vehicle_id = ? 
        ORDER BY service_date DESC
    """, (vehicle_id,))
    maintenance_history = cursor.fetchall()
    
    connection.close()
    
    return render_template(
        "maintenance_history.html", 
        vehicle=vehicle, 
        maintenance=maintenance_history
    )

# Add maintenance record
@app.route("/vehicle/<int:vehicle_id>/maintenance/add", methods=['GET', 'POST'])
def add_maintenance_record(vehicle_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Validate vehicle existence
    cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
    if cursor.fetchone() is None:
        connection.close()
        return "Vehicle not found", 404

    if request.method == 'POST':
        data = dict(request.form)
        
        try:
            data['cost'] = float(data['cost'])
        except ValueError:
            data['cost'] = 0.0
        
        # Parameterized insert for maintenance record
        cursor.execute("""
            INSERT INTO maintenance 
            (vehicle_id, service_date, description, cost) 
            VALUES (?, ?, ?, ?)
        """, (
            vehicle_id, 
            data['service_date'], 
            data['description'], 
            data['cost']
        ))
        
        connection.commit()
        connection.close()
        
        return redirect(url_for('view_maintenance_history', vehicle_id=vehicle_id))
    
    connection.close()
    return render_template("add_maintenance_record.html", vehicle_id=vehicle_id)

if __name__ == "__main__":
    app.run(debug=True)
