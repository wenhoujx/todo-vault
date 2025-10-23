import { useState, useEffect, type FormEvent } from 'react'
import './App.css'

interface Todo {
  id: string
  description: string
  completed: boolean
  created_at: string
}

const API_URL = "https://k6oxzhlefup26c55ovblprjmke0nxhkj.lambda-url.us-east-1.on.aws"

function App() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [newTodo, setNewTodo] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchTodos()
  }, [])

  const fetchTodos = async () => {
    try {
      const response = await fetch(`${API_URL}/todos`)
      if (response.ok) {
        const data = await response.json()
        setTodos(data)
      }
    } catch (error) {
      console.error('Error fetching todos:', error)
    }
  }

  const handleAddTodo = async (e: FormEvent) => {
    e.preventDefault()
    if (!newTodo.trim()) return

    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: newTodo }),
      })
      
      if (response.ok) {
        const todo = await response.json()
        setTodos([todo, ...todos])
        setNewTodo('')
      }
    } catch (error) {
      console.error('Error adding todo:', error)
    }
    setLoading(false)
  }

  const handleToggleTodo = async (todo: Todo) => {
    try {
      const response = await fetch(`${API_URL}/todos/${todo.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !todo.completed }),
      })
      
      if (response.ok) {
        const updatedTodo = await response.json()
        setTodos(todos.map(t => t.id === todo.id ? updatedTodo : t))
      }
    } catch (error) {
      console.error('Error updating todo:', error)
    }
  }

  const handleDeleteTodo = async (id: string) => {
    try {
      const response = await fetch(`${API_URL}/todos/${id}`, {
        method: 'DELETE',
      })
      
      if (response.ok) {
        setTodos(todos.filter(t => t.id !== id))
      }
    } catch (error) {
      console.error('Error deleting todo:', error)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1>📝 TODO App</h1>
        
        <form onSubmit={handleAddTodo} className="add-todo-form">
          <input
            type="text"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            placeholder="What needs to be done?"
            disabled={loading}
            className="todo-input"
          />
          <button type="submit" disabled={loading || !newTodo.trim()} className="add-button">
            Add
          </button>
        </form>

        <div className="todos-list">
          {todos.length === 0 ? (
            <p className="empty-state">No todos yet. Add one above!</p>
          ) : (
            todos.map(todo => (
              <div key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => handleToggleTodo(todo)}
                  className="todo-checkbox"
                />
                <span className="todo-title">{todo.description}</span>
                <button
                  onClick={() => handleDeleteTodo(todo.id)}
                  className="delete-button"
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>

        <div className="stats">
          {todos.length > 0 && (
            <p>
              {todos.filter(t => !t.completed).length} of {todos.length} tasks remaining
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
