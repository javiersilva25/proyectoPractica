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

  const cargando = Object.keys(indicadores).length === 0;

  return (
    <>
      <div className="bg-blue-100 border-b border-gray-300">
        <div className="mx-auto max-w-7xl px-4 py-2">
          {cargando ? (
            <div className="text-sm text-gray-800 font-medium text-center">
              🔄 Cargando indicadores...
            </div>
          ) : (
            <div className="overflow-hidden whitespace-nowrap">
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
          )}
        </div>
      </div>

      {fecha && !cargando && (
        <div className="text-center text-xs italic text-gray-600 mt-1">
          Datos actualizados al{' '}
          {new Date(fecha).toLocaleDateString('es-CL')}
        </div>
      )}
    </>
  );
};

export default BannerIndicadores;
