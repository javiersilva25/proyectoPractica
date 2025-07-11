import { useEffect, useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import Navbar from '../components/Navbar'
import BannerIndicadores from '../components/bannerindicadores'
import Footer from '../components/Footer'
import PerfilCard from '../components/PerfilCard'
import api from '../api/axios'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

interface Mensaje {
  id: number
  contenido: string
  fecha: string
  leido: boolean
}

export default function Dashboard() {
  const [documentosNoLeidos, setDocumentosNoLeidos] = useState<number>(0)
  const [mensajes, setMensajes] = useState<Mensaje[]>([])
  const { logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    // Validar token con una consulta ligera (por ejemplo dashboard)
    api
      .get('cliente/dashboard/')
      .catch(() => {
        console.error('Token inválido o expirado. Cerrando sesión automáticamente.')
        logout()
      })

    // Documentos
    api
      .get('documentos/', { withCredentials: true })
      .then((res) => {
        const docs = Array.isArray(res.data) ? res.data : []
        const noLeidos = docs.filter((d) => d.revisado === false).length
        setDocumentosNoLeidos(noLeidos)
        if (noLeidos > 0) {
          toast(`Tienes ${noLeidos} documento(s) nuevo(s) por revisar.`, {
            icon: '📄',
            duration: 5000,
          })
        }
      })
      .catch((err) => console.error('Error al obtener documentos:', err))

    // Mensajes
    api
      .get('mensajes/', { withCredentials: true })
      .then((res) => {
        const data = Array.isArray(res.data) ? res.data : []
        setMensajes(data)

        const nuevos = data.filter((m) => !m.leido)
        if (nuevos.length > 0) {
          toast(`Tienes ${nuevos.length} mensaje(s) nuevo(s).`, {
            icon: '📬',
            duration: 5000,
          })
        }
      })
      .catch((err) => console.error('Error al obtener mensajes:', err))
  }, [])

  const marcarMensajeComoLeido = async (id: number) => {
    try {
      await api.post(`mensajes/${id}/marcar_leido/`, null, {
        withCredentials: true,
      })
      setMensajes((prev) =>
        prev.map((m) => (m.id === id ? { ...m, leido: true } : m))
      )
    } catch (error) {
      console.error('Error al marcar mensaje como leído:', error)
    }
  }

  return (
    <div className="flex flex-col min-h-screen font-sans text-base text-gray-800">
      <Navbar />
      <BannerIndicadores />

      <main className="flex-grow">
        {/* Bienvenida y resumen */}
        <section className="bg-blue-200 py-10 px-6 md:px-16">
          <h2 className="text-3xl font-bold text-white mb-1">Bienvenido(a)</h2>
          <p className="text-white text-lg mb-6">Resumen de tu cuenta</p>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <PerfilCard />

            <div className="bg-white rounded-lg p-6 shadow text-center">
              <p className="text-gray-600 text-sm">Documentos</p>
              <p className="text-3xl font-bold text-blue-600">
                {documentosNoLeidos > 0 ? `${documentosNoLeidos} 📄 nuevos` : '0'}
              </p>
              <button
                onClick={() => navigate('/cliente/documentos')}
                className="mt-4 bg-blue-500 text-white text-sm px-4 py-2 rounded hover:bg-blue-600 transition"
              >
                Ver documentos
              </button>
            </div>
          </div>
        </section>

        {/* Mensajes recientes */}
        <section className="bg-gray-100 py-12 px-6 md:px-16">
          <h3 className="text-xl font-bold mb-6">📩 Mensajes recientes</h3>
          {mensajes.length === 0 ? (
            <p className="text-gray-600">No tienes mensajes por ahora.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {mensajes.map((mensaje) => (
                <div
                  key={mensaje.id}
                  className={`bg-white p-4 rounded shadow relative cursor-pointer transition hover:shadow-md ${
                    !mensaje.leido ? 'border-l-4 border-blue-500' : ''
                  }`}
                  onClick={() => {
                    if (!mensaje.leido) marcarMensajeComoLeido(mensaje.id)
                  }}
                >
                  {!mensaje.leido && (
                    <span className="absolute top-2 right-2 text-xs bg-blue-500 text-white px-2 py-1 rounded">
                      📬 Nuevo
                    </span>
                  )}
                  <p className="text-sm text-gray-500 mb-2">
                    {new Date(mensaje.fecha).toLocaleString()}
                  </p>
                  <p className="text-gray-800 whitespace-pre-wrap">{mensaje.contenido}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>

      <Footer />
    </div>
  )
}
