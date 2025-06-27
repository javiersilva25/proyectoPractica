import { useState } from 'react';
import { useNoticias } from '../hooks/useNoticias';

const categorias = {
  politica: 'Política',
  internacional: 'Internacional',
  economica: 'Económica',
};

const NoticiasFiltradas = () => {
  const [categoria, setCategoria] = useState('economica');
  const { noticias, loading } = useNoticias(categoria);

  return (
    <div className="noticias-container">
      <div className="noticias-header">
        <h3>Noticias por Categoría </h3>
        <select
          value={categoria}
          onChange={(e) => setCategoria(e.target.value)}
          style={{
            padding: '0.2rem 0.5rem',
            borderRadius: '8px',
            border: '1px solid #ccc',
            fontSize: '1rem',
          }}
        >
          {Object.entries(categorias).map(([key, label]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <p>Cargando noticias...</p>
      ) : (
        <ul className="lista-noticias">
          {noticias.map((n) => (
            <li key={n.id}>
              <a href={n.url} target="_blank" rel="noopener noreferrer">
                {n.titulo} <small>({n.fuente})</small>
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default NoticiasFiltradas;
