import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const register = async () => {
    try {
      const response = await axios.post('http://localhost:3000/api/register', { email, password });
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  const login = async () => {
    try {
      const response = await axios.post('http://localhost:3000/api/login', { email, password });
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  const getTasks = async () => {
    try {
      const response = await axios.get('http://localhost:3000/api/tasks');
      setTasks(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const createTask = async () => {
    try {
      const response = await axios.post('http://localhost:3000/api/tasks', { task: newTask });
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    getTasks();
  }, []);

  return (
    <div>
      <h1>Todo App</h1>
      <input type='email' value={email} onChange={(e) => setEmail(e.target.value)} placeholder='Email' />
      <input type='password' value={password} onChange={(e) => setPassword(e.target.value)} placeholder='Password' />
      <button onClick={register}>Register</button>
      <button onClick={login}>Login</button>
      <input type='text' value={newTask} onChange={(e) => setNewTask(e.target.value)} placeholder='New Task' />
      <button onClick={createTask}>Create Task</button>
      <ul>
        {tasks.map((task) => (
          <li key={task._id}>{task.task}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;