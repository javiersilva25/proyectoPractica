// src/hooks/useNoticias.ts
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

export const useNoticias = (categoria: string) => {
  const [noticias, setNoticias] = useState<Noticia[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  axios
    .get(`http://localhost:8000/api/noticias/?categoria=${categoria}`)
    .then((res) => {
      console.log("🟢 Noticias recibidas:", res.data.results);
      setNoticias(res.data.results);
    })
    .catch((err) => console.error("Error al obtener noticias", err))
    .finally(() => setLoading(false));
}, [categoria]);


  return { noticias, loading };
};
