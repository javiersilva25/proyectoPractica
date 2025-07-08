"""
# views.py
import time
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .acciones import acciones_service

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def obtener_acciones(request):
    
    #Endpoint para obtener datos de acciones desde la API
    
    try:
        simbolos_param = request.GET.get('simbolos', None)
        if simbolos_param:
            simbolos = [s.strip().upper() for s in simbolos_param.split(',')[:5]]
        else:
            simbolos = None
        
        logger.info(f"Solicitando acciones para: {simbolos}")
        
        resultado = acciones_service.obtener_todas_las_acciones(simbolos)
        
        # Debug de la respuesta
        logger.info(f"Resultado obtenido: {resultado}")
        
        response_data = {
            "acciones": resultado["acciones"],
            "status": "success",
            "timestamp": int(time.time()),
            "total": resultado["total"],
            "cached": resultado.get("cached", 0),
            "fresh": resultado.get("fresh", 0),
            "source": "api",
            "simbolos_solicitados": resultado.get("simbolos_solicitados", [])
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error en obtener_acciones: {e}")
        return JsonResponse({
            "error": f"Error obteniendo datos de la API: {str(e)}",
            "status": "error",
            "timestamp": int(time.time())
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def obtener_accion_individual(request, simbolo):
    
    #Endpoint para obtener una acción individual
    
    try:
        resultado = acciones_service.obtener_cotizacion(simbolo.upper())
        
        if resultado.get("success"):
            return JsonResponse({
                "accion": resultado,
                "status": "success",
                "timestamp": int(time.time()),
                "source": "api"
            })
        else:
            return JsonResponse({
                "error": resultado.get("error", "Error desconocido"),
                "status": "error",
                "simbolo": simbolo,
                "timestamp": int(time.time())
            }, status=404)
            
    except Exception as e:
        return JsonResponse({
            "error": f"Error obteniendo datos para {simbolo}: {str(e)}",
            "status": "error",
            "timestamp": int(time.time())
        }, status=500)
"""
# views.py - ARCHIVO COMPLETO CON TODAS LAS FUNCIONES
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Importar servicios disponibles
try:
    from .acciones_yahoo import acciones_yahoo_service
    USE_YAHOO = True
    print("✅ Yahoo Finance service cargado")
except ImportError:
    USE_YAHOO = False
    print("❌ Yahoo Finance service no disponible")

try:
    from .acciones import acciones_service
    USE_ALPHA_VANTAGE = True
    print("✅ Alpha Vantage service cargado")
except ImportError:
    USE_ALPHA_VANTAGE = False
    print("❌ Alpha Vantage service no disponible")

