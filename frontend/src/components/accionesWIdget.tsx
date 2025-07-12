import React, { useState, useEffect, useCallback } from 'react';

interface Accion {
  simbolo: string;
  precio: number;
  cambio: number;
  porcentaje_cambio: string;
  success?: boolean;
  fuente?: string;
  ultima_actualizacion?: string;
}

interface ApiResponse {
  acciones: Accion[];
  status: string;
  total: number;
  exitosas: number;
  fuente?: string;
  mensaje?: string;
  error?: string;
  auto_actualizacion?: {
    habilitada: boolean;
    intervalo_minutos: number;
    ultima_actualizacion: string;
    proxima_actualizacion: string;
  };
}

const AccionesWidget: React.FC = () => {
  const [acciones, setAcciones] = useState<Accion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [apiInfo, setApiInfo] = useState<ApiResponse['auto_actualizacion'] | null>(null);
  const [mensaje, setMensaje] = useState<string>('');

  const fetchAcciones = useCallback(async () => {
    try {
      setLoading(true);
      console.log('📊 Solicitando datos REALES de acciones...');
      
      const response = await fetch('http://localhost:8000/api/acciones/', {
        method: 'GET',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
      });

      const data: ApiResponse = await response.json();
      console.log('📊 Respuesta del backend:', data);

      if (response.ok && data.status === 'success') {
        if (data.acciones && Array.isArray(data.acciones) && data.acciones.length > 0) {
          // Solo usar acciones exitosas
          const accionesExitosas = data.acciones.filter(accion => accion.success !== false);
          
          if (accionesExitosas.length > 0) {
            setAcciones(accionesExitosas);
            setApiInfo(data.auto_actualizacion || null);
            setMensaje(data.mensaje || '');
            setError(null);
            setLastUpdate(new Date());
            
            console.log(`✅ ${accionesExitosas.length} acciones REALES cargadas`);
            console.log(`📡 Fuente: ${data.fuente}`);
          } else {
            throw new Error('No se recibieron acciones válidas');
          }
        } else {
          throw new Error('No se recibieron datos de acciones');
        }
      } else {
        // Error del servidor
        throw new Error(data.error || `Error del servidor: ${response.status}`);
      }
    } catch (err) {
      console.error('❌ Error al obtener acciones:', err);
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMessage);
      setAcciones([]); // NO hay datos de respaldo
      setMensaje('Error conectando con APIs de datos reales');
      setLastUpdate(new Date());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAcciones();

    // Actualizar cada 15 minutos
    const interval = setInterval(fetchAcciones, 300000);
    
    return () => clearInterval(interval);
  }, [fetchAcciones]);

  if (loading) {
    return (
      <div className="bg-white p-4 rounded-lg shadow text-center">
        <div className="animate-spin border-4 border-gray-200 border-t-blue-500 rounded-full w-8 h-8 mx-auto mb-2" />
        <p className="text-sm text-gray-700">Conectando con APIs reales...</p>
      </div>
    );
  }

  if (error || acciones.length === 0) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-md w-full max-w-md mx-auto">
        <div className="text-center">
          <div className="text-red-500 text-4xl mb-2">⚠️</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">
            APIs No Disponibles
          </h3>
          <p className="text-sm text-gray-600 mb-4">
            {error || 'No se pudieron obtener datos reales de las APIs de mercado'}
          </p>
          <button
            onClick={fetchAcciones}
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:opacity-50"
          >
            {loading ? 'Reintentando...' : 'Reintentar'}
          </button>
        </div>
        
        {lastUpdate && (
          <div className="text-center mt-4 text-xs text-gray-400">
            Último intento: {lastUpdate.toLocaleTimeString('es-CL')}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-md w-full max-w-md mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">
          Datos Reales de Mercado
        </h3>
        <div className="text-sm text-green-600 italic flex items-center">
          <div className="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse"></div>
          En Vivo
        </div>
      </div>

      {/* Mostrar mensaje del backend */}
      {mensaje && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-2 mb-4">
          <p className="text-xs text-green-700">{mensaje}</p>
        </div>
      )}

      <div className="flex flex-col gap-3">
        {acciones.map(({ simbolo, precio, cambio, porcentaje_cambio, fuente }) => (
          <div
            key={simbolo}
            className="bg-blue-50 rounded-lg p-4 flex flex-col justify-between hover:bg-blue-100 transition-colors border-l-4 border-green-500"
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
                ${Math.abs(cambio).toFixed(2)}
              </span>
              <span>({porcentaje_cambio}%)</span>
            </div>
            {fuente && (
              <div className="text-xs text-gray-500 mt-1">
                Fuente: {fuente.replace('_', ' ')}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Info de actualización */}
      <div className="text-center mt-4 text-xs text-gray-500">
        <div className="flex items-center justify-center gap-2 mb-1">
        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
         <span>Datos reales en tiempo real</span>
       </div>
       
       {apiInfo && (
         <div className="text-gray-400">
           Actualización automática cada {apiInfo.intervalo_minutos} min
         </div>
       )}
       
       {lastUpdate && (
         <div className="text-gray-400 italic">
           Última actualización: {lastUpdate.toLocaleTimeString('es-CL')}
         </div>
       )}
     </div>

     {/* Botón de actualización manual */}
     <div className="text-center mt-2">
       <button
         onClick={fetchAcciones}
         disabled={loading}
         className="text-xs text-blue-600 hover:text-blue-800 underline disabled:opacity-50"
       >
         {loading ? 'Actualizando...' : 'Actualizar datos reales'}
       </button>
     </div>
   </div>
 );
};

export default AccionesWidget;