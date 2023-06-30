import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:5001/api/task',
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  getUserTasks(userId) {
    return apiClient.get(`/user/${userId}`);
  },
  createTask(taskName, userId) {
    return apiClient.post('', {task_name: taskName, user_id: userId});
  },
  checkInTask(taskId) {
    return apiClient.post('/checkin', {task_id: taskId});
  },
  checkOutTask(taskId) {
    return apiClient.post('/checkout', {task_id: taskId});
  },
  createTaskReport() {
    return apiClient.get('/report');
  }
}