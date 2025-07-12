import React from 'react';
import BannerIndicadores from './components/bannerindicadores';
import GraficoHistorial from './components/graficohistorial';
import NoticiasFiltradas from './components/NoticiasFIltradas';
import AccionesWidget from './components/accionesWIdget';
import TeamSection from './components/TeamSection';

function App() {
  return (
    <div className="font-sans text-base text-gray-800">
      {/* Top Bar */}
      <header className="bg-gray-100 flex justify-between items-center px-5 py-2.5">
        <div className="text-xl font-bold text-gray-800">Logo</div>
        <div className="flex gap-2">
          <button className="bg-blue-400 text-black px-4 py-2 rounded-md font-semibold hover:bg-blue-600 transition-colors duration-300">
            Acceder
          </button>
        </div>
      </header>

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
            className="bg-blue-400 text-black px-6 py-3 rounded-md font-bold hover:bg-blue-700 transition-colors duration-300 transform hover:scale-105"
            onClick={() => {
              const target = document.getElementById('seccion-equipo');
              target?.scrollIntoView({ behavior: 'smooth' });
            }}
          >
            Conócenos
          </button>
        </div>
      </section>

      {/* Servicios */}
      <section className="bg-white px-5 py-10 flex flex-col md:flex-row justify-around gap-6 text-center">
        {[1, 2, 3].map((_, i) => (
          <div key={i} className="bg-blue-100 p-6 rounded-xl w-full md:w-1/4 transform hover:scale-105 transition-transform duration-300 shadow-lg hover:shadow-xl">
            <h3 className="text-lg font-semibold mb-2">Servicio</h3>
            <p className="mb-4">Descripción breve del servicio ofrecido.</p>
            <button className="bg-blue-400 text-black px-4 py-2 rounded-md hover:bg-blue-600 transition-colors duration-300">
              Solicitar
            </button>
          </div>
        ))}
      </section>

      {/* Noticias y Gráficos */}
      <section className="grid md:grid-cols-3 gap-5 px-4 py-8">
        <div className="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <NoticiasFiltradas />
        </div>
        <div>
          <GraficoHistorial />
        </div>
        <div className="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <AccionesWidget />
        </div>
      </section>

      {/* Team Section */}
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
            className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
          />
          <input
            type="email"
            placeholder="Email"
            required
            className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
          />
          <textarea
            placeholder="Mensaje"
            required
            className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 resize-vertical min-h-[120px] focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-600 transition-colors duration-300 transform hover:scale-105"
          >
            Enviar
          </button>
        </form>
      </section>

      {/* Footer */}
      <footer className="bg-blue-100 text-center py-4 text-sm text-gray-700">
        © 2025 JMG Servicios Contables y Tributarios SpA | jmarkezg@gmail.com | 722 711544 | Cardenal José María Caro N° 351
      </footer>
    </div>
  );
}

export default App;
