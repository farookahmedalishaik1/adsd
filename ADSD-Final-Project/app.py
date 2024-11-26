from flask import Flask, render_template, request, redirect, url_for
from database import Database

app = Flask(__name__)

# Initialize the database
db = Database("database.db")
db.init_db()

@app.route("/")
@app.route("/list")
def list_vehicles():
    """List all vehicles."""
    vehicles = db.get_all_vehicles()
    return render_template("list.html", vehicles=vehicles)

@app.route("/create", methods=["GET", "POST"])
def create_vehicle():
    """Create a new vehicle."""
    if request.method == "POST":
        make = request.form["make"]
        model = request.form["model"]
        owner = request.form["owner"]
        db.add_vehicle(make, model, owner)
        return redirect(url_for("list_vehicles"))
    return render_template("create.html")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_vehicle(id):
    """Update vehicle details."""
    vehicle = db.get_vehicle_by_id(id)
    if not vehicle:
        return redirect(url_for("list_vehicles"))

    if request.method == "POST":
        make = request.form["make"]
        model = request.form["model"]
        owner = request.form["owner"]
        db.update_vehicle(id, make, model, owner)
        return redirect(url_for("list_vehicles"))
    return render_template("update.html", vehicle=vehicle)

@app.route("/delete/<int:id>")
def delete_vehicle(id):
    """Delete a vehicle."""
    db.delete_vehicle(id)
    return redirect(url_for("list_vehicles"))

if __name__ == "__main__":
    app.run(debug=True)
