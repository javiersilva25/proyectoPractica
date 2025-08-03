import { useState, useEffect, type ChangeEvent, type FormEvent } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import axios from 'axios'

import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import BannerIndicadores from './bannerindicadores'

interface LoginForm {
  username: string
  password: string
}

export default function Login() {
  const [form, setForm] = useState<LoginForm>({ username: '', password: '' })
  const [error, setError] = useState('')
  const [registroExitoso, setRegistroExitoso] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    if (location.state?.registrado) {
      setRegistroExitoso(true)
      window.history.replaceState({}, document.title)
    }
  }, [location.state])

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await axios.post('https://jmgconsultores.cl/api/login/', form, {
        headers: { 'Content-Type': 'application/json' },
      })

      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)

      // Luego de guardar el token, obtenemos el perfil para saber el rol
      const perfil = await axios.get('https://jmgconsultores.cl/api/perfil/', {
        headers: {
          Authorization: `Bearer ${data.access}`,
        },
      })

      const { rol, is_superuser } = perfil.data

      if (rol === 'gerente' || is_superuser) {
        navigate('/dashboard/gerente')
      } else {
        navigate('/dashboard')
      }
    } catch {
      setError('Credenciales incorrectas')
    }
  }


  return (
    <div className="flex flex-col min-h-screen text-sm mx-auto max-w-7xl px-2">
      <Navbar />
      <BannerIndicadores />

      <main className="flex-grow flex items-center justify-center bg-gray-100 px-4">
        <div className="w-full max-w-md bg-white p-8 rounded shadow-md space-y-4">
          <h2 className="text-2xl font-bold text-center">Iniciar sesión</h2>

          {registroExitoso && (
            <p className="text-green-600 text-sm text-center">
              ✅ Registro exitoso. Ya puedes iniciar sesión.
            </p>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              name="username"
              type="text"
              placeholder="Nombre de usuario"
              value={form.username}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />

            <input
              name="password"
              type="password"
              placeholder="Contraseña"
              value={form.password}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />

            {error && <p className="text-red-500 text-sm">{error}</p>}

            <button
              type="submit"
              className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Iniciar sesión
            </button>
          </form>

          <p className="text-center text-sm text-gray-600">
            ¿No tienes una cuenta?{' '}
            <Link to="/registro" className="text-blue-500 hover:underline">
              Regístrate aquí
            </Link>
          </p>
        </div>
      </main>

      <Footer />
    </div>
  )
}
