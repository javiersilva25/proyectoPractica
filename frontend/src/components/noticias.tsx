import { useEffect, useState } from 'react';
import axios from 'axios';
import type { Noticia } from '../types/noticia';

const Noticias = () => {
  const [noticias, setNoticias] = useState<Noticia[]>([]);

  useEffect(() => {
  axios.get<Noticia[]>('http://localhost:8000/api/noticias/')
    .then(res => {
      console.log("Noticias recibidas:", res.data);
      setNoticias(res.data);
    })
    .catch(err => console.error("Error al cargar noticias", err));
}, []);


  return (
    <div>
      {noticias.length === 0 ? (
        <p>No hay noticias disponibles.</p>
      ) : (
        noticias.map((noticia, index) => (
          <div key={index}>
            <h4>{noticia.titulo}</h4>
            <button onClick={() => window.open(noticia.url, '_blank')}>
              Ver noticia
            </button>
            <hr />
          </div>
        ))
      )}
    </div>
  );
};

export default Noticias;
