import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

export function useAuth() {
  const navigate = useNavigate()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [rol, setRol] = useState<string | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('access')
    if (token) {
      setIsAuthenticated(true)
      api
        .get('/perfil/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((res) => {
          setRol(res.data.rol || null)
        })
        .catch(() => {
          setIsAuthenticated(false)
          setRol(null)
        })
    } else {
      setIsAuthenticated(false)
      setRol(null)
    }
  }, [])

  const logout = () => {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    setIsAuthenticated(false)
    setRol(null)
    navigate('/login')
  }

  return { isAuthenticated, rol, logout }
}
