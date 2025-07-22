import React from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import BannerIndicadores from '../components/bannerindicadores'
import GraficoHistorial from '../components/graficohistorial'
import NoticiasFiltradas from '../components/NoticiasFIltradas'
import AccionesWidget from '../components/accionesWIdget'
import TeamSection from '../components/TeamSection'
import IndicesGlobalesWidget from '../components/IndicesGlobalesWidget'
import Contacto from '../components/Contacto'

const servicios = [
  {
    titulo: 'Asesoramiento Personalizado',
    descripcion: 'Soluciones a medida para su negocio.',
    imagen: 'https://gaux.eu/wp-content/uploads/2024/10/persoenliche-beratung-fuer-ihre-baeckerei.jpg',
  },
  {
    titulo: 'Cumplimiento Normativo',
    descripcion: 'Dominio actualizado de normativas fiscales.',
    imagen: 'https://www.floresattorneys.com/wp-content/uploads/2020/07/thumb-tax-litigation_support.jpg',
  },
  {
    titulo: 'Innovación y Tecnología',
    descripcion: 'Tecnología para la gestión contable moderna.',
    imagen: 'https://5092991.fs1.hubspotusercontent-na1.net/hubfs/5092991/Blog%20notas%20maestrias%20y%20diplomados/Innovaci%C3%B3n%20tecnol%C3%B3gica.jpg',
  },
]

export default function HomePage() {
  return (
    <div className="font-sans text-sm text-gray-800">
      <Navbar />
        <div className="mx-auto max-w-7xl px-2">
          <BannerIndicadores />
        </div>
      <main className="mx-auto max-w-7xl px-2">
        {/* Hero */}
        <section
          id="hero"
          className="relative z-0 bg-cover bg-center text-white px-4 py-14 min-h-[280px] flex items-center"
          style={{ backgroundImage: "url('/imagenes/fondo.jpg')" }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-black/40 to-transparent z-10" />
          <div className="relative z-20 max-w-xl">
            <h1 className="text-3xl font-bold mb-2">Tu tranquilidad financiera comienza aquí</h1>
            <button
              className="bg-blue-400 text-black px-5 py-2 rounded-md font-bold hover:bg-blue-700 transition"
              onClick={() => document.getElementById('seccion-equipo')?.scrollIntoView({ behavior: 'smooth' })}
            >
              Conócenos
            </button>
          </div>
        </section>

        {/* Servicios */}
        <section className="py-5 flex flex-col md:flex-row justify-around gap-4 text-center bg-gray-50">
          {servicios.map((servicio, i) => (
            <div key={i} className="bg-blue-100 p-4 rounded-xl w-full md:w-1/4 hover:shadow-md transition">
              <img src={servicio.imagen} alt={servicio.titulo} className="w-full h-32 object-cover rounded-lg mb-3" />
              <h3 className="text-base font-semibold mb-1">{servicio.titulo}</h3>
              <p className="text-sm">{servicio.descripcion}</p>
            </div>
          ))}
        </section>

        {/* Noticias y Gráficos */}
        <section className="py-4 space-y-4 bg-gray-50">
          {/* Noticias (una sola columna) */}
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-base font-semibold text-gray-800 mb-2">📰 Noticias Destacadas</h2>
            <NoticiasFiltradas />
          </div>

          {/* Gráfico (una sola columna debajo) */}
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-base font-semibold text-gray-800 mb-2">📈 Historial de Indicadores</h2>
            <GraficoHistorial />
          </div>

          {/* Acciones e Índices (dos columnas) */}
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <h2 className="text-base font-semibold text-gray-800 mb-2">💼 Acciones Recomendadas</h2>
              <AccionesWidget />
            </div>

            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <h2 className="text-base font-semibold text-gray-800 mb-2">🌍 Índices Globales</h2>
              <IndicesGlobalesWidget />
            </div>
          </div>
        </section>

        <TeamSection />

        {/* Contacto */}
        <Contacto />
      </main>
      <div className="mx-auto max-w-7xl px-2">   
       <Footer />
      </div>
    </div>
  )
}