@csrf_exempt
@require_http_methods(["GET"])
def obtener_acciones(request):
    """
    Endpoint para obtener datos de acciones - Auto-actualización cada 15 min
    """
    try:
        simbolos_param = request.GET.get('simbolos', None)
        if simbolos_param:
            simbolos = [s.strip().upper() for s in simbolos_param.split(',')[:5]]
        else:
            simbolos = None
        
        # Intentar Yahoo Finance primero
        if USE_YAHOO:
            print("🟡 Usando Yahoo Finance...")
            resultado = acciones_yahoo_service.obtener_todas_las_acciones(simbolos)
        elif USE_ALPHA_VANTAGE:
            print("🔵 Usando Alpha Vantage...")
            resultado = acciones_service.obtener_todas_las_acciones(simbolos)
        else:
            print("🔄 Usando datos simulados...")
            resultado = generar_datos_simulados(simbolos)
        
        response_data = {
            "acciones": resultado["acciones"],
            "status": "success",
            "timestamp": int(time.time()),
            "total": resultado["total"],
            "exitosas": resultado.get("exitosas", resultado["total"]),
            "fuente": resultado.get("fuente", "simulado"),
            "source": "yahoo_finance" if USE_YAHOO else ("alpha_vantage" if USE_ALPHA_VANTAGE else "simulado"),
            "auto_actualizacion": {
                "habilitada": True,
                "intervalo_minutos": 15,
                "ultima_actualizacion": resultado.get("ultima_actualizacion_automatica", "N/A"),
                "proxima_actualizacion": resultado.get("proxima_actualizacion", "N/A")
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"❌ Error en obtener_acciones: {e}")
        return JsonResponse({
            "error": f"Error obteniendo datos: {str(e)}",
            "status": "error",
            "timestamp": int(time.time())
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def obtener_accion_individual(request, simbolo):
    """
    Endpoint para obtener una acción individual
    """
    try:
        print(f"🎯 Obteniendo acción individual: {simbolo}")
        
        if USE_YAHOO:
            print(f"🟡 Usando Yahoo Finance para {simbolo}")
            resultado = acciones_yahoo_service.obtener_cotizacion(simbolo.upper())
        elif USE_ALPHA_VANTAGE:
            print(f"🔵 Usando Alpha Vantage para {simbolo}")
            resultado = acciones_service.obtener_cotizacion(simbolo.upper())
        else:
            print(f"🔄 Usando datos simulados para {simbolo}")
            resultado = generar_datos_simulados([simbolo.upper()])["acciones"][0]
        
        if resultado.get("success"):
            return JsonResponse({
                "accion": resultado,
                "status": "success",
                "timestamp": int(time.time()),
                "source": resultado.get("fuente", "simulado")
            })
        else:
            return JsonResponse({
                "error": resultado.get("error", "Error desconocido"),
                "status": "error",
                "simbolo": simbolo,
                "timestamp": int(time.time())
            }, status=404)
            
    except Exception as e:
        print(f"❌ Error obteniendo {simbolo}: {e}")
        return JsonResponse({
            "error": f"Error obteniendo datos para {simbolo}: {str(e)}",
            "status": "error",
            "timestamp": int(time.time())
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def obtener_status(request):
    """
    Endpoint para obtener el estado del servicio de actualización
    """
    try:
        if USE_YAHOO:
            status = acciones_yahoo_service.get_status()
        else:
            status = {
                "servicio": "Simulado",
                "auto_actualizacion": False,
                "mensaje": "Servicio Yahoo Finance no disponible"
            }
        
        return JsonResponse({
            "status": "success",
            "service_status": status,
            "timestamp": int(time.time())
        })
        
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "status": "error",
            "timestamp": int(time.time())
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def obtener_noticias(request):
    """Endpoint temporal para noticias"""
    try:
        noticias_mock = [
            {
                "id": 1,
                "titulo": "Mercados suben tras datos económicos positivos",
                "contenido": "Los mercados experimentaron ganancias significativas...",
                "fecha": "2025-07-08",
                "categoria": "economica",
                "fuente": "Financial Times"
            },
            {
                "id": 2,
                "titulo": "Tecnológicas lideran el rally del día",
                "contenido": "Las acciones tecnológicas mostraron un fuerte desempeño...",
                "fecha": "2025-07-08",
                "categoria": "tecnologia",
                "fuente": "Reuters"
            }
        ]
        
        categoria = request.GET.get('categoria', None)
        if categoria:
            noticias_filtradas = [n for n in noticias_mock if n['categoria'] == categoria]
        else:
            noticias_filtradas = noticias_mock
        
        return JsonResponse({
            "noticias": noticias_filtradas,
            "status": "success",
            "total": len(noticias_filtradas)
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def obtener_indicadores(request):
    """Endpoint temporal para indicadores"""
    try:
        indicadores_mock = [
            {
                "nombre": "S&P 500",
                "valor": 4580.25,
                "cambio": 15.75,
                "porcentaje_cambio": "0.34%"
            },
            {
                "nombre": "NASDAQ",
                "valor": 14320.45,
                "cambio": -8.22,
                "porcentaje_cambio": "-0.06%"
            },
            {
                "nombre": "DOW JONES",
                "valor": 35450.12,
                "cambio": 125.33,
                "porcentaje_cambio": "0.35%"
            }
        ]
        
        return JsonResponse({
            "indicadores": indicadores_mock,
            "status": "success",
            "total": len(indicadores_mock)
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def generar_datos_simulados(simbolos=None):
    """Genera datos simulados como fallback"""
    import random
    
    if simbolos is None:
        simbolos = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    precios_base = {
        "AAPL": 192.53,
        "GOOGL": 175.82,
        "MSFT": 423.17,
        "TSLA": 259.32,
        "AMZN": 171.43
    }
    
    resultados = []
    for simbolo in simbolos:
        precio_base = precios_base.get(simbolo, random.uniform(50, 500))
        variacion = random.uniform(-0.05, 0.05)  # ±5%
        precio_actual = precio_base * (1 + variacion)
        cambio = precio_actual - precio_base
        porcentaje_cambio = (cambio / precio_base) * 100
        
        resultados.append({
            "simbolo": simbolo,
            "precio": round(precio_actual, 2),
            "cambio": round(cambio, 2),
            "porcentaje_cambio": f"{porcentaje_cambio:.2f}",
            "success": True,
            "timestamp": int(time.time()),
            "volumen": f"{random.randint(1000000, 50000000):,}",
            "ultimo_dia_trading": "2025-07-08",
            "fuente": "simulado"
        })
    
    return {
        "acciones": resultados,
        "total": len(resultados),
        "exitosas": len(resultados),
        "fuente": "simulado"
    }