import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:5001/api/user',
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  getAllUsers() {
    return apiClient.get();
  },
  createUser(userName) {
    return apiClient.post('', { user_name: userName});
  },
}
