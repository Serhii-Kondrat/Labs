from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__)

todos = [
    {"id": 1, "task": "Приклад завдання", "status": "В процесі"},
    {"id": 2, "task": "Інше завдання", "status": "Виконано"}
]

@app.route('/')
def index():
    return redirect('/todos.html')
# Отримати список завдань
@app.route('/api/todos', methods=['GET'])
def get_all_todos():
    return jsonify(todos)

# Отримати конкретне завдання за його id
@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        return jsonify(todo)
    return jsonify({'message': 'Todo not found'}), 404

# Створити нове завдання
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = {
        'id': len(todos) + 1,
        'task': data.get('task'),
        'status': data.get('status')
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# Оновити існуюче завдання
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        data = request.json
        todo['task'] = data.get('task', todo['task'])
        todo['status'] = data.get('status', todo['status'])
        return jsonify(todo)
    return jsonify({'message': 'Todo not found'}), 404

# Видалити завдання
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'message': 'Todo deleted'})


# Відображення HTML сторінки для списку завдань
@app.route('/todos.html', methods=['GET'])
def show_todos():
    return render_template('todos.html', todos=todos)

