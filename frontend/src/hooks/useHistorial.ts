import { useEffect, useState } from 'react';
import axios from 'axios';

export interface DatoHistorico {
  fecha: string;
  valor: number;
}

export const useHistorial = (indicador: string, anio: number) => {
  const [datos, setDatos] = useState<DatoHistorico[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios.get(`https://mindicador.cl/api/${indicador}/${anio}`)
      .then(res => {
        const serie = res.data.serie.map((item: any) => ({
          fecha: item.fecha.slice(0, 10),
          valor: item.valor,
        }));
        setDatos(serie.reverse());
      })
      .catch(err => console.error("Error al obtener histórico", err))
      .finally(() => setLoading(false));
  }, [indicador, anio]);

  return { datos, loading };
};


