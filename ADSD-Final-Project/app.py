import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('vehicles.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            owner TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route to show all vehicles
@app.route('/list')
def get_list():
    vehicles = get_all_vehicles()
    return render_template('list.html', vehicles=vehicles)

# Helper function to get all vehicles from the database
def get_all_vehicles():
    conn = sqlite3.connect('vehicles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles')
    vehicles = cursor.fetchall()  # Fetch all vehicles as a list of tuples
    conn.close()
    # Convert the list of tuples into a list of dictionaries for easier access
    vehicle_list = []
    for vehicle in vehicles:
        vehicle_list.append({
            'id': vehicle[0],
            'make': vehicle[1],
            'model': vehicle[2],
            'owner': vehicle[3]
        })
    return vehicle_list

# Route to show the update form
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def get_update(id):
    vehicle = get_vehicle_by_id(id)
    if request.method == 'GET':
        return render_template('update.html', vehicle=vehicle)
    
    if request.method == 'POST':
        make = request.form["make"]
        model = request.form["model"]
        owner = request.form["owner"]
        update_vehicle(id, make, model, owner)
        return redirect(url_for('get_list'))

# Helper function to get a vehicle by id
def get_vehicle_by_id(id):
    conn = sqlite3.connect('vehicles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'id': row[0],
            'make': row[1],
            'model': row[2],
            'owner': row[3]
        }
    return None

# Helper function to update vehicle information
def update_vehicle(id, make, model, owner):
    conn = sqlite3.connect('vehicles.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE vehicles
        SET make = ?, model = ?, owner = ?
        WHERE id = ?
    ''', (make, model, owner, id))
    conn.commit()
    conn.close()

# Route to add a new vehicle
@app.route("/add", methods=['GET', 'POST'])
def get_add():
    if request.method == 'POST':
        make = request.form["make"]
        model = request.form["model"]
        owner = request.form["owner"]
        add_vehicle(make, model, owner)
        return redirect(url_for('get_list'))
    return render_template("add.html")

# Helper function to add a new vehicle to the database
def add_vehicle(make, model, owner):
    conn = sqlite3.connect('vehicles.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehicles (make, model, owner)
        VALUES (?, ?, ?)
    ''', (make, model, owner))
    conn.commit()
    conn.close()

# Route to delete a vehicle
@app.route("/delete/<int:id>")
def get_delete(id):
    delete_vehicle(id)
    return redirect(url_for('get_list'))

# Helper function to delete a vehicle
def delete_vehicle(id):
    conn = sqlite3.connect('vehicles.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vehicles WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Run the application
if __name__ == "__main__":
    init_db()  # Ensure the database is initialized when the app starts
    app.run(debug=True)
