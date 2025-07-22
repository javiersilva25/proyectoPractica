import React, { useState, useEffect, useCallback } from 'react';

interface Indice {
  simbolo: string;
  nombre: string;
  precio: number;
  cambio: number;
  porcentaje_cambio: string;
  success?: boolean;
  fuente?: string;
  ultima_actualizacion?: string;
}

interface ApiResponse {
  indices: Indice[];
  status: string;
  total: number;
  exitosos: number;
  fuente?: string;
  error?: string;
  auto_actualizacion?: {
    habilitada: boolean;
    intervalo_minutos: number;
    ultima_actualizacion: string;
    proxima_actualizacion: string;
  };
}

const IndiceSkeleton = () => (
  <div className="animate-pulse">
    <div className="bg-gray-100 rounded-lg p-4 border border-gray-300">
      <div className="flex justify-between items-center mb-2">
        <div className="h-4 bg-gray-300 rounded w-20"></div>
        <div className="h-4 bg-gray-300 rounded w-24"></div>
      </div>
      <div className="flex justify-between items-center">
        <div className="h-3 bg-gray-300 rounded w-24"></div>
        <div className="h-3 bg-gray-300 rounded w-18"></div>
      </div>
    </div>
  </div>
);

const IndicesGlobalesWidget: React.FC = () => {
  const [indices, setIndices] = useState<Indice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [apiInfo, setApiInfo] = useState<ApiResponse['auto_actualizacion'] | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchIndices = useCallback(async () => {
    try {
      if (!loading) setRefreshing(true);

      const response = await fetch('http://localhost:8000/api/acciones/indices/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
      });

      const data: ApiResponse = await response.json();

      if (response.ok && data.status === 'success') {
        const exitosos = data.indices.filter(indice => indice.success !== false);
        if (exitosos.length > 0) {
          setIndices(exitosos);
          setApiInfo(data.auto_actualizacion || null);
          setError(null);
          setLastUpdate(new Date());
        } else {
          throw new Error('No se recibieron índices válidos');
        }
      } else {
        throw new Error(data.error || `Error del servidor: ${response.status}`);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMessage);
      setIndices([]);
      setLastUpdate(new Date());
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [loading]);

  useEffect(() => {
    fetchIndices();
    const interval = setInterval(fetchIndices, 300000);
    return () => clearInterval(interval);
  }, [fetchIndices]);

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-md border border-gray-300 overflow-hidden min-h-[520px]">
        <div className="bg-blue-600 p-4 rounded-t-xl">
          <h3 className="text-lg font-semibold text-white">Índices Globales</h3>
        </div>
        <div className="p-4 space-y-3">
          {[...Array(8)].map((_, i) => (
            <IndiceSkeleton key={i} />
          ))}
        </div>
      </div>
    );
  }

  if (error || indices.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md border border-gray-300 overflow-hidden min-h-[520px]">
        <div className="bg-blue-600 p-4 rounded-t-xl">
          <h3 className="text-lg font-semibold text-white">Índices No Disponibles</h3>
        </div>
        <div className="p-6 text-center">
          <div className="bg-gray-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl font-bold text-gray-700">!</span>
          </div>
          <h4 className="text-lg font-semibold text-gray-800 mb-2">
            No se pudieron obtener datos de índices globales
          </h4>
          <p className="text-sm text-gray-600 mb-4 max-w-xs mx-auto">
            {error || 'Los servicios de índices no están disponibles'}
          </p>
          <button
            onClick={fetchIndices}
            disabled={loading || refreshing}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded transition-colors disabled:opacity-50"
          >
            {loading || refreshing ? 'Reintentando...' : 'Reintentar'}
          </button>
          {lastUpdate && (
            <div className="mt-3 text-xs text-gray-500">
              Último intento: {lastUpdate.toLocaleTimeString('es-CL')}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-md border border-gray-300 overflow-hidden min-h-[520px]">
      <div className="bg-blue-600 p-4 rounded-t-xl">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold text-white">Índices Globales</h3>
          <div className="flex items-center text-white text-sm">
            <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
            En Vivo
          </div>
        </div>
      </div>

      <div className="p-4 max-h-[420px] overflow-y-auto space-y-3">
        {indices.map(({ simbolo, nombre, precio, cambio, porcentaje_cambio, fuente }) => {
          const isPositive = cambio >= 0;
          const changeColor = isPositive ? 'text-green-600' : 'text-red-600';

          return (
            <div
              key={simbolo}
              className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:bg-gray-100 transition-colors"
            >
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-semibold text-gray-800">{nombre}</div>
                  {fuente && (
                    <div className="text-xs text-gray-500">
                      {fuente.replace('_', ' ')}
                    </div>
                  )}
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-800">
                    {precio.toLocaleString('es-CL', { maximumFractionDigits: 2 })}
                  </div>
                  <div className={`text-sm ${changeColor} font-medium`}>
                    {isPositive ? '+' : '-'}{Math.abs(cambio).toFixed(2)} ({porcentaje_cambio}%)
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="border-t border-gray-300 pt-3 mt-4 text-center">
        <div className="flex items-center justify-center gap-2 text-sm text-gray-600 mb-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span>Mercados globales</span>
        </div>
        {lastUpdate && (
          <div className="text-xs text-gray-500 mb-2">
            {lastUpdate.toLocaleTimeString('es-CL')}
          </div>
        )}
        {apiInfo && (
          <div className="text-xs text-gray-400 mb-2">
            Actualización automática cada {apiInfo.intervalo_minutos} min
          </div>
        )}
        <button
          onClick={fetchIndices}
          disabled={refreshing}
          className="text-sm text-blue-600 hover:text-blue-800 underline disabled:opacity-50"
        >
          {refreshing ? 'Actualizando...' : 'Actualizar manualmente'}
        </button>
      </div>
    </div>
  );
};

export default IndicesGlobalesWidget;
