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

export const useIndicadores = () => {
  const [datos, setDatos] = useState<Indicadores>({});
  const [fecha, setFecha] = useState<string | null>(null);

  useEffect(() => {
    axios.get('https://mindicador.cl/api')
      .then(res => {
        const copia = { ...res.data };
        delete copia.version;
        delete copia.autor;
        setFecha(res.data.fecha);
        setDatos(copia);
      })
      .catch(err => console.error("Error al obtener indicadores", err));
  }, []);

  return { datos, fecha };
};
