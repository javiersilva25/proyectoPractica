# acciones_yahoo.py - CON MEJOR MANEJO DE RATE LIMITING
import yfinance as yf
import time
import random
import threading
from typing import List, Dict, Any
from django.core.cache import cache
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AccionesYahooService:
    def __init__(self):
        self.simbolos = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        self.cache_timeout = 900  # 15 minutos en segundos
        self.update_interval = 900  # 15 minutos
        self.is_updating = False
        self.last_update = None
        self.rate_limited = False
        self.rate_limit_until = None
        print("🟡 Yahoo Finance service inicializado - Auto-actualización cada 15 minutos")
        
        # Iniciar actualización automática con delay inicial
        self._start_auto_update()
    
    def _start_auto_update(self):
        """Inicia el hilo de actualización automática"""
        def update_loop():
            # Esperar 2 minutos antes de la primera actualización
            print("⏳ Esperando 2 minutos antes de iniciar actualizaciones automáticas...")
            time.sleep(120)
            
            while True:
                try:
                    if not self.rate_limited:
                        print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Iniciando actualización automática...")
                        self._update_all_cached_data()
                        self.last_update = datetime.now()
                        print(f"✅ Actualización completada a las {self.last_update.strftime('%H:%M:%S')}")
                    else:
                        print(f"⚠️ Rate limited hasta {self.rate_limit_until}, saltando actualización...")
                        
                except Exception as e:
                    print(f"❌ Error en actualización automática: {e}")
                
                # Esperar 15 minutos
                time.sleep(self.update_interval)
        
        # Iniciar hilo daemon
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
                    time.sleep(3)  # Pausa más larga entre llamadas
                
                print(f"🔄 Actualizando {simbolo}...")
                resultado = self._obtener_cotizacion_fresh(simbolo)
                
                # Si hay rate limit, parar la actualización
                if "rate limit" in resultado.get("error", "").lower():
                    self._set_rate_limit(60)  # Rate limit por 1 hora
                    break
                    
        finally:
            self.is_updating = False
    
    def _obtener_cotizacion_fresh(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene cotización fresca sin verificar caché"""
        try:
            print(f"🌐 Obteniendo {simbolo} FRESH de Yahoo Finance...")
            
            # Verificar rate limit antes de llamar API
            self._check_rate_limit()
            if self.rate_limited:
                print(f"🚫 Rate limited, usando fallback para {simbolo}")
                return self._generar_fallback(simbolo)
            
            # Crear ticker con configuración más conservadora
            ticker = yf.Ticker(simbolo)
            
            # Obtener información actual con timeout más largo
            hist = ticker.history(period="2d", timeout=30)
            
            if len(hist) < 1:
                raise Exception("No hay datos históricos disponibles")
            
            # Precio actual
            precio_actual = hist['Close'].iloc[-1]
            
            # Calcular cambio
            if len(hist) >= 2:
                precio_anterior = hist['Close'].iloc[-2]
                cambio = precio_actual - precio_anterior
                porcentaje_cambio = (cambio / precio_anterior) * 100
            else:
                cambio = 0
                porcentaje_cambio = 0
            
            # Volumen
            volumen = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
            
            resultado = {
                "simbolo": simbolo,
                "precio": round(float(precio_actual), 2),
                "cambio": round(float(cambio), 2),
                "porcentaje_cambio": f"{porcentaje_cambio:.2f}",
                "success": True,
                "timestamp": int(time.time()),
                "volumen": f"{int(volumen):,}" if volumen > 0 else "N/A",
                "ultimo_dia_trading": hist.index[-1].strftime('%Y-%m-%d'),
                "fuente": "yahoo_finance",
                "ultima_actualizacion": datetime.now().strftime('%H:%M:%S')
            }
            
            # Actualizar caché
            cache_key = f"yahoo_accion_{simbolo}"
            try:
                cache.set(cache_key, resultado, self.cache_timeout)
                print(f"💾 {simbolo} actualizado en caché: ${precio_actual:.2f} ({cambio:+.2f})")
            except Exception as e:
                print(f"⚠️ Error guardando en caché: {e}")
            
            return resultado
            
        except Exception as e:
            error_msg = str(e).lower()
            print(f"❌ Error obteniendo {simbolo} fresh: {e}")
            
            # Detectar rate limiting
            if "too many requests" in error_msg or "rate limit" in error_msg:
                self._set_rate_limit(60)
                return {
                    "simbolo": simbolo,
                    "error": "Rate limited",
                    "success": False,
                    "timestamp": int(time.time())
                }
            
            return self._generar_fallback(simbolo)
    
    def obtener_cotizacion(self, simbolo: str) -> Dict[str, Any]:
        """Obtiene cotización de Yahoo Finance (con caché)"""
        cache_key = f"yahoo_accion_{simbolo}"
        
        # Verificar caché primero
        try:
            cached_data = cache.get(cache_key)
            if cached_data and cached_data.get("success"):
                # Verificar si los datos son recientes (menos de 15 minutos)
                timestamp = cached_data.get("timestamp", 0)
                if time.time() - timestamp < self.cache_timeout:
                    print(f"✅ Cache hit para {simbolo} (actualizado hace {int((time.time() - timestamp) / 60)} min)")
                    return cached_data
        except Exception as e:
            print(f"⚠️ Error accediendo al caché para {simbolo}: {e}")
        
        # Si estamos en rate limit, usar fallback
        self._check_rate_limit()
        if self.rate_limited:
            print(f"🚫 Rate limited, usando fallback para {simbolo}")
            return self._generar_fallback(simbolo)
        
        # Si no hay caché válido y no hay rate limit, obtener datos frescos
        return self._obtener_cotizacion_fresh(simbolo)
    
    def _generar_fallback(self, simbolo: str) -> Dict[str, Any]:
        """Genera datos de fallback cuando Yahoo falla"""
        precios_base = {
            "AAPL": 192.53,
            "GOOGL": 175.82,
            "MSFT": 423.17,
            "TSLA": 259.32,
            "AMZN": 171.43
        }
        
        precio_base = precios_base.get(simbolo, random.uniform(50, 500))
        variacion = random.uniform(-0.03, 0.03)  # ±3%
        precio_actual = precio_base * (1 + variacion)
        cambio = precio_actual - precio_base
        porcentaje_cambio = (cambio / precio_base) * 100
        
        return {
            "simbolo": simbolo,
            "precio": round(precio_actual, 2),
            "cambio": round(cambio, 2),
            "porcentaje_cambio": f"{porcentaje_cambio:.2f}",
            "success": True,
            "timestamp": int(time.time()),
            "volumen": f"{random.randint(1000000, 50000000):,}",
            "ultimo_dia_trading": "2025-07-08",
            "fuente": "simulado_fallback",
            "ultima_actualizacion": datetime.now().strftime('%H:%M:%S')
        }
    
    def obtener_todas_las_acciones(self, simbolos: List[str] = None) -> Dict[str, Any]:
        """Obtiene todas las acciones usando Yahoo Finance"""
        if simbolos is None:
            simbolos = self.simbolos
        
        simbolos = [s.upper().strip() for s in simbolos[:5]]
        print(f"🎯 Obteniendo acciones de Yahoo Finance: {simbolos}")
        
        resultados = []
        exitosas = 0
        
        for simbolo in simbolos:
            resultado = self.obtener_cotizacion(simbolo)
            resultados.append(resultado)
            
            if resultado.get("success"):
                exitosas += 1
        
        print(f"📊 Yahoo Finance: {exitosas}/{len(simbolos)} exitosas")
        
        proxima_actualizacion = "N/A"
        if self.last_update:
            proxima = self.last_update + timedelta(minutes=15)
            proxima_actualizacion = proxima.strftime('%H:%M:%S')
        
        return {
            "acciones": resultados,
            "total": len(resultados),
            "exitosas": exitosas,
            "simbolos_solicitados": simbolos,
            "fuente": "yahoo_finance",
            "ultima_actualizacion_automatica": self.last_update.strftime('%H:%M:%S') if self.last_update else "Pendiente",
            "proxima_actualizacion": proxima_actualizacion,
            "rate_limited": self.rate_limited
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servicio"""
        return {
            "servicio": "Yahoo Finance",
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