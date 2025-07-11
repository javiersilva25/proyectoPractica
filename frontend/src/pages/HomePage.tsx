import React from 'react'
import BannerIndicadores from '../components/bannerindicadores'
import GraficoHistorial from '../components/graficohistorial'
import NoticiasFiltradas from '../components/NoticiasFIltradas'
import AccionesWidget from '../components/accionesWIdget'
import TeamSection from '../components/TeamSection'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

export default function HomePage() {
  return (
    <div className="font-sans text-base text-gray-800">
      {/* ✅ Barra de navegación inteligente */}
      <Navbar />

      {/* Indicadores */}
      <BannerIndicadores />

      {/* Hero Section */}
      <section
        className="relative z-0 bg-cover bg-center bg-no-repeat text-white px-10 py-24 min-h-[400px] flex items-center justify-start"
        style={{ backgroundImage: "url('/imagenes/fondo.jpg')" }}
        id="hero"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-black/40 to-transparent z-10" />
        <div className="relative z-20 max-w-xl">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Tu tranquilidad financiera comienza aquí
          </h1>
          <button
            className="bg-blue-400 text-black px-6 py-3 rounded-md font-bold hover:bg-blue-700 transition"
            onClick={() => {
              const target = document.getElementById('seccion-equipo')
              target?.scrollIntoView({ behavior: 'smooth' })
            }}
          >
            Conócenos
          </button>
        </div>
      </section>

      {/* Servicios */}
      <section className="bg-white px-5 py-10 flex flex-col md:flex-row justify-around gap-6 text-center">
        {[1, 2, 3].map((_, i) => (
          <div key={i} className="bg-blue-100 p-6 rounded-xl w-full md:w-1/4">
            <h3 className="text-lg font-semibold mb-2">Servicio</h3>
            <p className="mb-4">Descripción breve del servicio ofrecido.</p>
          </div>
        ))}
      </section>

      {/* Noticias y Gráficos */}
      <section className="grid md:grid-cols-3 gap-5 px-4 py-8">
        <div className="bg-white p-4 rounded-lg shadow">
          <NoticiasFiltradas />
        </div>
        <div>
          <GraficoHistorial />
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <AccionesWidget />
        </div>
      </section>

      {/* Nuestro equipo */}
      <TeamSection />

      {/* Contacto */}
      <section className="bg-gray-50 px-5 py-16 text-center">
        <h3 className="text-2xl font-bold mb-2 text-gray-800">Contáctanos</h3>
        <p className="text-gray-600 mb-8">¿Tienes alguna duda o comentario? Escríbenos.</p>
        <form className="flex flex-col items-center gap-4">
          <input
            type="text"
            placeholder="Nombre Completo"
            required
            className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300"
          />
          <input
            type="email"
            placeholder="Email"
            required
            className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300"
          />
          <textarea
            placeholder="Mensaje"
            required
            className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 resize-vertical min-h-[120px]"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-600 transition"
          >
            Enviar
          </button>
        </form>
      </section>

      <Footer />
    </div>
  )
}
