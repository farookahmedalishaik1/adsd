from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from database import init_db, get_all_vehicles, add_vehicle, get_vehicle_by_id, update_vehicle, delete_vehicle, get_maintenance_records_by_vehicle, add_maintenance_record

app = Flask(__name__)

# Initialize the database
init_db()

@app.route("/")
@app.route("/list")
def get_list():
    # Fetch all vehicles from the database
    vehicles = get_all_vehicles()
    return render_template("list.html", vehicles=vehicles)

@app.route("/create", methods=['GET', 'POST'])
def get_post_create():
    if request.method == "GET":
        return render_template("create.html")
    
    if request.method == "POST":
        # Get the data from the form
        data = dict(request.form)
        make = data["make"]
        model = data["model"]
        owner = data["owner"]
        
        # Add the new vehicle to the database
        add_vehicle(make, model, owner)
        
        return redirect(url_for('get_list'))

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def get_update(id):
    vehicle = get_vehicle_by_id(id)  # Get the vehicle details by ID
    
    if request.method == 'GET':
        if vehicle:
            return render_template("update.html", vehicle=vehicle)
        else:
            return "Vehicle not found."
    
    if request.method == 'POST':
        # Get the updated data from the form
        data = dict(request.form)
        make = data["make"]
        model = data["model"]
        owner = data["owner"]
        
        # Update the vehicle in the database
        update_vehicle(id, make, model, owner)
        
        return redirect(url_for('get_list'))

@app.route("/delete/<int:id>")
def get_delete(id):
    # Delete the vehicle from the database
    delete_vehicle(id)
    return redirect(url_for('get_list'))

@app.route("/maintenance/<int:vehicle_id>")
def get_maintenance(vehicle_id):
    # Fetch maintenance records for the vehicle
    records = get_maintenance_records_by_vehicle(vehicle_id)
    return render_template("maintenance.html", vehicle_id=vehicle_id, records=records)

@app.route("/add-maintenance/<int:vehicle_id>", methods=['GET', 'POST'])
def add_maintenance(vehicle_id):
    if request.method == "GET":
        return render_template("add_maintenance.html", vehicle_id=vehicle_id)
    
    if request.method == "POST":
        # Get maintenance details from the form
        data = dict(request.form)
        service_date = data["service_date"]
        service_type = data["service_type"]
        cost = float(data["cost"])
        
        # Add the maintenance record to the database
        add_maintenance_record(vehicle_id, service_date, service_type, cost)
        
        return redirect(url_for('get_maintenance', vehicle_id=vehicle_id))

if __name__ == "__main__":
    app.run(debug=True)

