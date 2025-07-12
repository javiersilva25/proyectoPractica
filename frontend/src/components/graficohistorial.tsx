import { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';
import { useHistorial } from '../hooks/useHistorial';

const indicadoresDisponibles = {
  uf: 'UF',
  dolar: 'Dólar',
  euro: 'Euro',
  bitcoin: 'Bitcoin',
  utm: 'UTM',
  ipc: 'IPC',
  imacec: 'IMACEC',
  ivp: 'IVP',
  yen: 'Yen',
  libra_cobre: 'Cobre',
  tasa_desempleo: 'Desempleo',
  tpm: 'TPM',
  dolar_intercambio: 'Dólar Acuerdo',
};

const anios = Array.from({ length: 2025 - 2000 + 1 }, (_, i) => 2000 + i);

const GraficoHistorial = () => {
  const [indicador, setIndicador] = useState('uf');
  const [anio, setAnio] = useState(new Date().getFullYear());
  const { datos, loading } = useHistorial(indicador, anio);

  return (
    <div className="flex flex-col items-center text-center px-4 py-6 bg-white rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Valores Históricos</h3>

      {/* Selectores */}
      <div className="flex flex-wrap justify-center gap-4 mb-6">
        <select
          value={indicador}
          onChange={(e) => setIndicador(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md text-sm"
        >
          {Object.entries(indicadoresDisponibles).map(([key, nombre]) => (
            <option key={key} value={key}>
              {nombre}
            </option>
          ))}
        </select>

        <select
          value={anio}
          onChange={(e) => setAnio(Number(e.target.value))}
          className="px-3 py-2 border border-gray-300 rounded-md text-sm"
        >
          {anios.map((a) => (
            <option key={a} value={a}>
              {a}
            </option>
          ))}
        </select>
      </div>

      {/* Gráfico */}
      {loading ? (
        <p className="text-gray-500 text-sm">Cargando datos...</p>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={datos}>
            <CartesianGrid stroke="#e0e0e0" strokeDasharray="5 5" />
            <XAxis
              dataKey="fecha"
              tick={{ fontSize: 10, fill: '#555' }}
              tickFormatter={(str) => {
                const date = new Date(str);
                return `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}`;
              }}
            />
            <YAxis tick={{ fontSize: 10, fill: '#555' }} />
            <Tooltip
              formatter={(value: number) =>
                value.toLocaleString('es-CL', {
                  style: 'decimal',
                  maximumFractionDigits: 2,
                })
              }
              labelFormatter={(label) => `Fecha: ${label}`}
            />
            <Line
              type="monotone"
              dataKey="valor"
              stroke="#007bff"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default GraficoHistorial;
