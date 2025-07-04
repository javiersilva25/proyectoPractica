
import React, { useState, useEffect } from 'react';

interface Accion {
  simbolo: string;
  precio: number;
  cambio: number;
  porcentaje_cambio: string;
}

const AccionesWidget: React.FC = () => {
  const [acciones, setAcciones] = useState<Accion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAcciones = async () => {
      try {
        setLoading(true);

        const response = await fetch('http://localhost:8000/api/acciones/', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);

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

        // Datos de respaldo
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

    fetchAcciones();
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

export default AccionesWidget;
