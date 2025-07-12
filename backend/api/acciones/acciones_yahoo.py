# acciones_yahoo.py - Yahoo Finance simplificado
import yfinance as yf
import time
import threading
from typing import List, Dict, Any
from django.core.cache import cache
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AccionesYahooService:
    def __init__(self):
        self.simbolos = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        self.cache_timeout = 900  # 15 minutos
        self.update_interval = 900  # 15 minutos
        self.is_updating = False
        self.last_update = None
        
        print("🟡 Yahoo Finance simplificado - CONSULTAS CADA 15 MINUTOS")
        self._start_auto_update()
    
    def _start_auto_update(self):
        """Inicia consultas automáticas cada 15 minutos"""
        def update_loop():
            # Esperar 2 minutos antes de la primera consulta
            time.sleep(120)
            
            while True:
                try:
                    current_time = datetime.now().strftime('%H:%M:%S')
                    print(f"🕐 {current_time} - Consultando Yahoo Finance cada 15 min...")
                    self._consultar_todas_las_acciones()
                    self.last_update = datetime.now()
                    update_time = self.last_update.strftime('%H:%M:%S')
                    print(f"✅ Consulta Yahoo completada a las {update_time}")
                except Exception as e:
                    print(f"❌ Error en consulta automática Yahoo: {e}")
                
                print(f"⏳ Próxima consulta Yahoo en 15 minutos...")
                time.sleep(self.update_interval)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        print("🚀 Consultas automáticas Yahoo cada 15 minutos iniciadas")
    
    def _consultar_todas_las_acciones(self):
        """Consulta todas las acciones y actualiza cache"""
        if self.is_updating:
            print("⚠️ Consulta Yahoo ya en progreso...")
            return
        
        self.is_updating = True
        print(f"🔄 Consultando {len(self.simbolos)} acciones en Yahoo...")
        
        try:
            exitosas = 0
            for i, simbolo in enumerate(self.simbolos):
                try:
                    if i > 0:
                        time.sleep(2)  # Pausa de 2 segundos entre consultas
                    
                    print(f"🔄 Obteniendo {simbolo}...")
                    resultado = self._obtener_datos_accion(simbolo)
                    
                    if resultado.get("success"):
                        exitosas += 1
                        precio = resultado.get("precio", 0)
                        cambio = resultado.get("cambio", 0)
                        print(f"✅ {simbolo}: ${precio:.2f} ({cambio:+.2f})")
                        
                        # Guardar en cache
                        cache_key = f"yahoo_accion_{simbolo}"
                        cache.set(cache_key, resultado, self.cache_timeout)
                    else:
                        print(f"❌ Error {simbolo}: {resultado.get('error', 'Sin datos')}")
                        
                except Exception as e:
                    print(f"❌ Error consultando {simbolo}: {e}")
            
            print(f"📊 Yahoo Finance: {exitosas}/{len(self.simbolos)} acciones obtenidas")
                    
        finally:
            self.is_updating = False
    
    def _obtener_datos_accion(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene datos de una acción usando yfinance básico"""
        try:
            # Crear ticker sin configuración especial
            ticker = yf.Ticker(simbolo)
            
            # Obtener datos históricos de los últimos 2 días
            hist = ticker.history(period="2d")
            
            if not hist.empty and len(hist) >= 1:
                # Obtener precio actual (último precio de cierre)
                precio_actual = float(hist['Close'].iloc[-1])
                
                # Calcular cambio si hay datos del día anterior
                if len(hist) >= 2:
                    precio_anterior = float(hist['Close'].iloc[-2])
                    cambio = precio_actual - precio_anterior
                    porcentaje_cambio = (cambio / precio_anterior) * 100
                else:
                    cambio = 0
                    porcentaje_cambio = 0
                
                # Obtener volumen
                volumen = int(hist['Volume'].iloc[-1]) if len(hist['Volume']) > 0 else 0
                
                return {
                    "simbolo": simbolo,
                    "precio": round(precio_actual, 2),
                    "cambio": round(cambio, 2),
                    "porcentaje_cambio": f"{porcentaje_cambio:.2f}",
                    "success": True,
                    "timestamp": int(time.time()),
                    "volumen": f"{volumen:,}" if volumen > 0 else "N/A",
                    "ultimo_dia_trading": hist.index[-1].strftime('%Y-%m-%d'),
                    "fuente": "Yahoo Finance",
                    "ultima_actualizacion": datetime.now().strftime('%H:%M:%S')
                }
            
            # Si no hay datos históricos, intentar con info básica
            try:
                info = ticker.info
                if info and 'regularMarketPrice' in info:
                    precio = float(info['regularMarketPrice'])
                    cambio = float(info.get('regularMarketChange', 0))
                    porcentaje = float(info.get('regularMarketChangePercent', 0))
                    
                    return {
                        "simbolo": simbolo,
                        "precio": round(precio, 2),
                        "cambio": round(cambio, 2),
                        "porcentaje_cambio": f"{porcentaje:.2f}",
                        "success": True,
                        "timestamp": int(time.time()),
                        "volumen": str(info.get('regularMarketVolume', 'N/A')),
                        "ultimo_dia_trading": datetime.now().strftime('%Y-%m-%d'),
                        "fuente": "Yahoo Finance",
                        "ultima_actualizacion": datetime.now().strftime('%H:%M:%S')
                    }
            except:
                pass
            
            return {
                "simbolo": simbolo,
                "error": "No se pudieron obtener datos de Yahoo Finance",
                "success": False,
                "timestamp": int(time.time())
            }
            
        except Exception as e:
            return {
                "simbolo": simbolo,
                "error": f"Error obteniendo datos: {str(e)}",
                "success": False,
                "timestamp": int(time.time())
            }
    
    def obtener_cotizacion(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene cotización de una acción (con cache)"""
        cache_key = f"yahoo_accion_{simbolo}"
        
        # Verificar cache primero
        try:
            cached_data = cache.get(cache_key)
            if cached_data and cached_data.get("success"):
                timestamp = cached_data.get("timestamp", 0)
                if time.time() - timestamp < self.cache_timeout:
                    return cached_data
        except Exception:
            pass
        
        # Si no hay cache válido, obtener datos frescos
        return self._obtener_datos_accion(simbolo)
    
    def obtener_todas_las_acciones(self, simbolos: List[str] = None) -> Dict[str, Any]:
        """Obtiene todas las acciones"""
        if simbolos is None:
            simbolos = self.simbolos
        
        simbolos = [s.upper().strip() for s in simbolos[:5]]
        resultados = []
        exitosas = 0
        
        for simbolo in simbolos:
            resultado = self.obtener_cotizacion(simbolo)
            resultados.append(resultado)
            if resultado.get("success"):
                exitosas += 1
        
        # Calcular próxima actualización
        proxima_actualizacion = "N/A"
        if self.last_update:
            proxima = self.last_update + timedelta(minutes=15)
            proxima_actualizacion = proxima.strftime('%H:%M:%S')
        
        return {
            "acciones": resultados,
            "total": len(resultados),
            "exitosas": exitosas,
            "simbolos_solicitados": simbolos,
            "fuente": "Yahoo Finance",
            "ultima_actualizacion_automatica": self.last_update.strftime('%H:%M:%S') if self.last_update else "Pendiente",
            "proxima_actualizacion": proxima_actualizacion,
            "intervalo_consultas": "15 minutos"
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Estado del servicio"""
        return {
            "servicio": "Yahoo Finance Simple",
            "auto_actualizacion": True,
            "intervalo_consultas": "15 minutos",
            "ultima_consulta": self.last_update.strftime('%Y-%m-%d %H:%M:%S') if self.last_update else "Nunca",
            "consultando_ahora": self.is_updating,
            "simbolos_monitoreados": self.simbolos,
            "cache_timeout": f"{self.cache_timeout // 60} minutos"
        }

# Instancia del servicio
acciones_yahoo_service = AccionesYahooService()