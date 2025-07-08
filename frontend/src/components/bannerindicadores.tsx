import { useIndicadores } from '../hooks/useIndicadores';
import { useState, useEffect } from 'react';

const BannerIndicadores = () => {
  const { datos: indicadores, fecha } = useIndicadores();
  const [indicadorActual, setIndicadorActual] = useState(0);
  const [mostrarCompleto, setMostrarCompleto] = useState(false);

  const nombres: Record<string, string> = {
    uf: 'UF',
    utm: 'UTM',
    dolar: 'Dólar',
    euro: 'Euro',
    yen: 'Yen',
    ipc: 'IPC',
    ivp: 'IVP',
    imacec: 'IMACEC',
    tpm: 'TPM',
    libra_cobre: 'Cobre',
    tasa_desempleo: 'Desempleo',
    indice_remuneraciones: 'Remuneraciones',
  };

<<<<<<< Updated upstream
  return (
    <>
      <div className="banner-container">
        <div className="banner-content">
          {Object.entries(nombres).map(([clave, nombre]) => {
            const indicador = indicadores[clave];
            if (!indicador) return null;

            return (
              <span className="banner-item" key={clave}>
                {nombre}: {indicador.valor.toLocaleString('es-CL', {
                  style: 'decimal',
                  maximumFractionDigits: 2,
                })} {indicador.unidad_medida}
              </span>
            );
=======
  // Filtrar indicadores disponibles
  const indicadoresDisponibles = Object.entries(nombres).filter(([clave]) => 
    indicadores[clave]
  );

  useEffect(() => {
    const timer = setInterval(() => {
      if (!mostrarCompleto) {
        if (indicadorActual < indicadoresDisponibles.length - 1) {
          setIndicadorActual(prev => prev + 1);
        } else {
          setMostrarCompleto(true);
          setTimeout(() => {
            setMostrarCompleto(false);
            setIndicadorActual(0);
          }, 60000);
        }
      }
    }, 1500);

    return () => clearInterval(timer);
  }, [indicadorActual, mostrarCompleto, indicadoresDisponibles.length]);

  const contenidoVisible = mostrarCompleto 
    ? indicadoresDisponibles 
    : indicadoresDisponibles.slice(0, indicadorActual + 1);

  const renderIndicador = ([clave, nombre]: [string, string], index: number) => {
    const indicador = indicadores[clave];
    if (!indicador) return null;

    return (
      <span 
        key={clave} 
        className={`inline-block mr-6 whitespace-nowrap transition-all duration-500 ${
          !mostrarCompleto && index === indicadorActual ? 'animate-slide-in' : ''
        }`}
      >
        <span className="font-medium">{nombre}:</span>{' '}
        <span className="font-semibold">
          {indicador.valor.toLocaleString('es-CL', {
            style: 'decimal',
            maximumFractionDigits: 2,
>>>>>>> Stashed changes
          })}
        </span>{' '}
        <span className="text-xs opacity-75">{indicador.unidad_medida}</span>
      </span>
    );
  };

  return (
    <div className="w-full">
      {/* Banner de indicadores */}
      <div className="bg-blue-100 border-b border-gray-300">
        <div className="overflow-hidden py-3">
          {mostrarCompleto ? (
            // Animación completa tipo marquee
            <div className="flex animate-marquee-seamless text-sm text-gray-800">
              <div className="flex shrink-0 whitespace-nowrap">
                {contenidoVisible.map(renderIndicador)}
              </div>
              <div className="flex shrink-0 items-center mx-8">
                <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              </div>
              <div className="flex shrink-0 whitespace-nowrap">
                {contenidoVisible.map(renderIndicador)}
              </div>
              <div className="flex shrink-0 items-center mx-8">
                <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              </div>
            </div>
          ) : (
            // Mostrar indicadores uno por uno - centrado
            <div className="text-sm text-gray-800 text-center px-4 min-h-[24px] flex items-center justify-center">
              <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2">
                {contenidoVisible.map(renderIndicador)}
              </div>
            </div>
          )}
        </div>
      </div>

      {fecha && (
<<<<<<< Updated upstream
        <div className="banner-date">
          Datos actualizados al {new Date(fecha).toLocaleDateString('es-CL')}
=======
        <div className="bg-gray-50 text-center text-xs italic text-gray-600 py-1 px-4">
          Datos actualizados al{' '}
          {new Date(fecha).toLocaleDateString('es-CL', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          })}
>>>>>>> Stashed changes
        </div>
      )}
    </div>
  );
};

export default BannerIndicadores;