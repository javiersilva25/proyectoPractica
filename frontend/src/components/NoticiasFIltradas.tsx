import { useState } from 'react';
import { useNoticias } from '../hooks/useNoticias';

const categorias = {
  laboral: { label: 'Laboral', count: 33, color: 'bg-green-100 text-green-800' },
  internacional: { label: 'Internacional', count: 47, color: 'bg-blue-100 text-blue-800' },
  economica: { label: 'Económica', count: 15, color: 'bg-yellow-100 text-yellow-800' },
  politica: { label: 'Política', count: 11, color: 'bg-purple-100 text-purple-800' },
  tributaria: { label: 'Tributaria', count: 2, color: 'bg-red-100 text-red-800' },
};

const NoticiasFiltradas = () => {
  const [categoria, setCategoria] = useState('laboral');
  const { noticias, loading, error } = useNoticias(categoria);
  const categoriaActual = categorias[categoria as keyof typeof categorias];

  const formatearFecha = (fechaString: string) => {
    const fecha = new Date(fechaString);
    const ahora = new Date();
    const diferencia = ahora.getTime() - fecha.getTime();
    const dias = Math.floor(diferencia / (1000 * 60 * 60 * 24));

    if (dias === 0) return 'Hoy';
    if (dias === 1) return 'Ayer';
    if (dias < 7) return `${dias}d`;
    return fecha.toLocaleDateString('es-CL', { day: 'numeric', month: 'short' });
  };

  const truncateText = (text: string, maxLength: number) => {
    return text.length <= maxLength ? text : text.slice(0, maxLength) + '...';
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 max-h-[460px] flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-semibold text-gray-900">Noticias</h3>
            <p className="text-xs text-gray-500">{noticias.length} encontradas</p>
          </div>
          <div className="relative">
            <select
              value={categoria}
              onChange={(e) => setCategoria(e.target.value)}
              className="appearance-none bg-white border border-gray-300 rounded-md px-3 py-2 pr-8 text-sm text-gray-700 font-medium shadow-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              {Object.entries(categorias).map(([key, cat]) => (
                <option key={key} value={key}>
                  {cat.label} ({cat.count})
                </option>
              ))}
            </select>
            <svg
              className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <div className="mt-2">
          <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${categoriaActual.color}`}>
            {categoriaActual.label}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-3 flex-1 overflow-y-auto space-y-2">
        {loading && (
          <div className="flex justify-center items-center py-6 text-sm text-gray-600">
            <div className="w-5 h-5 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin mr-2" />
            Cargando...
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 text-sm rounded-md p-3 flex items-center gap-2">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            Error: {error}
          </div>
        )}

        {!loading && !error && noticias.length === 0 && (
          <div className="text-center py-10 text-sm text-gray-500">
            <div className="w-12 h-12 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-2">
              <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            No hay noticias disponibles
          </div>
        )}

        {!loading && !error && noticias.map((noticia) => (
          <div
            key={noticia.id}
            className="group bg-white border border-gray-200 hover:border-blue-400 rounded-lg p-3 transition"
          >
            <div className="flex justify-between items-start gap-3">
              <div className="flex-1">
                <a href={noticia.url} target="_blank" rel="noopener noreferrer" className="block">
                  <h4 className="font-medium text-sm text-gray-900 group-hover:text-blue-700 line-clamp-2 mb-1">
                    {truncateText(noticia.titulo, 100)}
                  </h4>
                </a>
                <div className="flex gap-4 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8a9 9 0 100-18 9 9 0 000 18z" />
                    </svg>
                    {noticia.fuente}
                  </span>
                  <span className="flex items-center gap-1">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {formatearFecha(noticia.fecha_scraping)}
                  </span>
                </div>
              </div>
              <a
                href={noticia.url}
                target="_blank"
                rel="noopener noreferrer"
                className="w-6 h-6 border border-gray-200 hover:border-blue-400 text-gray-400 hover:text-blue-600 rounded flex items-center justify-center transition"
              >
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      {!loading && !error && noticias.length > 0 && (
        <div className="bg-gray-50 border-t border-gray-200 px-4 py-2 text-xs text-gray-500 flex justify-between items-center">

        </div>
      )}
    </div>
  );
};

export default NoticiasFiltradas;
