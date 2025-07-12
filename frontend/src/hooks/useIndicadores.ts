import { useEffect, useState } from 'react';
import axios from 'axios';

interface Indicador {
  valor: number;
  nombre?: string;
  unidad_medida?: string;
}

interface Indicadores {
  [key: string]: Indicador;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useIndicadores = () => {
  const [datos, setDatos] = useState<Indicadores>({});
  const [fecha, setFecha] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    axios.get(`${API_BASE_URL}/api/indicadores/`, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then(res => {
        const copia = { ...res.data };
        setFecha(res.data.fecha);
        delete copia.fecha;
        setDatos(copia);
        setError(null);
      })
      .catch(err => {
        console.error("Error al obtener indicadores", err);
        setError("No se pudieron cargar los indicadores");
        // Datos de fallback
        setDatos({
          uf: { valor: 37500, unidad_medida: '$' },
          utm: { valor: 65967, unidad_medida: '$' },
          dolar: { valor: 980, unidad_medida: '$' },
          euro: { valor: 1020, unidad_medida: '$' },
        });
      })
      .finally(() => setLoading(false));
  }, []);

  return { datos, fecha, loading, error };
};