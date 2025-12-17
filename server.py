from flask import Flask, request, jsonify, send_from_directory
import sqlite3

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  email TEXT PRIMARY KEY,
  password TEXT,
  role TEXT,
  earnings REAL
)
""")

conn.commit()
conn.close()

app = Flask(__name__)

users = []# Default admin account (fixed)
tasks = []

users.append({
    "email": "admin@learnandearn.com",
    "password": "admin123",
    "role": "admin"
})

users.append({
    "email": "admin@learnandearn.com",
    "password": "admin123",
    "role": "admin",
    "earnings": 0.0,
    "completed": []
})


@app.route("/")
def home():
    return send_from_directory(".", "login.html")

@app.route("/<path:path>")
def files(path):
    return send_from_directory(".", path)

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "worker")

    for user in users:
        if user["email"] == email:
            return jsonify({"status": "failed", "message": "User already exists"})
    
    users.append({
        "email": email,
        "password": password,
        "role": role  # worker / company / admin    
        
    })

    return jsonify({"status": "success", "message": "Account created successfully"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({"status": "success", "email": user["email"], "role": user["role"]
    })

    return jsonify({"status": "failed"})

    
@app.route("/api/admin-data")
def admin_data():
    return jsonify({
        "users": users,
        "tasks": tasks
    })

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/api/company-completed")
def company_completed():
    result = []

    for user in users:
        for task in user.get("completed", []):
            result.append({
                "worker": user["email"],
                "task": task,
                "earnings": user["earnings"]
            })

    return jsonify(result)

@app.route("/api/complete-task", methods=["POST"])
def complete_task():
    data = request.json
    email = data.get("email")
    task_title = data.get("title")
    pay = float(data.get("pay"))

    for user in users:
        if user["email"] == email:
            user["earnings"] += pay
            user["completed"].append(task_title)
            return jsonify({
                "status": "success",
                "earnings": user["earnings"],
                "completed": user["completed"]
            })

    return jsonify({"status": "failed"})

@app.route("/api/admin/users")
def admin_users():
    return jsonify(users)

@app.route("/api/admin/tasks")
def admin_tasks():
    return jsonify(tasks)

@app.route("/api/create-task", methods=["POST"])
def create_task():
    data = request.json

    task = {
        "title": data.get("title"),
        "pay": float(data.get("pay")),
        "company": data.get("company"),
        "completed_by": []
    }

    tasks.append(task)
    return jsonify({"status": "success"})

@app.route("/api/admin-approve", methods=["POST"])
def admin_approve():
    data = request.json
    worker = data.get("worker")
    task = data.get("task")

    for user in users:
        if user["email"] == worker and task in user["completed"]:
            user["approved"].append(task)
            return jsonify({"status": "approved"})

    return jsonify({"status": "failed"})

@app.route("/api/company-pay", methods=["POST"])
def company_pay():
    data = request.json
    worker = data.get("worker")
    task = data.get("task")

    for user in users:
        if user["email"] == worker and task in user["approved"]:
            user["approved"].remove(task)
            return jsonify({"status": "paid"})

    return jsonify({"status": "failed"})

@app.route("/api/me")
def me():
    email = request.args.get("email")

    for user in users:
        if user["email"] == email:
            return jsonify({
                "email": user["email"],
                "role": user["role"]
            })

    return jsonify({"error": "Not logged in"}), 401

if __name__ == "__main__":
    app.run()
