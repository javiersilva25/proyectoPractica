# acciones.py - SOLO DATOS REALES DE ALPHA VANTAGE
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
        
        print(f"🔑 Alpha Vantage API Key: {self.API_KEY} - SOLO DATOS REALES")
    
    def obtener_cotizacion(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene la cotización REAL de un símbolo específico"""
        cache_key = f"alpha_accion_{simbolo}"
        
        # Verificar cache primero
        try:
            cached_data = cache.get(cache_key)
            if cached_data and cached_data.get("success"):
                print(f"✅ Cache hit para {simbolo}")
                return cached_data
        except Exception as e:
            print(f"⚠️ Error accediendo al cache para {simbolo}: {e}")
        
        # Obtener datos REALES de la API
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": simbolo,
            "apikey": self.API_KEY
        }
        
        url_completa = f"{self.url}?function=GLOBAL_QUOTE&symbol={simbolo}&apikey={self.API_KEY}"
        print(f"🌐 Llamando Alpha Vantage REAL para {simbolo}")
        
        try:
            response = requests.get(self.url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            print(f"📡 Respuesta Alpha Vantage para {simbolo}:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Keys en respuesta: {list(data.keys()) if isinstance(data, dict) else 'No es dict'}")
            
            # Verificar errores de API
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
            
            # Verificar si tenemos Global Quote REAL
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                print(f"✅ Global Quote REAL encontrado para {simbolo}")
                
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
                        "fuente": "alpha_vantage_real"
                    }
                    
                    # Guardar en cache
                    try:
                        cache.set(cache_key, resultado, self.cache_timeout)
                        print(f"💾 Datos REALES de {simbolo} guardados en cache: ${precio:.2f}")
                    except Exception as e:
                        print(f"⚠️ Error guardando en cache para {simbolo}: {e}")
                    
                    return resultado
                    
                except (ValueError, TypeError) as e:
                    error_msg = f"Error procesando datos REALES para {simbolo}: {e}"
                    print(f"❌ {error_msg}")
                    return {
                        "simbolo": simbolo,
                        "error": error_msg,
                        "success": False,
                        "timestamp": int(time.time())
                    }
            
            # Si llegamos aquí, no hay Global Quote válido
            error_msg = f"No se encontraron datos reales válidos para {simbolo}"
            print(f"❌ {error_msg}")
            return {
                "simbolo": simbolo,
                "error": error_msg,
                "success": False,
                "timestamp": int(time.time())
            }
                
        except requests.exceptions.Timeout:
            error_msg = f"Timeout obteniendo datos REALES para {simbolo}"
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
        """Obtiene TODAS las acciones REALES"""
        if simbolos is None:
            simbolos = self.simbolos
        
        simbolos = [s.upper().strip() for s in simbolos[:5]]
        print(f"🎯 Obteniendo acciones REALES de Alpha Vantage: {simbolos}")
        
        resultados = []
        
        # Intentar obtener cada símbolo con pausa entre llamadas
        for i, simbolo in enumerate(simbolos):
            if i > 0:
                print(f"⏳ Esperando 12 segundos antes de llamar API para {simbolo}...")
                time.sleep(12)  # Respetar rate limits
            
            resultado = self.obtener_cotizacion(simbolo)
            resultados.append(resultado)
        
        # Contar exitosas
        exitosas = [r for r in resultados if r.get("success")]
        fallidas = [r for r in resultados if not r.get("success")]
        
        print(f"📊 Alpha Vantage REAL: {len(exitosas)} exitosas, {len(fallidas)} fallidas")
        
        return {
            "acciones": resultados,
            "total": len(resultados),
            "exitosas": len(exitosas),
            "fallidas": len(fallidas),
            "simbolos_solicitados": simbolos,
            "fuente": "alpha_vantage_real"
        }

# Instancia del servicio
acciones_service = AccionesService()