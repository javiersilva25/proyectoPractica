import './index.css';
import BannerIndicadores from './components/bannerindicadores';
import GraficoHistorial from './components/graficohistorial';
import NoticiasFiltradas from './components/NoticiasFIltradas';
import AccionesWidget from './components/accionesWIdget';
import React from 'react';
import TeamSection from './components/TeamSection';

function App() {
  return (
    <div className="app-container">
    <header className="top-bar">
      <div className="logo">Logo</div>
      <div className="buttons">
        <button className="login-button">Acceder</button>
      </div>
    </header>

      <BannerIndicadores />

      <section className="hero" id="hero">
        <div className="hero-text">
          <h1>Tu tranquilidad financiera comienza aquí</h1>
          <button onClick={() => {
            const target = document.getElementById("seccion-equipo");
            target?.scrollIntoView({ behavior: 'smooth' });
          }}>
            Conócenos
          </button>
        </div>
      </section>

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
        <div className="news widget-box">
          <NoticiasFiltradas />
        </div>

        <div>
          <GraficoHistorial />
        </div>

        <div className="acciones widget-box">
          <AccionesWidget />
        </div>
      </section>
      
      <TeamSection />

      <section className="contact-form">
        <h3>Contáctanos</h3>
        <p>¿Tienes alguna duda o comentario? Escríbenos.</p>
        <form>
          <input type="text" placeholder="Nombre Completo" required />
          <input type="email" placeholder="Email" required />
          <textarea placeholder="Mensaje" required></textarea>
          <button type="submit">Enviar</button>
        </form>
      </section>

      <footer className="footer">
        <p>
          © 2025 JMG Servicios Contables y Tributarios SpA | jmarkezg@gmail.com | 722 711544 | Cardenal José María Caro N° 351
        </p>
      </footer>
    </div>
  );
}

export default App;
