const express = require('express');
const router = express.Router();
const userController = require('./userController');
const taskController = require('./taskController');

router.post('/register', userController.register);
router.post('/login', userController.login);
router.get('/tasks', taskController.getTasks);
router.get('/tasks/:id', taskController.getTask);
router.post('/tasks', taskController.createTask);
router.put('/tasks/:id', taskController.updateTask);
router.delete('/tasks/:id', taskController.deleteTask);

module.exports = router;