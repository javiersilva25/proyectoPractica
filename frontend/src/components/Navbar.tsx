import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { useEffect, useRef, useState } from 'react'
import api from '../api/axios'

export default function Navbar() {
  const { isAuthenticated, rol, logout } = useAuth()
  const navigate = useNavigate()
  const [nombreUsuario, setNombreUsuario] = useState<string>('')
  const [menuAbierto, setMenuAbierto] = useState(false)
  const menuRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('access')
    if (isAuthenticated && token) {
      api
        .get('/perfil/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((res) => {
          const { nombre } = res.data
          setNombreUsuario(nombre)
        })
        .catch(() => {
          setNombreUsuario('')
        })
    }
  }, [isAuthenticated])

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const getDashboardRoute = () => {
    if (rol === 'gerente') return '/dashboard/gerente'
    return '/dashboard'
  }

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuAbierto(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-xl font-bold text-blue-600 tracking-tight hover:opacity-80 transition">
              🧾 JMG Asesores Contables
            </Link>
          </div>

          {/* Navegación */}
          <nav className="space-x-6 text-sm font-medium flex items-center relative">
            <Link to="/" className="text-gray-700 hover:text-blue-600 transition">
              Inicio
            </Link>

            {isAuthenticated ? (
              <>
                {/* Menú de usuario */}
                <div className="relative" ref={menuRef}>
                  <button
                    onClick={() => setMenuAbierto(!menuAbierto)}
                    className="flex items-center text-gray-700 hover:text-blue-600 transition gap-2"
                  >
                    <span className="text-lg">👤</span>
                    {nombreUsuario}
                    <svg
                      className={`w-4 h-4 transform transition-transform ${menuAbierto ? 'rotate-180' : ''}`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {menuAbierto && (
                    <div className="absolute right-0 mt-2 w-44 bg-white shadow-lg rounded border z-50 overflow-hidden">
                      <Link
                        to={getDashboardRoute()}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
                        onClick={() => setMenuAbierto(false)}
                      >
                        Ir al Dashboard
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition"
                      >
                        Cerrar sesión
                      </button>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-blue-600 transition">
                  Iniciar sesión
                </Link>
                <Link to="/registro" className="text-gray-700 hover:text-blue-600 transition">
                  Registrarse
                </Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
