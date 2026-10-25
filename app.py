from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)
tasks = [
    {"id": 1, "title": "Finish CCA 2 project", "done": False},
    {"id": 2, "title": "Revise Kubernetes basics", "done": True},
]
next_id = 3

@app.get("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.post("/tasks")
def add_task():
    global next_id
    title = request.form.get("title", "").strip()
    if title:
        tasks.append({"id": next_id, "title": title, "done": False})
        next_id += 1
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
