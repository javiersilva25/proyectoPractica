import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import api from '../api/axios'
import toast from 'react-hot-toast'

interface Cliente {
  id: number
  username: string
  first_name: string
  last_name: string
}

interface Indicadores {
  documentos_hoy: number
  clientes_con_mensajes_no_leidos: number
  clientes_con_documentos: number
}

export default function DashboardGerente() {
  const [clientes, setClientes] = useState<Cliente[]>([])
  const [clienteId, setClienteId] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [archivo, setArchivo] = useState<File | null>(null)
  const [subiendo, setSubiendo] = useState(false)
  const [mensaje, setMensaje] = useState('')
  const [enviandoMensaje, setEnviandoMensaje] = useState(false)
  const [rolValido, setRolValido] = useState(false)
  const [indicadores, setIndicadores] = useState<Indicadores | null>(null)
  const navigate = useNavigate()

  // Validar rol y cargar clientes e indicadores
  useEffect(() => {
    api
      .get('/perfil/')
      .then((res) => {
        const { rol, is_superuser } = res.data
        if (rol === 'gerente' || is_superuser) {
          setRolValido(true)

          api.get('/usuarios/clientes/').then((res) => setClientes(res.data))
          api.get('/gerente/indicadores/').then((res) => setIndicadores(res.data))
        } else {
          navigate('/dashboard')
        }
      })
      .catch(() => {
        navigate('/login')
      })
  }, [navigate])

  if (!rolValido) return null

  // Subida de documentos
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!clienteId || !descripcion || !archivo) {
      toast.error('Completa todos los campos.')
      return
    }

    const formData = new FormData()
    formData.append('cliente', clienteId)
    formData.append('descripcion', descripcion)
    formData.append('archivo', archivo)

    setSubiendo(true)
    try {
      await api.post('/documentos/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        withCredentials: true,
      })
      toast.success('Documento subido correctamente.')
      setClienteId('')
      setDescripcion('')
      setArchivo(null)
      // Actualizar indicadores
      const res = await api.get('/gerente/indicadores/')
      setIndicadores(res.data)
    } catch {
      toast.error('Error al subir el documento.')
    } finally {
      setSubiendo(false)
    }
  }

  // Envío de mensajes
  const handleMensajeSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!clienteId || !mensaje) {
      toast.error('Debes seleccionar un cliente y escribir un mensaje.')
      return
    }

    setEnviandoMensaje(true)
    try {
      await api.post('/mensajes/', {
        cliente: clienteId,
        contenido: mensaje,
      })
      toast.success('Mensaje enviado correctamente.')
      setMensaje('')
      // Actualizar indicadores
      const res = await api.get('/gerente/indicadores/')
      setIndicadores(res.data)
    } catch {
      toast.error('Error al enviar el mensaje.')
    } finally {
      setEnviandoMensaje(false)
    }
  }

  return (
    <div className="flex flex-col min-h-screen font-sans">
      <Navbar />
      <main className="flex-grow bg-gray-50 py-12">
        <div className="max-w-5xl mx-auto px-4 space-y-10">
          <h1 className="text-3xl font-bold text-blue-700">Panel del Gerente</h1>

          {/* Indicadores */}
          {indicadores && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-white rounded shadow p-4 text-center">
                <p className="text-gray-500 text-sm">Documentos subidos hoy</p>
                <p className="text-3xl font-bold text-blue-600">{indicadores.documentos_hoy}</p>
              </div>
              <div className="bg-white rounded shadow p-4 text-center">
                <p className="text-gray-500 text-sm">Clientes con mensajes no leídos</p>
                <p className="text-3xl font-bold text-yellow-600">{indicadores.clientes_con_mensajes_no_leidos}</p>
              </div>
              <div className="bg-white rounded shadow p-4 text-center">
                <p className="text-gray-500 text-sm">Clientes con documentos</p>
                <p className="text-3xl font-bold text-green-600">{indicadores.clientes_con_documentos}</p>
              </div>
            </div>
          )}

          {/* Subir Documento */}
          <section className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">📤 Subir Documento a Cliente</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Cliente</label>
                <select
                  value={clienteId}
                  onChange={(e) => setClienteId(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
                >
                  <option value="">Selecciona un cliente</option>
                  {clientes.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.first_name} {c.last_name} ({c.username})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Descripción</label>
                <input
                  type="text"
                  value={descripcion}
                  onChange={(e) => setDescripcion(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Archivo</label>
                <input
                  type="file"
                  onChange={(e) => setArchivo(e.target.files?.[0] || null)}
                  className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
                />
              </div>
              <div className="text-right">
                <button
                  type="submit"
                  disabled={subiendo}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded disabled:opacity-50"
                >
                  {subiendo ? 'Subiendo...' : 'Subir Documento'}
                </button>
              </div>
            </form>
          </section>

          {/* Enviar Mensaje */}
          <section className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">💬 Enviar Mensaje a Cliente</h2>
            <form onSubmit={handleMensajeSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Cliente</label>
                <select
                  value={clienteId}
                  onChange={(e) => setClienteId(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
                >
                  <option value="">Selecciona un cliente</option>
                  {clientes.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.first_name} {c.last_name} ({c.username})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Mensaje</label>
                <textarea
                  value={mensaje}
                  onChange={(e) => setMensaje(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
                  rows={4}
                ></textarea>
              </div>
              <div className="text-right">
                <button
                  type="submit"
                  disabled={enviandoMensaje}
                  className="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded disabled:opacity-50"
                >
                  {enviandoMensaje ? 'Enviando...' : 'Enviar Mensaje'}
                </button>
              </div>
            </form>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  )
}
