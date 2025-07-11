import { useEffect, useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import Navbar from '../components/Navbar'
import BannerIndicadores from '../components/bannerindicadores'
import Footer from '../components/Footer'
import api from '../api/axios'

export default function Dashboard() {
  const [data, setData] = useState<any>(null)
  const { logout } = useAuth()

  useEffect(() => {
    api
      .get('cliente/dashboard/')
      .then((res) => {
        setData(res.data)
      })
      .catch(() => {
        console.error('Token inválido o expirado. Cerrando sesión automáticamente.')
        logout()
      })
  }, [])

  return (
    <div className="font-sans text-base text-gray-800">
      <Navbar />
      <BannerIndicadores />

      {/* Bienvenida y resumen */}
      <section className="bg-blue-200 py-10 px-6 md:px-16">
        <h2 className="text-3xl font-bold text-white mb-1">Bienvenido, {data?.username || 'Usuario'}</h2>
        <p className="text-white text-lg mb-6">Resumen de tu cuenta</p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-6 shadow text-center">
            <p className="text-gray-600 text-sm">Tareas</p>
            <p className="text-3xl font-bold text-blue-600">3</p>
          </div>
          <div className="bg-white rounded-lg p-6 shadow text-center">
            <p className="text-gray-600 text-sm">Documentos</p>
            <p className="text-3xl font-bold text-blue-600">5</p>
          </div>
          <div className="bg-white rounded-lg p-6 shadow text-center">
            <p className="text-gray-600 text-sm">Mensajes</p>
            <p className="text-3xl font-bold text-blue-600">1</p>
          </div>
        </div>
      </section>

      {/* Actividad reciente */}
      <section className="bg-gray-100 py-12 px-6 md:px-16">
        <h3 className="text-xl font-bold mb-6">Actividad Reciente</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-blue-100 p-6 rounded-xl">
            <div className="h-4 bg-gray-300 mb-4 rounded w-2/3"></div>
            <div className="h-4 bg-gray-300 mb-2 rounded w-full"></div>
            <div className="h-4 bg-gray-300 mb-2 rounded w-3/4"></div>
            <div className="h-4 bg-gray-300 rounded w-1/2"></div>
          </div>
          <div className="bg-blue-100 p-6 rounded-xl">
            <div className="space-y-2">
              {[1, 2, 3, 4].map((_, i) => (
                <div key={i} className="h-4 bg-gray-300 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}
