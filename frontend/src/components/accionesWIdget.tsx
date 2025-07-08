// components/accionesWIdget.tsx
import React, { useState, useEffect } from 'react';

const AccionesWidget = () => {
  const [lastUpdate, setLastUpdate] = useState(new Date());
  
  const stockData = [
    { symbol: 'AAPL', price: '$209.95', change: '-3.60', percentage: '(-1.69%)', isNegative: true },
    { symbol: 'GOOGL', price: '$176.79', change: '-2.74', percentage: '(-1.53%)', isNegative: true },
    { symbol: 'MSFT', price: '$497.72', change: '-1.12', percentage: '(-0.22%)', isNegative: true },
    { symbol: 'TSLA', price: '$293.94', change: '-21.41', percentage: '(-6.79%)', isNegative: true },
    { symbol: 'AMZN', price: '$223.47', change: '+0.06', percentage: '(0.03%)', isNegative: false },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdate(new Date());
      // Aquí podrías actualizar los datos reales
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 h-full">
      {/* Header */}
      <div className="border-b border-gray-200 pb-3 mb-4">
        <h3 className="text-lg font-semibold text-gray-800 text-center">
          Indicadores de Mercado
        </h3>
        <p className="text-sm text-gray-500 text-center mt-1">
          En Tiempo Real
        </p>
      </div>

      {/* Stock Table */}
      <div className="space-y-3">
        {stockData.map((stock, index) => (
          <div 
            key={index} 
            className="flex justify-between items-center py-2 px-3 rounded-lg hover:bg-gray-50 transition-colors duration-200 border-l-4 border-transparent hover:border-blue-400"
          >
            {/* Left side - Symbol and Price */}
            <div className="flex flex-col">
              <span className="font-bold text-gray-800 text-sm">
                {stock.symbol}
              </span>
              <span className="text-xs text-gray-500">
                {stock.price}
              </span>
            </div>
            
            {/* Right side - Change and Percentage */}
            <div className="flex flex-col items-end">
              <span className={`font-semibold text-sm ${
                stock.isNegative ? 'text-red-600' : 'text-green-600'
              }`}>
                {stock.change}
              </span>
              <span className={`text-xs ${
                stock.isNegative ? 'text-red-500' : 'text-green-500'
              }`}>
                {stock.percentage}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex items-center justify-center text-xs text-gray-500">
          <div className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></div>
          <span>Actualización automática cada 30 segundos</span>
        </div>
      </div>
    </div>
  );
};

export default AccionesWidget;
