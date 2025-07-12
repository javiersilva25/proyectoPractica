# acciones.py - SOLO DATOS REALES DE ALPHA VANTAGE
import requests
import time
import os
import threading
from typing import List, Dict, Any
from django.core.cache import cache
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AccionesService:
    def __init__(self):
        self.API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "2RCP7B03LNGI0QWCN")
        self.url = "https://www.alphavantage.co/query"
        self.simbolos = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        self.cache_timeout = 900  # 15 minutos
        self.update_interval = 900  # 15 minutos en segundos
        self.is_updating = False
        self.last_update = None
        
        print(f"🔑 Alpha Vantage API Key: {self.API_KEY} - CONSULTAS CADA 15 MINUTOS")
        self._start_auto_update()
    
    def _start_auto_update(self):
        """Inicia el hilo de consultas automáticas cada 15 minutos"""
        def update_loop():
            # Esperar 5 minutos antes de la primera consulta (para no chocar con Yahoo)
            time.sleep(300)
            
            while True:
                try:
                    current_time = datetime.now().strftime('%H:%M:%S')
                    print(f"🕐 {current_time} - Iniciando consulta Alpha Vantage cada 15 min...")
                    self._update_all_cached_data()
                    self.last_update = datetime.now()
                    update_time = self.last_update.strftime('%H:%M:%S')
                    print(f"✅ Consulta Alpha Vantage completada a las {update_time}")
                except Exception as e:
                    print(f"❌ Error en consulta automática Alpha Vantage: {e}")
                
                # Esperar exactamente 15 minutos
                print(f"⏳ Próxima consulta Alpha Vantage en 15 minutos...")
                time.sleep(self.update_interval)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        print("🚀 Hilo de consultas Alpha Vantage cada 15 minutos iniciado")
    
    def _update_all_cached_data(self):
        """Consulta Alpha Vantage y actualiza los datos en caché"""
        if self.is_updating:
            print("⚠️ Consulta Alpha Vantage ya en progreso, saltando...")
            return
        
        self.is_updating = True
        print(f"🔄 Consultando Alpha Vantage para {len(self.simbolos)} acciones...")
        
        try:
            exitosas = 0
            for i, simbolo in enumerate(self.simbolos):
                if i > 0:
                    # Alpha Vantage permite 5 calls por minuto, esperamos 15 segundos
                    tiempo_espera = 300
                    print(f"⏳ Esperando {tiempo_espera}s antes de consultar {simbolo} (Alpha Vantage)...")
                    time.sleep(tiempo_espera)
                
                print(f"🔄 Consultando {simbolo} en Alpha Vantage...")
                resultado = self.obtener_cotizacion(simbolo)
                
                if resultado.get("success"):
                    exitosas += 1
                    precio = resultado.get("precio", 0)
                    cambio = resultado.get("cambio", 0)
                    print(f"✅ {simbolo}: ${precio:.2f} ({cambio:+.2f}) [Alpha Vantage]")
                else:
                    print(f"❌ Error consultando {simbolo}: {resultado.get('error', 'Unknown')}")
            
            print(f"📊 Consulta Alpha Vantage completada: {exitosas}/{len(self.simbolos)} acciones actualizadas")
                    
        finally:
            self.is_updating = False
    
    def obtener_cotizacion(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene la cotización REAL de un símbolo específico"""
        cache_key = f"alpha_accion_{simbolo}"
        
        # Verificar cache primero
        try:
            cached_data = cache.get(cache_key)
            if cached_data and cached_data.get("success"):
                timestamp = cached_data.get("timestamp", 0)
                if time.time() - timestamp < self.cache_timeout:
                    age_minutes = int((time.time() - timestamp) / 60)
                    return cached_data
        except Exception as e:
            print(f"⚠️ Error accediendo al cache para {simbolo}: {e}")
        
        # Obtener datos REALES de la API
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": simbolo,
            "apikey": self.API_KEY
        }
        
        try:
            response = requests.get(self.url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Verificar errores de API
            if "Note" in data:
                error_msg = f"Rate limit excedido: {data['Note']}"
                return {
                    "simbolo": simbolo,
                    "error": error_msg,
                    "success": False,
                    "timestamp": int(time.time())
                }
            
            if "Error Message" in data:
                error_msg = f"Error de API: {data['Error Message']}"
                return {
                    "simbolo": simbolo,
                    "error": error_msg,
                    "success": False,
                    "timestamp": int(time.time())
                }
            
            # Verificar si tenemos Global Quote REAL
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                
                try:
                    precio = float(quote.get("05. price", 0))
                    cambio = float(quote.get("09. change", 0))
                    porcentaje_cambio = quote.get("10. change percent", "0%").replace("%", "")
                    
                    if precio <= 0:
                        raise ValueError("Precio inválido recibido de la API")
                    
                    resultado = {
                        "simbolo": simbolo,
                        "precio": precio,
                        "cambio": cambio,
                        "porcentaje_cambio": porcentaje_cambio,
                        "success": True,
                        "timestamp": int(time.time()),
                        "volumen": quote.get("06. volume", "N/A"),
                        "ultimo_dia_trading": quote.get("07. latest trading day", "N/A"),
                        "fuente": "Alpha Vantage"
                    }
                    
                    # Guardar en cache
                    try:
                        cache.set(cache_key, resultado, self.cache_timeout)
                    except Exception as e:
                        print(f"⚠️ Error guardando en cache para {simbolo}: {e}")
                    
                    return resultado
                    
                except (ValueError, TypeError) as e:
                    error_msg = f"Error procesando datos REALES para {simbolo}: {e}"
                    return {
                        "simbolo": simbolo,
                        "error": error_msg,
                        "success": False,
                        "timestamp": int(time.time())
                    }
            
            # Si llegamos aquí, no hay Global Quote válido
            error_msg = f"No se encontraron datos reales válidos para {simbolo}"
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time())
            }
                
        except requests.exceptions.Timeout:
            error_msg = f"Timeout obteniendo datos REALES para {simbolo}"
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time())
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"Error de conexión para {simbolo}: {str(e)}"
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time())
            }
        except Exception as e:
            error_msg = f"Error inesperado para {simbolo}: {str(e)}"
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time())
            }
    
    def obtener_todas_las_acciones(self, simbolos: List[str] = None) -> Dict[str, Any]:
        """Obtiene TODAS las acciones REALES"""
        if simbolos is None:
            simbolos = self.simbolos
        
        simbolos = [s.upper().strip() for s in simbolos[:5]]
        
        resultados = []
        
        # Obtener cada símbolo (ya con cache integrado)
        for simbolo in simbolos:
            resultado = self.obtener_cotizacion(simbolo)
            resultados.append(resultado)
        
        # Contar exitosas
        exitosas = [r for r in resultados if r.get("success")]
        fallidas = [r for r in resultados if not r.get("success")]
        
        proxima_actualizacion = "N/A"
        if self.last_update:
            proxima = self.last_update + timedelta(minutes=15)
            proxima_actualizacion = proxima.strftime('%H:%M:%S')
        
        return {
            "acciones": resultados,
            "total": len(resultados),
            "exitosas": len(exitosas),
            "fallidas": len(fallidas),
            "simbolos_solicitados": simbolos,
            "fuente": "Alpha Vantage",
            "ultima_actualizacion_automatica": self.last_update.strftime('%H:%M:%S') if self.last_update else "Pendiente",
            "proxima_actualizacion": proxima_actualizacion,
            "intervalo_consultas": "15 minutos"
        }

# Instancia del servicio
acciones_service = AccionesService()