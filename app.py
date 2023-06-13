from flask import Flask, render_template, request, redirect, jsonify, g
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

DATABASE = 'tasks.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_table():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, deadline DATETIME, completed INTEGER DEFAULT 0)")
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks')
def get_tasks():
    create_table()
    tasks = []
    cur = get_db().execute("SELECT id, description, deadline, completed FROM tasks")
    for row in cur.fetchall():
        task = {
            'id': row[0],
            'description': row[1],
            'deadline': row[2],
            'completed': bool(row[3])
        }
        tasks.append(task)
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    description = request.form.get('description')
    deadline = request.form.get('deadline')

    db = get_db()
    db.execute("INSERT INTO tasks (description, deadline) VALUES (?, ?)", (description, deadline))
    db.commit()

    return redirect('/')

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    db = get_db()
    db.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    db.commit()
    return redirect('/')

@app.route('/api/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return redirect('/')

@app.before_request
def check_deadlines():
    if request.endpoint != 'static':
        create_table()
        cur = get_db().execute("SELECT id, deadline, completed FROM tasks")
        for row in cur.fetchall():
            task_id = row[0]
            deadline = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            completed = bool(row[2])

            if not completed:
                current_time = datetime.now()
                time_difference = deadline - current_time

                if time_difference < timedelta(hours=1):
                    print(f'Task {task_id} approaching deadline!')

if __name__ == '__main__':
    app.run(debug=True)
