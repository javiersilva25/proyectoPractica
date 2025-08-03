import axios from 'axios'

const instance = axios.create({
  baseURL: 'https://jmgconsultores.cl/api/'
})

instance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default instance
