

from flask import Flask, render_template, request, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = "unifix-local-demo-secret"
ACCESS_CONTROL_ENABLED = True

# Fictional student accounts
students = {
    "alex@unifix.test": {
        "password": "alex123",
        "name": "Alex"
    },
    "jamie@unifix.test": {
        "password": "jamie123",
        "name": "Jamie"
    }
}

# Fictional maintenance records

maintenance_requests = {
    101: {
        "owner": "alex@unifix.test",
        "title": "Leaking bathroom tap",
        "location": "Bathroom",
        "description": "The bathroom tap continues to leak.",
        "status": "Awaiting repair"
    },
    102: {
        "owner": "jamie@unifix.test",
        "title": "Broken bedroom heating",
        "location": "Bedroom",
        "description": "The radiator is not producing heat.",
        "status": "In progress"
    },
    103: {
        "owner": "security@unifix.test",
        "title": "Confidential security inspection",
        "location": "Staff Office",
        "description": "Internal inspection record. CTF FLAG: flag{unifix_access_control}",
        "status": "Confidential"
    }
}

    
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").lower()
        password = request.form.get("password", "")

        student = students.get(email)

        if student and student["password"] == password:
            session["email"] = email
            session["name"] = student["name"]
            return redirect(url_for("dashboard"))

        error = "Incorrect email or password."

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))

    my_requests = {
        request_id: record
        for request_id, record in maintenance_requests.items()
        if record["owner"] == session["email"]
    }

    return render_template(
        "dashboard.html",
        name=session["name"],
        maintenance_requests=my_requests
    )


@app.route("/request/<int:request_id>")
def view_request(request_id):
    if "email" not in session:
        return redirect(url_for("login"))

    record = maintenance_requests.get(request_id)

    if record is None:
        abort(404)

    if ACCESS_CONTROL_ENABLED:
        if record["owner"] != session["email"]:
            abort(403)

    return render_template(
        "request.html",
        record=record,
        request_id=request_id
    )




@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
