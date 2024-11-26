from flask import Flask, render_template, request, redirect, url_for
from database import Database

app = Flask(__name__)
db = Database("database.db")  # Database instance


# Redirect to the vehicle list
@app.route("/")
def index():
    return redirect(url_for("list_vehicles"))


# List all vehicles
@app.route("/list")
def list_vehicles():
    vehicles = db.get_all_vehicles()  # Fetch all vehicles from the database
    return render_template("list.html", vehicles=vehicles)


# Add a new vehicle
@app.route("/add", methods=["GET", "POST"])
def add_vehicle():
    if request.method == "POST":
        # Fetch data from the form
        owner_name = request.form["owner_name"]
        make = request.form["make"]
        model = request.form["model"]
        year = request.form["year"]
        # Add the vehicle to the database
        db.add_vehicle(owner_name, make, model, int(year))
        return redirect(url_for("list_vehicles"))
    return render_template("create.html")


# Update an existing vehicle
@app.route("/update/<int:vehicle_id>", methods=["GET", "POST"])
def update_vehicle(vehicle_id):
    vehicle = db.get_vehicle(vehicle_id)  # Fetch the vehicle details
    if request.method == "POST":
        # Update vehicle details based on the form
        owner_name = request.form["owner_name"]
        make = request.form["make"]
        model = request.form["model"]
        year = request.form["year"]
        db.update_vehicle(vehicle_id, owner_name, make, model, int(year))
        return redirect(url_for("list_vehicles"))
    return render_template("update.html", vehicle=vehicle)


# Delete a vehicle
@app.route("/delete/<int:vehicle_id>")
def delete_vehicle(vehicle_id):
    db.delete_vehicle(vehicle_id)  # Remove vehicle from the database
    return redirect(url_for("list_vehicles"))


# View maintenance history for a specific vehicle
@app.route("/vehicle/<int:vehicle_id>/maintenance")
def view_maintenance_history(vehicle_id):
    vehicle = db.get_vehicle(vehicle_id)  # Fetch vehicle details
    maintenance_history = db.get_maintenance_history(vehicle_id)  # Fetch maintenance records
    return render_template(
        "maintenance_history.html", 
        vehicle=vehicle, 
        maintenance=maintenance_history
    )


# Add a maintenance record for a specific vehicle
@app.route("/vehicle/<int:vehicle_id>/maintenance/add", methods=["GET", "POST"])
def add_maintenance_record(vehicle_id):
    if request.method == "POST":
        # Fetch maintenance data from the form
        service_date = request.form["service_date"]
        description = request.form["description"]
        cost = request.form["cost"]
        # Add the maintenance record to the database
        db.add_maintenance_record(vehicle_id, service_date, description, float(cost))
        return redirect(url_for("view_maintenance_history", vehicle_id=vehicle_id))
    return render_template("add_maintenance_record.html", vehicle_id=vehicle_id)


if __name__ == "__main__":
    app.run(debug=True)
