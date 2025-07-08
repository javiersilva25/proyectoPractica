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
        setAcciones([
          { simbolo: "AAPL", precio: 175.43, cambio: 2.15, porcentaje_cambio: "1.24" },
          { simbolo: "GOOGL", precio: 2845.67, cambio: -12.34, porcentaje_cambio: "-0.43" },
          { simbolo: "MSFT", precio: 412.89, cambio: 5.67, porcentaje_cambio: "1.39" },
          { simbolo: "TSLA", precio: 248.50, cambio: -3.25, porcentaje_cambio: "-1.29" },
          { simbolo: "AMZN", precio: 3456.78, cambio: 15.23, porcentaje_cambio: "0.44" }
        ]);
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
      <div className="bg-white p-4 rounded-lg shadow text-center">
        <div className="animate-spin border-4 border-gray-200 border-t-blue-500 rounded-full w-8 h-8 mx-auto mb-2" />
        <p className="text-sm text-gray-700">Cargando indicadores del mercado...</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-md w-full max-w-md">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Indicadores de Mercado en Tiempo Real</h3>
        {error && (
          <div className="text-sm text-red-600 italic">
            ⚠️ Usando datos de respaldo
          </div>
        )}
      </div>

      <div className="flex flex-col gap-3">
        {acciones.map((accion) => (
          <div key={accion.simbolo} className="bg-blue-50 rounded-lg p-4 flex flex-col justify-between">
            <div className="flex justify-between font-semibold mb-1">
              <span className="text-gray-800">{accion.simbolo}</span>
              <span className="text-blue-600">${accion.precio.toFixed(2)}</span>
            </div>
            <div className={`flex justify-between text-sm ${accion.cambio >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              <span>
                {accion.cambio >= 0 ? '+' : ''}
                {accion.cambio.toFixed(2)}
              </span>
              <span>({accion.porcentaje_cambio}%)</span>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center mt-4 text-xs text-gray-500">
        🔄 Actualización automática cada 30 segundos
      </div>
    </div>
  );
};

export default AccionesWidget;
