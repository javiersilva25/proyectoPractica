import { useIndicadores } from '../hooks/useIndicadores';

const BannerIndicadores = () => {
  const { datos: indicadores, fecha } = useIndicadores();

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

  return (
    <>
      {/* Banner de indicadores con animación */}
      <div className="overflow-hidden whitespace-nowrap bg-blue-100 py-2 border-b border-gray-300 relative">
        <div className="inline-block pl-full animate-marquee text-sm text-gray-800 font-medium">
          {Object.entries(nombres).map(([clave, nombre]) => {
            const indicador = indicadores[clave];
            if (!indicador) return null;

            return (
              <span key={clave} className="inline-block mr-10">
                {nombre}:{' '}
                {indicador.valor.toLocaleString('es-CL', {
                  style: 'decimal',
                  maximumFractionDigits: 2,
                })}{' '}
                {indicador.unidad_medida}
              </span>
            );
          })}
        </div>
      </div>

      {/* Fecha de actualización */}
      {fecha && (
        <div className="text-center text-xs italic text-gray-600 mt-1">
          Datos actualizados al{' '}
          {new Date(fecha).toLocaleDateString('es-CL')}
        </div>
      )}
    </>
  );
};

export default BannerIndicadores;
