from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

db = {}
app = Flask(__name__)
CORS(app)

TODO_KEY_PREFIX = "todo:"

def get_all_todos():
    todos = []
    for key in db.keys():
        if key.startswith(TODO_KEY_PREFIX):
            todo_data = db[key]
            if isinstance(todo_data, str):
                todo_data = json.loads(todo_data)
            todos.append(todo_data)
    return sorted(todos, key=lambda x: x.get('created_at', ''), reverse=True)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        todos = get_all_todos()
        return jsonify(todos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({"error": "Title is required"}), 400
        
        todo_id = str(datetime.now().timestamp()).replace('.', '')
        todo = {
            "id": todo_id,
            "title": data['title'],
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        db[f"{TODO_KEY_PREFIX}{todo_id}"] = json.dumps(todo)
        return jsonify(todo), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    try:
        key = f"{TODO_KEY_PREFIX}{todo_id}"
        if key not in db:
            return jsonify({"error": "Todo not found"}), 404
        
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid request body"}), 400
        
        todo_data = db[key]
        if isinstance(todo_data, str):
            todo_data = json.loads(todo_data)
        
        if 'title' in data:
            todo_data['title'] = data['title']
        if 'completed' in data:
            todo_data['completed'] = data['completed']
        
        db[key] = json.dumps(todo_data)
        return jsonify(todo_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        key = f"{TODO_KEY_PREFIX}{todo_id}"
        if key not in db:
            return jsonify({"error": "Todo not found"}), 404
        
        del db[key]
        return jsonify({"message": "Todo deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
