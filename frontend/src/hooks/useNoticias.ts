import { useEffect, useState } from 'react';
import axios from 'axios';

export interface Noticia {
  id: number;
  titulo: string;
  url: string;
  categoria: string;
  fuente: string;
  fecha_publicacion: string | null;
  fecha_scraping: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useNoticias = (categoria: string) => {
  const [noticias, setNoticias] = useState<Noticia[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    axios
      .get(`${API_BASE_URL}/api/noticias/`, {
        params: { categoria },
        timeout: 10000,
        headers: {
          'Content-Type': 'application/json',
        }
      })
      .then((res) => {
        console.log("🟢 Noticias recibidas:", res.data.results);
        setNoticias(res.data.results || []);
      })
      .catch((err) => {
        console.error("❌ Error al obtener noticias", err);
        setError("No se pudieron cargar las noticias.");
        setNoticias([]);
      })
      .finally(() => setLoading(false));
  }, [categoria]);

  return { noticias, loading, error };
};