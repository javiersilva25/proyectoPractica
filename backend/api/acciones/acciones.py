# acciones.py
import requests
import time
import os
from typing import List, Dict, Any
from django.core.cache import cache
import threading
import logging

logger = logging.getLogger(__name__)

class AccionesService:
    def __init__(self):
        self.API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "2RCP7B03LNGI0QWCN")
        self.url = "https://www.alphavantage.co/query"
        self.simbolos = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        self.cache_timeout = 300  # 5 minutos
        
        print(f"🔑 Alpha Vantage API Key: {self.API_KEY}")
    
    def obtener_cotizacion(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene la cotización de un símbolo específico"""
        cache_key = f"accion_{simbolo}"
        
        # Verificar cache primero
        try:
            cached_data = cache.get(cache_key)
            if cached_data and cached_data.get("success"):
                print(f"✅ Cache hit para {simbolo}")
                return cached_data
        except Exception as e:
            print(f"⚠️ Error accediendo al cache para {simbolo}: {e}")
        
        # Obtener datos de la API
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": simbolo,
            "apikey": self.API_KEY
        }
        
        url_completa = f"{self.url}?function=GLOBAL_QUOTE&symbol={simbolo}&apikey={self.API_KEY}"
        print(f"🌐 Llamando API para {simbolo}: {url_completa}")
        
        try:
            response = requests.get(self.url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            print(f"📡 Respuesta API para {simbolo}:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Keys en respuesta: {list(data.keys()) if isinstance(data, dict) else 'No es dict'}")
            print(f"   Respuesta completa: {data}")
            
            # Verificar diferentes tipos de respuesta de error
            if "Note" in data:
                error_msg = f"Rate limit excedido: {data['Note']}"
                print(f"❌ {error_msg}")
                return {
                    "simbolo": simbolo,
                    "error": error_msg,
                    "success": False,
                    "timestamp": int(time.time())
                }
            
            if "Error Message" in data:
                error_msg = f"Error de API: {data['Error Message']}"
                print(f"❌ {error_msg}")
                return {
                    "simbolo": simbolo,
                    "error": error_msg,
                    "success": False,
                    "timestamp": int(time.time())
                }
            
            if "Information" in data:
                error_msg = f"Información de API: {data['Information']}"
                print(f"❌ {error_msg}")
                return {
                    "simbolo": simbolo,
                    "error": error_msg,
                    "success": False,
                    "timestamp": int(time.time())
                }
            
            # Verificar si tenemos Global Quote
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                print(f"✅ Global Quote encontrado para {simbolo}: {quote}")
                
                # Obtener valores con manejo de errores
                try:
                    precio = float(quote.get("05. price", 0))
                    cambio = float(quote.get("09. change", 0))
                    porcentaje_cambio = quote.get("10. change percent", "0%").replace("%", "")
                    
                    resultado = {
                        "simbolo": simbolo,
                        "precio": precio,
                        "cambio": cambio,
                        "porcentaje_cambio": porcentaje_cambio,
                        "success": True,
                        "timestamp": int(time.time()),
                        "volumen": quote.get("06. volume", "N/A"),
                        "ultimo_dia_trading": quote.get("07. latest trading day", "N/A")
                    }
                    
                    # Guardar en cache
                    try:
                        cache.set(cache_key, resultado, self.cache_timeout)
                        print(f"💾 Datos de {simbolo} guardados en cache")
                    except Exception as e:
                        print(f"⚠️ Error guardando en cache para {simbolo}: {e}")
                    
                    return resultado
                    
                except (ValueError, TypeError) as e:
                    error_msg = f"Error procesando datos numéricos para {simbolo}: {e}"
                    print(f"❌ {error_msg}")
                    return {
                        "simbolo": simbolo,
                        "error": error_msg,
                        "success": False,
                        "timestamp": int(time.time())
                    }
            
            # Si llegamos aquí, no hay Global Quote
            error_msg = f"No se encontró 'Global Quote' en la respuesta para {simbolo}"
            print(f"❌ {error_msg}")
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time()),
                "respuesta_api": data  # Para debugging
            }
                
        except requests.exceptions.Timeout:
            error_msg = f"Timeout obteniendo datos para {simbolo}"
            print(f"❌ {error_msg}")
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time())
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"Error de conexión para {simbolo}: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time())
            }
        except Exception as e:
            error_msg = f"Error inesperado para {simbolo}: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time())
            }
    
    def obtener_todas_las_acciones(self, simbolos: List[str] = None) -> Dict[str, Any]:
        """Obtiene TODAS las acciones, con fallback a datos de prueba"""
        if simbolos is None:
            simbolos = self.simbolos
        
        simbolos = [s.upper().strip() for s in simbolos[:5]]
        print(f"🎯 Obteniendo acciones para: {simbolos}")
        
        resultados = []
        
        # Intentar obtener cada símbolo
        for i, simbolo in enumerate(simbolos):
            if i > 0:
                print(f"⏳ Esperando 12 segundos antes de llamar API para {simbolo}...")
                time.sleep(12)
            
            resultado = self.obtener_cotizacion(simbolo)
            resultados.append(resultado)
        
        # Contar exitosas
        exitosas = [r for r in resultados if r.get("success")]
        fallidas = [r for r in resultados if not r.get("success")]
        
        print(f"📊 Resultados: {len(exitosas)} exitosas, {len(fallidas)} fallidas")
        
        # Si no hay ninguna exitosa, usar datos de fallback
        if len(exitosas) == 0:
            print("🔄 No hay datos exitosos, usando fallback")
            resultados = self._generar_datos_fallback(simbolos)
        
        return {
            "acciones": resultados,
            "total": len(resultados),
            "exitosas": len(exitosas),
            "fallidas": len(fallidas),
            "simbolos_solicitados": simbolos
        }
    
    def _generar_datos_fallback(self, simbolos: List[str]) -> List[Dict[str, Any]]:
        """Genera datos de fallback realistas"""
        import random
        
        precios_base = {
            "AAPL": 175.43,
            "GOOGL": 142.65, 
            "MSFT": 412.89,
            "TSLA": 248.50,
            "AMZN": 155.78
        }
        
        resultados = []
        for simbolo in simbolos:
            precio_base = precios_base.get(simbolo, 100.0)
            precio = precio_base + random.uniform(-5, 5)
            cambio = random.uniform(-3, 3)
            porcentaje = (cambio / precio) * 100
            
            resultados.append({
                "simbolo": simbolo,
                "precio": round(precio, 2),
                "cambio": round(cambio, 2),
                "porcentaje_cambio": f"{porcentaje:.2f}",
                "success": True,
                "timestamp": int(time.time()),
                "fuente": "fallback"
            })
        
        return resultados

# Instancia del servicio
acciones_service = AccionesService()