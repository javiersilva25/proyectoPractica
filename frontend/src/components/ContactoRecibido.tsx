import { useEffect, useState } from 'react'
import api from '../api/axios'
import toast from 'react-hot-toast'

interface Contacto {
  id: number
  nombre: string
  email: string
  mensaje: string
  creado_en: string
  leido: boolean
}

export default function ContactoRecibido() {
  const [mensajes, setMensajes] = useState<Contacto[]>([])

  const cargarMensajes = () => {
    api
      .get('/contacto/mensajes/')
      .then((res) => setMensajes(res.data))
      .catch(() => toast.error('Error al cargar los mensajes de contacto.'))
  }

  useEffect(() => {
    cargarMensajes()
  }, [])

  const marcarComoLeido = async (id: number) => {
    try {
      await api.patch(`/contacto/mensajes/${id}/`, { leido: true })
      toast.success('Mensaje marcado como leído.')
      cargarMensajes()
    } catch {
      toast.error('Error al marcar como leído.')
    }
  }

  return (
    <section className="bg-white p-6 rounded-lg shadow border border-gray-200">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">📥 Contacto desde el Sitio Web</h2>

      {mensajes.length === 0 ? (
        <p className="text-gray-500">No hay mensajes recibidos aún.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300 text-left text-sm">
            <thead className="bg-gray-100 text-gray-700">
              <tr>
                <th className="px-4 py-2 border">Nombre</th>
                <th className="px-4 py-2 border">Email</th>
                <th className="px-4 py-2 border">Mensaje</th>
                <th className="px-4 py-2 border">Fecha</th>
                <th className="px-4 py-2 border text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {mensajes.map((m) => (
                <tr key={m.id} className="hover:bg-gray-50">
                  <td className="px-4 py-2 border">{m.nombre}</td>
                  <td className="px-4 py-2 border">{m.email}</td>
                  <td className="px-4 py-2 border">{m.mensaje}</td>
                  <td className="px-4 py-2 border">{new Date(m.creado_en).toLocaleString()}</td>
                  <td className="px-4 py-2 border text-center space-y-1">
                    {!m.leido && (
                      <button
                        onClick={() => marcarComoLeido(m.id)}
                        className="bg-blue-500 text-white px-2 py-1 rounded text-xs hover:bg-blue-600"
                      >
                        Marcar como leído
                      </button>
                    )}
                    <a
                      href={`mailto:${m.email}`}
                      className="inline-block bg-green-500 text-white px-2 py-1 rounded text-xs hover:bg-green-600"
                    >
                      Responder
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
