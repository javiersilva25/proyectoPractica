import './index.css';
import BannerIndicadores from './components/bannerindicadores';
import GraficoHistorial from './components/graficohistorial';
import NoticiasFiltradas from './components/NoticiasFIltradas';

function App() {

  return (
    <div>
      <header className="top-bar">
      <div className="logo">Logo</div>
      <div className="buttons">
        <a href="#">Acceder</a>
        <button>Suscribirse</button>
      </div>
      </header>

      <BannerIndicadores />
      

      <section className="hero">
        <div className="hero-text">
          <h1>Tu tranquilidad financiera comienza aquí</h1>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
          <button>Conócenos</button>
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
        <div className="news">
          <h3>Últimas noticias</h3>
          <NoticiasFiltradas />
        </div>

        <div className="chart">
          <GraficoHistorial />
        </div>
      </section>

      <section className="team">
        <h3>Acerca de</h3>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        <img src="persona.jpg" alt="Persona" />
        <button>Contáctanos</button>
      </section>

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
          © 2025 Nombre Empresa | email@empresa.cl | +56 234585576 | Dirección oficina 123, San Fernando
        </p>
      </footer>
    </div>
  );
}

export default App;
