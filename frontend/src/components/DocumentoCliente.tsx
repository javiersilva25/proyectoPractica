import { useEffect, useState } from 'react'
//import { useNavigate } from 'react-router-dom'
import api from '../api/axios'
import Navbar from '../components/Navbar'
import BannerIndicadores from '../components/bannerindicadores'
import Footer from '../components/Footer'

interface Documento {
  id: number
  descripcion: string
  archivo: string
  fecha_subida: string
  revisado?: boolean
}

export default function DocumentosCliente() {
  const [documentos, setDocumentos] = useState<Documento[]>([])
  //const navigate = useNavigate()

  const fetchDocumentos = async () => {
    try {
      const response = await api.get('documentos/')
      setDocumentos(Array.isArray(response.data) ? response.data : [])
    } catch (error) {
      console.error('Error al obtener documentos:', error)
    }
  }

  const marcarComoRevisado = async (id: number) => {
    try {
      await api.post(`documentos/${id}/marcar_revisado/`)
      setDocumentos((prev) =>
        prev.map((doc) => (doc.id === id ? { ...doc, revisado: true } : doc))
      )
    } catch (error) {
      console.error('Error al marcar como revisado:', error)
    }
  }

  const handleDescargar = async (doc: Documento) => {
    if (!doc.revisado) await marcarComoRevisado(doc.id)
    window.open(doc.archivo, '_blank')
  }

  useEffect(() => {
    fetchDocumentos()
  }, [])

  return (
    <div className="flex flex-col min-h-screen font-sans text-gray-800">
      <Navbar />
      <BannerIndicadores />

      <main className="flex-grow">
        {/* Título y acción */}
        <section className="bg-blue-100 py-10 px-6 md:px-16">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <h2 className="text-3xl font-bold text-blue-800 mb-4 md:mb-0">📄 Mis Documentos</h2>
          </div>
        </section>

        {/* Documentos */}
        <section className="bg-gray-50 py-12 px-6 md:px-16">
          {documentos.length === 0 ? (
            <p className="text-gray-600 text-center">No tienes documentos disponibles por el momento.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {documentos.map((doc) => (
                <div
                  key={doc.id}
                  className={`bg-white p-6 rounded shadow-md border-l-4 transition ${
                    doc.revisado ? 'border-gray-300' : 'border-blue-500 bg-blue-50'
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-lg text-blue-800">{doc.descripcion}</h3>
                    {!doc.revisado && (
                      <span className="text-xs bg-blue-500 text-white px-2 py-1 rounded">
                        📥 Nuevo
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 mb-4">
                    {new Date(doc.fecha_subida).toLocaleString()}
                  </p>
                  <button
                    onClick={() => handleDescargar(doc)}
                    className="bg-blue-500 text-white text-sm px-4 py-2 rounded hover:bg-blue-600 transition"
                  >
                    Descargar documento
                  </button>
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
