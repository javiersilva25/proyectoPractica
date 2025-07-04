import React, { useState } from 'react';

const equipo = [
  {
    nombre: 'Jorge Márquez',
    cargo: 'Comunicaciones y Vinculación con el Medio',
    imagen: 'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png',
    descripcion:
      'Descripción breve de Jorge Márquez',
  },
];

const TeamSection: React.FC = () => {
  const [index, setIndex] = useState(0);

  const handlePrev = () => {
    setIndex((prev) => (prev === 0 ? equipo.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setIndex((prev) => (prev === equipo.length - 1 ? 0 : prev + 1));
  };

  return (
    <section className="team" id="seccion-equipo">
      <div className="team-wrapper">
        <div className="team-content">
          <h3>Acerca de</h3>
          <p>
            Con más de 35 años de experiencia, JMG Asesores Contables SpA se ha
            posicionado como un socio confiable en el ámbito contable y
            tributario. Nos distinguimos por nuestro profesionalismo, atención
            personalizada y profundo conocimiento normativo, lo que nos permite
            ofrecer soluciones eficientes y ajustadas a cada cliente. Apostamos
            por la tecnología y la innovación para entregar información oportuna
            que apoye la toma de decisiones estratégicas, siempre con un enfoque
            cercano, ágil y comprometido con la excelencia.
          </p>
        </div>

        <div className="team-slider">
          <h3>Nuestro Equipo</h3>
          <div className="slider-container">
            <button className="nav left" onClick={handlePrev}>‹</button>
            <div className="slider-card">
              <img
                src={equipo[index].imagen}
                alt={equipo[index].nombre}
              />
              <p className="quote">“{equipo[index].descripcion}”</p>
              <h4>{equipo[index].nombre}</h4>
            </div>
            <button className="nav right" onClick={handleNext}>›</button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TeamSection;
