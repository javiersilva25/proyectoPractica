import React from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import BannerIndicadores from '../components/bannerindicadores'
import GraficoHistorial from '../components/graficohistorial'
import NoticiasFiltradas from '../components/NoticiasFIltradas'
import AccionesWidget from '../components/accionesWIdget'
import TeamSection from '../components/TeamSection'

const servicios = [
  {
    titulo: 'Asesoramiento Personalizado',
    descripcion: 'Ofrecemos soluciones personalizadas que se adaptan a las particularidades de su negocio.',
    imagen: 'https://gaux.eu/wp-content/uploads/2024/10/persoenliche-beratung-fuer-ihre-baeckerei.jpg'
  },
  {
    titulo: 'Cumplimiento Normativo',
    descripcion: 'Nos destacamos por nuestro conocimiento actualizado de las normativas fiscales y contables. Gracias a esto, hemos podido asesorar a muchos clientes en el cumplimiento de sus obligaciones legales, evitando sanciones y optimizando su carga tributaria.',
    imagen: 'https://www.floresattorneys.com/wp-content/uploads/2020/07/thumb-tax-litigation_support.jpg'
  },
  {
    titulo: 'Innovación y Tecnología',
    descripcion: 'Nuestra empresa utiliza herramientas tecnológicas avanzadas que facilitan la gestión contable y financiera. Esto no solo mejora la eficiencia, sino que también proporciona a nuestros clientes información oportuna para la toma de decisiones estratégicas.',
    imagen: 'https://5092991.fs1.hubspotusercontent-na1.net/hubfs/5092991/Blog%20notas%20maestrias%20y%20diplomados/Innovaci%C3%B3n%20tecnol%C3%B3gica.jpg'
  }
]

export default function HomePage() {
  return (
    <div className="font-sans text-base text-gray-800">
      <Navbar />
      <BannerIndicadores />

      {/* Hero */}
      <section
        id="hero"
        className="relative z-0 bg-cover bg-center bg-no-repeat text-white px-10 py-24 min-h-[400px] flex items-center justify-start"
        style={{ backgroundImage: "url('/imagenes/fondo.jpg')" }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-black/40 to-transparent z-10" />
        <div className="relative z-20 max-w-xl">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Tu tranquilidad financiera comienza aquí</h1>
          <button
            className="bg-blue-400 text-black px-6 py-3 rounded-md font-bold hover:bg-blue-700 transition"
            onClick={() => document.getElementById('seccion-equipo')?.scrollIntoView({ behavior: 'smooth' })}
          >
            Conócenos
          </button>
        </div>
      </section>

      {/* Servicios */}
      <section className="bg-white px-5 py-10 flex flex-col md:flex-row justify-around gap-6 text-center">
        {servicios.map((serv, idx) => (
          <div key={idx} className="bg-blue-100 p-6 rounded-xl w-full md:w-1/4">
            <img src={serv.imagen} alt={serv.titulo} className="w-full h-40 object-cover rounded-lg mb-4" />
            <h3 className="text-lg font-semibold mb-2">{serv.titulo}</h3>
            <p className="mb-4">{serv.descripcion}</p>
          </div>
        ))}
      </section>

      {/* Noticias y Gráficos */}
      <section className="grid md:grid-cols-3 gap-5 px-4 py-8">
        <div className="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <NoticiasFiltradas />
        </div>
        <GraficoHistorial />
        <div className="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <AccionesWidget />
        </div>
      </section>

      <TeamSection />

      {/* Contacto */}
      <section className="bg-gray-50 px-5 py-16 text-center">
        <h3 className="text-2xl font-bold mb-2 text-gray-800">Contáctanos</h3>
        <p className="text-gray-600 mb-8">¿Tienes alguna duda o comentario? Escríbenos.</p>
        <form className="flex flex-col items-center gap-4">
          {['Nombre Completo', 'Email'].map((ph, idx) => (
            <input
              key={idx}
              type={ph === 'Email' ? 'email' : 'text'}
              placeholder={ph}
              required
              className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300"
            />
          ))}
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
