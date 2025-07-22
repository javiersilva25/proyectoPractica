import { useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'


interface FormData {
  nombre: string
  email: string
  mensaje: string
}

export default function Contacto() {
  const [formData, setFormData] = useState<FormData>({
    nombre: '',
    email: '',
    mensaje: '',
  })
  const [status, setStatus] = useState<'success' | 'error' | null>(null)

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/contacto/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        setStatus('success')
        setFormData({ nombre: '', email: '', mensaje: '' })
      } else {
        throw new Error('Error al enviar el mensaje')
      }
    } catch (error) {
      console.error(error)
      setStatus('error')
    }
  }

  return (
    <section className="bg-gray-50 px-4 py-10 text-center">
      <h3 className="text-xl font-bold mb-1 text-gray-800">Contáctanos</h3>
      <p className="text-gray-600 mb-4 text-sm">¿Tienes alguna duda o comentario? Escríbenos.</p>

      {status === 'success' && (
        <p className="text-green-600 mb-4 font-semibold">¡Mensaje enviado con éxito!</p>
      )}
      {status === 'error' && (
        <p className="text-red-600 mb-4 font-semibold">Hubo un problema al enviar el mensaje.</p>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col items-center gap-3">
        <input
          type="text"
          name="nombre"
          placeholder="Nombre Completo"
          value={formData.nombre}
          onChange={handleChange}
          required
          className="w-full max-w-md px-3 py-2 rounded-md border border-gray-300 text-sm"
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full max-w-md px-3 py-2 rounded-md border border-gray-300 text-sm"
        />
        <textarea
          name="mensaje"
          placeholder="Mensaje"
          value={formData.mensaje}
          onChange={handleChange}
          required
          className="w-full max-w-md px-3 py-2 rounded-md border border-gray-300 min-h-[100px] text-sm"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-5 py-2 rounded-md font-semibold hover:bg-blue-600 transition"
        >
          Enviar
        </button>
      </form>
    </section>
  )
}
