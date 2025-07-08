import { useState } from 'react';
import { useNoticias } from '../hooks/useNoticias';

const categorias = {
  politica: 'Política',
  internacional: 'Internacional',
  economica: 'Económica',
  tributaria: 'Tributaria',
  laboral: 'Laboral',
};

const NoticiasFiltradas = () => {
  const [categoria, setCategoria] = useState('economica');
  const { noticias, loading } = useNoticias(categoria);

  return (
    <div className="bg-gray-100 p-6 rounded-xl shadow-md mt-6">
      {/* Encabezado */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
        <h3 className="text-xl font-semibold text-gray-800">
          Noticias por Categoría
        </h3>
        <select
          value={categoria}
          onChange={(e) => setCategoria(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md text-sm"
        >
          {Object.entries(categorias).map(([key, label]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
      </div>

      {/* Lista de noticias */}
      {loading ? (
        <p className="text-sm text-gray-600">Cargando noticias...</p>
      ) : (
        <ul className="mt-4 space-y-4 max-h-80 overflow-y-auto">
          {noticias.map((n) => (
            <li
              key={n.id}
              className="flex flex-col border-b border-gray-300 pb-2 last:border-none"
            >
              <a
                href={n.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-base font-semibold text-blue-800 hover:underline"
              >
                {n.titulo}
                <small className="ml-2 text-gray-500 font-normal text-sm">
                  ({n.fuente})
                </small>
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default NoticiasFiltradas;
