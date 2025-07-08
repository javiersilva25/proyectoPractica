import React, { useState } from 'react';

const equipo = [
  {
    nombre: 'Jorge Márquez',
    imagen:
      'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png',
    descripcion: 'Descripción breve de Jorge Márquez',
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
    <section id="seccion-equipo" className="bg-blue-50 py-16 px-4 flex justify-center">
      <div className="flex flex-col md:flex-row gap-8 w-full max-w-6xl">
        {/* Sección Acerca de */}
        <div className="bg-blue-100 rounded-2xl p-8 shadow-lg flex-1 min-w-[300px]">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">Acerca de</h3>
          <p className="text-justify text-gray-700 leading-relaxed">
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

        {/* Sección Nuestro Equipo */}
        <div className="bg-blue-100 rounded-2xl p-8 shadow-lg flex-1 min-w-[300px] text-center">
          <h3 className="text-2xl font-semibold text-gray-800 mb-6">Nuestro Equipo</h3>
          <div className="flex items-center justify-center gap-4">
            {/* Botón Anterior */}
            <button
              onClick={handlePrev}
              className="text-2xl bg-white text-black w-10 h-10 rounded-full shadow hover:bg-gray-200 transition"
            >
              ‹
            </button>

            {/* Tarjeta */}
            <div className="text-center max-w-xs">
              <img
                src={equipo[index].imagen}
                alt={equipo[index].nombre}
                className="w-24 h-24 object-cover rounded-full mx-auto mb-4"
              />
              <p className="italic text-sm text-gray-600 mb-2">
                “{equipo[index].descripcion}”
              </p>
              <h4 className="text-lg font-semibold text-gray-800">
                {equipo[index].nombre}
              </h4>
            </div>

            {/* Botón Siguiente */}
            <button
              onClick={handleNext}
              className="text-2xl bg-white text-black w-10 h-10 rounded-full shadow hover:bg-gray-200 transition"
            >
              ›
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TeamSection;
