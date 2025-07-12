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
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

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
        setLastUpdate(new Date());
      } else {
        throw new Error('Formato de datos incorrecto');
      }
    } catch (err) {
      console.error('Error al obtener acciones:', err);
      setError(err instanceof Error ? err.message : 'Error desconocido');

      // Datos de respaldo
      setAcciones([
        { simbolo: "AAPL", precio: 175.43, cambio: 2.15, porcentaje_cambio: "1.24" },
        { simbolo: "GOOGL", precio: 2845.67, cambio: -12.34, porcentaje_cambio: "-0.43" },
        { simbolo: "MSFT", precio: 412.89, cambio: 5.67, porcentaje_cambio: "1.39" },
        { simbolo: "TSLA", precio: 248.50, cambio: -3.25, porcentaje_cambio: "-1.29" },
        { simbolo: "AMZN", precio: 3456.78, cambio: 15.23, porcentaje_cambio: "0.44" }
      ]);
      setLastUpdate(new Date());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAcciones();
    const interval = setInterval(fetchAcciones, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="bg-white p-4 rounded-lg shadow text-center">
        <div className="animate-spin border-4 border-gray-200 border-t-blue-500 rounded-full w-8 h-8 mx-auto mb-2" />
        <p className="text-sm text-gray-700">Cargando indicadores del mercado...</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-md w-full max-w-md mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Indicadores de Mercado en Tiempo Real</h3>
        {error && (
          <div className="text-sm text-red-600 italic" title={error}>
            ⚠️ Usando datos de respaldo
          </div>
        )}
      </div>

      <div className="flex flex-col gap-3">
        {acciones.map(({ simbolo, precio, cambio, porcentaje_cambio }) => (
          <div
            key={simbolo}
            className="bg-blue-50 rounded-lg p-4 flex flex-col justify-between"
          >
            <div className="flex justify-between font-semibold mb-1">
              <span className="text-gray-800">{simbolo}</span>
              <span className="text-blue-600">${precio.toFixed(2)}</span>
            </div>
            <div
              className={`flex justify-between text-sm ${
                cambio >= 0 ? 'text-green-600' : 'text-red-600'
              }`}
            >
              <span>
                {cambio >= 0 ? '+' : ''}
                {cambio.toFixed(2)}
              </span>
              <span>({porcentaje_cambio}%)</span>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center mt-4 text-xs text-gray-500 flex items-center justify-center gap-2">
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
        <span>Actualización automática cada 30 segundos</span>
      </div>

      {lastUpdate && (
        <div className="text-center mt-1 text-xs text-gray-400 italic">
          Última actualización: {lastUpdate.toLocaleTimeString('es-CL')}
        </div>
      )}
    </div>
  );
};

export default AccionesWidget;