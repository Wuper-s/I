from flask import Flask, request, jsonify
from task_manager import TaskMan

app = Flask(__name__)

task_manager = TaskMan()

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        tasks = task_manager.get_tasks()
        return jsonify(tasks)

    if request.method == "POST":
        data = request.json
        if not data or not data.get("title") or not data.get("description"):
            return jsonify({"error": "Se requiere título y descripción"}), 400

        task = task_manager.add_task(data["title"], data["description"])
        return jsonify(task), 201

if __name__ == "__main__":
    app.run(debug=True)
