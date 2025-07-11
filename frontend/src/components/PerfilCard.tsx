import React, { useEffect, useState } from 'react';
import { obtenerPerfil } from '../api/perfil';

export default function PerfilCard() {
  const [perfil, setPerfil] = useState<{ nombre: string; correo: string; rol: string } | null>(null);

  useEffect(() => {
    obtenerPerfil().then(res => setPerfil(res.data));
  }, []);

  if (!perfil) return <div className="p-4 bg-white shadow rounded">Cargando perfil...</div>;

  return (
    <div className="p-4 bg-white shadow rounded w-full md:max-w-xs">
      <h2 className="text-lg font-semibold mb-2">Perfil del Usuario</h2>
      <p><strong>Nombre:</strong> {perfil.nombre}</p>
      <p><strong>Correo:</strong> {perfil.correo}</p>
    </div>
  );
}
