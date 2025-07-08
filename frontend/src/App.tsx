import './index.css';
import BannerIndicadores from './components/bannerindicadores';
import GraficoHistorial from './components/graficohistorial';
import NoticiasFiltradas from './components/NoticiasFIltradas';
import React, { useState, useEffect } from 'react';

// Interfaces para tipado
interface Accion {
  simbolo: string;
  precio: number;
  cambio: number;
  porcentaje_cambio: string;
}

// Componente AccionesWidget integrado
const AccionesWidget: React.FC = () => {
  const [acciones, setAcciones] = useState<Accion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAcciones = async () => {
      try {
        setLoading(true);
        
        // Llamada a tu API del backend
        const response = await fetch('http://localhost:8000/api/acciones/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.acciones && Array.isArray(data.acciones)) {
          setAcciones(data.acciones);
          setError(null);
        } else {
          throw new Error('Formato de datos incorrecto');
        }

      } catch (err) {
        console.error('Error al obtener acciones:', err);
        setError(err instanceof Error ? err.message : 'Error desconocido');
        
        // Datos de respaldo en caso de error
        const datosRespaldo = [
          { simbolo: "AAPL", precio: 175.43, cambio: 2.15, porcentaje_cambio: "1.24" },
          { simbolo: "GOOGL", precio: 2845.67, cambio: -12.34, porcentaje_cambio: "-0.43" },
          { simbolo: "MSFT", precio: 412.89, cambio: 5.67, porcentaje_cambio: "1.39" },
          { simbolo: "TSLA", precio: 248.50, cambio: -3.25, porcentaje_cambio: "-1.29" },
          { simbolo: "AMZN", precio: 3456.78, cambio: 15.23, porcentaje_cambio: "0.44" }
        ];
        setAcciones(datosRespaldo);
      } finally {
        setLoading(false);
      }
    };

    // Cargar datos inicialmente
    fetchAcciones();
    
    // Actualizar cada 30 segundos
    const interval = setInterval(fetchAcciones, 30000);
    
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="acciones-widget">
        <div className="widget-loading">
          <div className="loading-spinner"></div>
          <p>Cargando indicadores del mercado...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="acciones-widget">
      <div className="widget-header">
        <h3>Indicadores de Mercado en Tiempo Real</h3>
        {error && (
          <div className="error-notice">
            <span>⚠️ Usando datos de respaldo</span>
          </div>
        )}
      </div>
      
      <div className="acciones-grid">
        {acciones.map((accion) => (
          <div key={accion.simbolo} className="accion-card">
            <div className="accion-header">
              <span className="simbolo">{accion.simbolo}</span>
              <span className="precio">${accion.precio.toFixed(2)}</span>
            </div>
            <div className={`cambio ${accion.cambio >= 0 ? 'positivo' : 'negativo'}`}>
              <span className="cambio-valor">
                {accion.cambio >= 0 ? '+' : ''}{accion.cambio.toFixed(2)}
              </span>
              <span className="porcentaje">
                ({accion.porcentaje_cambio}%)
              </span>
            </div>
          </div>
        ))}
      </div>
      
      <div className="widget-footer">
        <p>🔄 Actualización automática cada 30 segundos</p>
      </div>
    </div>
  );
};

// Componente principal App
function App() {
  return (
<<<<<<< Updated upstream
    <div className="app-container">
      <header className="top-bar">
        <div className="logo">Logo</div>
        <div className="buttons">
          <a href="#">Acceder</a>
          <button>Suscribirse</button>
=======
    <div className="font-sans text-base text-gray-800">
      {/* Top Bar */}
      <header className="bg-gray-100 flex justify-between items-center px-5 py-2.5">
        <div className="text-xl font-bold text-gray-800">Logo</div>
        <div className="flex gap-2">
          <button className="bg-blue-400 text-black px-4 py-2 rounded-md font-semibold hover:bg-blue-600 transition-colors duration-300">
            Acceder
          </button>
>>>>>>> Stashed changes
        </div>
      </header>

      <BannerIndicadores />
<<<<<<< Updated upstream
      
      <section className="hero">
        <div className="hero-text">
          <h1>Tu tranquilidad financiera comienza aquí</h1>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
          <button>Conócenos</button>
        </div>
      </section>

      {/* Widget de Acciones integrado */}
      <AccionesWidget />

      <section className="services">
        <div className="service-card">
          <h3>Servicio</h3>
          <p>Descripción breve del servicio ofrecido.</p>
          <button>Solicitar</button>
        </div>
        <div className="service-card">
          <h3>Servicio</h3>
          <p>Descripción breve del servicio ofrecido.</p>
          <button>Solicitar</button>
        </div>
        <div className="service-card">
          <h3>Servicio</h3>
          <p>Descripción breve del servicio ofrecido.</p>
          <button>Solicitar</button>
        </div>
      </section>

      <section className="news-chart">
        <div className="news">
          <h3>Últimas noticias</h3>
=======

      {/* Hero Section */}
      <section
        className="relative z-0 bg-cover bg-center bg-no-repeat text-white px-10 py-24 min-h-[400px] flex items-center justify-start"
        style={{ backgroundImage: "url('/imagenes/fondo.jpg')" }}
        id="hero"
      >
        {/* Capa semitransparente */}
        <div className="absolute inset-0 bg-gradient-to-r from-black/40 to-transparent z-10" />

        {/* Contenido visible */}
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

      {/* Services */}
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

      {/* News & Gráficos */}
      <section className="grid md:grid-cols-3 gap-5 px-4 py-8">
        <div className="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
>>>>>>> Stashed changes
          <NoticiasFiltradas />
        </div>

        <div className="chart">
          <GraficoHistorial />
        </div>
<<<<<<< Updated upstream
=======
        <div className="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <AccionesWidget />
        </div>
>>>>>>> Stashed changes
      </section>

      <section className="team">
        <h3>Acerca de</h3>
        <p>Con más de 35 años de experiencia, JMG Asesores Contables SpA se ha posicionado como un socio confiable en el ámbito contable y tributario. Nos distinguimos por nuestro profesionalismo, atención personalizada y profundo conocimiento normativo, lo que nos permite ofrecer soluciones eficientes y ajustadas a cada cliente. Apostamos por la tecnología y la innovación para entregar información oportuna que apoye la toma de decisiones estratégicas, siempre con un enfoque cercano, ágil y comprometido con la excelencia.</p>
        <button>Contáctanos</button>
      </section>

<<<<<<< Updated upstream
      <section className="contact-form">
        <h3>Contáctanos</h3>
        <p>¿Tienes alguna duda o comentario? Escríbenos.</p>
        <form>
          <input type="text" placeholder="Nombre Completo" required />
          <input type="email" placeholder="Email" required />
          <textarea placeholder="Mensaje" required></textarea>
          <button type="submit">Enviar</button>
=======
      {/* Contact Form */}
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
>>>>>>> Stashed changes
        </form>
      </section>

      <footer className="footer">
        <p>
          © 2025 Nombre Empresa | email@empresa.cl | +56 234585576 | Dirección oficina 123, San Fernando
        </p>
      </footer>
    </div>
  );
}

export default App;