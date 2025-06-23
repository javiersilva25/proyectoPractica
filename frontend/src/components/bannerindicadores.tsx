import { useIndicadores } from '../hooks/useIndicadores';

const BannerIndicadores = () => {
  const { datos: indicadores, fecha } = useIndicadores();

  const nombres: Record<string, string> = {
    uf: 'UF',
    utm: 'UTM',
    dolar: 'Dólar',
    dolar_intercambio: 'Dólar Acuerdo',
    euro: 'Euro',
    yen: 'Yen',
    ipc: 'IPC',
    ivp: 'IVP',
    imacec: 'IMACEC',
    tpm: 'TPM',
    libra_cobre: 'Cobre',
    tasa_desempleo: 'Desempleo',
    bitcoin: 'Bitcoin',
    indice_remuneraciones: 'Remuneraciones',
    tasa_interes_corriente: 'Interés Corriente',
  };

  return (
    <>
      <div className="banner-container">
        <div className="banner-content">
          {Object.entries(nombres).map(([clave, nombre]) => {
            const valor = indicadores[clave]?.valor;
            if (!valor) return null;

            return (
              <span className="banner-item" key={clave}>
                {nombre}: {valor.toLocaleString('es-CL', {
                  style: 'decimal',
                  maximumFractionDigits: 2,
                })}
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
