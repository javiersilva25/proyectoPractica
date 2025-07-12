# acciones_yahoo.py - SOLO DATOS REALES DE YAHOO FINANCE
import yfinance as yf
import time
import threading
from typing import List, Dict, Any
from django.core.cache import cache
import logging
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class AccionesYahooService:
    def __init__(self):
        self.simbolos = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        self.cache_timeout = 900  # 15 minutos
        self.update_interval = 900  # 15 minutos
        self.is_updating = False
        self.last_update = None
        self.rate_limited = False
        self.rate_limit_until = None
        
        # Configurar session con headers específicos
        self.session = self._create_session()
        
        print("🟡 Yahoo Finance service inicializado - SOLO DATOS REALES")
        self._start_auto_update()
    
    def _create_session(self):
        """Crea una sesión HTTP configurada para Yahoo Finance"""
        session = requests.Session()
        
        # Headers que imitan un navegador real
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        })
        
        # Configurar reintentos
        retry_strategy = Retry(
            total=5,
            backoff_factor=3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _start_auto_update(self):
        """Inicia el hilo de actualización automática"""
        def update_loop():
            time.sleep(300)  # Esperar 5 minutos antes de iniciar
            
            while True:
                try:
                    if not self.rate_limited:
                        print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Iniciando actualización automática...")
                        self._update_all_cached_data()
                        self.last_update = datetime.now()
                        print(f"✅ Actualización completada a las {self.last_update.strftime('%H:%M:%S')}")
                    else:
                        print(f"⚠️ Rate limited hasta {self.rate_limit_until}, esperando...")
                        
                except Exception as e:
                    print(f"❌ Error en actualización automática: {e}")
                
                time.sleep(self.update_interval)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        print("🚀 Hilo de actualización automática iniciado")
    
    def _check_rate_limit(self):
        """Verifica si estamos en rate limit"""
        if self.rate_limited and self.rate_limit_until:
            if datetime.now() > self.rate_limit_until:
                self.rate_limited = False
                self.rate_limit_until = None
                print("✅ Rate limit expirado, reanudando operaciones")
    
    def _set_rate_limit(self, minutes=60):
        """Establece rate limit por X minutos"""
        self.rate_limited = True
        self.rate_limit_until = datetime.now() + timedelta(minutes=minutes)
        print(f"🚫 Rate limit activado hasta {self.rate_limit_until.strftime('%H:%M:%S')}")
    
    def _update_all_cached_data(self):
        """Actualiza todos los datos en caché"""
        if self.is_updating:
            print("⚠️ Actualización ya en progreso, saltando...")
            return
        
        self._check_rate_limit()
        if self.rate_limited:
            print("⚠️ En rate limit, saltando actualización...")
            return
        
        self.is_updating = True
        try:
            for i, simbolo in enumerate(self.simbolos):
                if i > 0:
                    tiempo_espera = 10  # 10 segundos entre llamadas
                    print(f"⏳ Esperando {tiempo_espera}s antes de obtener {simbolo}...")
                    time.sleep(tiempo_espera)
                
                print(f"🔄 Actualizando {simbolo}...")
                resultado = self._obtener_cotizacion_fresh(simbolo)
                
                if "rate limit" in resultado.get("error", "").lower():
                    self._set_rate_limit(120)  # 2 horas
                    break
                    
        finally:
            self.is_updating = False
    
    def _obtener_cotizacion_fresh(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene cotización fresca SOLO DE YAHOO FINANCE"""
        try:
            print(f"🌐 Obteniendo {simbolo} de Yahoo Finance API...")
            
            self._check_rate_limit()
            if self.rate_limited:
                return {
                    "simbolo": simbolo,
                    "error": "Rate limited - esperando para reanudar",
                    "success": False,
                    "timestamp": int(time.time())
                }
            
            # Método 1: Usar yfinance con session personalizada
            ticker = yf.Ticker(simbolo, session=self.session)
            
            # Intentar obtener datos históricos
            hist = ticker.history(period="2d", interval="1d", timeout=30)
            
            if not hist.empty and len(hist) >= 1:
                resultado = self._procesar_datos_historicos(simbolo, hist)
                if resultado:
                    return resultado
            
            # Método 2: Usar info del ticker
            print(f"🔄 Intentando método alternativo para {simbolo}...")
            info = ticker.info
            
            if info and ('regularMarketPrice' in info or 'currentPrice' in info):
                precio_actual = float(info.get('regularMarketPrice') or info.get('currentPrice', 0))
                if precio_actual > 0:
                    cambio_anterior = float(info.get('regularMarketChange', 0))
                    porcentaje_cambio = float(info.get('regularMarketChangePercent', 0))
                    
                    resultado = {
                        "simbolo": simbolo,
                        "precio": round(precio_actual, 2),
                        "cambio": round(cambio_anterior, 2),
                        "porcentaje_cambio": f"{porcentaje_cambio:.2f}",
                        "success": True,
                        "timestamp": int(time.time()),
                        "volumen": str(info.get('regularMarketVolume', 'N/A')),
                        "ultimo_dia_trading": datetime.now().strftime('%Y-%m-%d'),
                        "fuente": "yahoo_finance_info",
                        "ultima_actualizacion": datetime.now().strftime('%H:%M:%S')
                    }
                    
                    # Actualizar caché
                    cache_key = f"yahoo_accion_{simbolo}"
                    cache.set(cache_key, resultado, self.cache_timeout)
                    print(f"✅ {simbolo} obtenido: ${precio_actual:.2f} ({cambio_anterior:+.2f})")
                    return resultado
            
            # Si no se pudo obtener datos válidos
            print(f"❌ No se pudieron obtener datos reales para {simbolo}")
            return {
                "simbolo": simbolo,
                "error": "No se pudieron obtener datos reales de Yahoo Finance",
                "success": False,
                "timestamp": int(time.time())
            }
            
        except Exception as e:
            error_msg = str(e).lower()
            print(f"❌ Error obteniendo {simbolo}: {e}")
            
            # Detectar rate limiting
            if any(keyword in error_msg for keyword in ["too many requests", "rate limit", "403", "429"]):
                self._set_rate_limit(120)
                return {
                    "simbolo": simbolo,
                    "error": "Rate limited por Yahoo Finance",
                    "success": False,
                    "timestamp": int(time.time())
                }
            
            return {
                "simbolo": simbolo,
                "error": f"Error de conexión: {str(e)}",
                "success": False,
                "timestamp": int(time.time())
            }
    
    def _procesar_datos_historicos(self, simbolo: str, hist) -> Dict[str, Any]:
        """Procesa datos históricos de yfinance"""
        try:
            precio_actual = float(hist['Close'].iloc[-1])
            
            # Calcular cambio si hay datos previos
            if len(hist) >= 2:
                precio_anterior = float(hist['Close'].iloc[-2])
                cambio = precio_actual - precio_anterior
                porcentaje_cambio = (cambio / precio_anterior) * 100
            else:
                cambio = 0
                porcentaje_cambio = 0
            
            volumen = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns and len(hist['Volume']) > 0 else 0
            
            resultado = {
                "simbolo": simbolo,
                "precio": round(precio_actual, 2),
                "cambio": round(cambio, 2),
                "porcentaje_cambio": f"{porcentaje_cambio:.2f}",
                "success": True,
                "timestamp": int(time.time()),
                "volumen": f"{volumen:,}" if volumen > 0 else "N/A",
                "ultimo_dia_trading": hist.index[-1].strftime('%Y-%m-%d'),
                "fuente": "yahoo_finance_historical",
                "ultima_actualizacion": datetime.now().strftime('%H:%M:%S')
            }
            
            # Actualizar caché
            cache_key = f"yahoo_accion_{simbolo}"
            cache.set(cache_key, resultado, self.cache_timeout)
            print(f"✅ {simbolo}: ${precio_actual:.2f} ({cambio:+.2f})")
            
            return resultado
            
        except Exception as e:
            print(f"❌ Error procesando datos históricos para {simbolo}: {e}")
            return None
    
    def obtener_cotizacion(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene cotización REAL de Yahoo Finance (con caché)"""
        cache_key = f"yahoo_accion_{simbolo}"
        
        # Verificar caché primero
        try:
            cached_data = cache.get(cache_key)
            if cached_data and cached_data.get("success"):
                timestamp = cached_data.get("timestamp", 0)
                if time.time() - timestamp < self.cache_timeout:
                    age_minutes = int((time.time() - timestamp) / 60)
                    print(f"✅ Cache hit para {simbolo} (edad: {age_minutes} min)")
                    return cached_data
        except Exception as e:
            print(f"⚠️ Error accediendo al caché para {simbolo}: {e}")
        
        # Obtener datos frescos REALES
        return self._obtener_cotizacion_fresh(simbolo)
    
    def obtener_todas_las_acciones(self, simbolos: List[str] = None) -> Dict[str, Any]:
        """Obtiene todas las acciones REALES usando Yahoo Finance"""
        if simbolos is None:
            simbolos = self.simbolos
        
        simbolos = [s.upper().strip() for s in simbolos[:5]]
        print(f"🎯 Obteniendo acciones REALES de Yahoo Finance: {simbolos}")
        
        resultados = []
        exitosas = 0
        
        for i, simbolo in enumerate(simbolos):
            if i > 0:
                time.sleep(2)  # Pausa entre llamadas
                
            resultado = self.obtener_cotizacion(simbolo)
            resultados.append(resultado)
            
            if resultado.get("success"):
                exitosas += 1
        
        print(f"📊 Yahoo Finance REAL: {exitosas}/{len(simbolos)} exitosas")
        
        proxima_actualizacion = "N/A"
        if self.last_update:
            proxima = self.last_update + timedelta(minutes=15)
            proxima_actualizacion = proxima.strftime('%H:%M:%S')
        
        return {
            "acciones": resultados,
            "total": len(resultados),
            "exitosas": exitosas,
            "simbolos_solicitados": simbolos,
            "fuente": "yahoo_finance_real",
            "ultima_actualizacion_automatica": self.last_update.strftime('%H:%M:%S') if self.last_update else "Pendiente",
            "proxima_actualizacion": proxima_actualizacion,
            "rate_limited": self.rate_limited
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servicio"""
        return {
            "servicio": "Yahoo Finance REAL",
            "auto_actualizacion": True,
            "intervalo_minutos": 15,
            "ultima_actualizacion": self.last_update.strftime('%Y-%m-%d %H:%M:%S') if self.last_update else "Nunca",
            "actualizando_ahora": self.is_updating,
            "simbolos_monitoreados": self.simbolos,
            "rate_limited": self.rate_limited,
            "rate_limit_hasta": self.rate_limit_until.strftime('%H:%M:%S') if self.rate_limit_until else None
        }

# Instancia del servicio
acciones_yahoo_service = AccionesYahooService()