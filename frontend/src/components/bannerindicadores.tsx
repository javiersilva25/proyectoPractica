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
          })}
        </div>
      </div>

      {fecha && (
        <div className="banner-date">
          Datos actualizados al {new Date(fecha).toLocaleDateString('es-CL')}
        </div>
      )}
    </>
  );
};

export default BannerIndicadores;
