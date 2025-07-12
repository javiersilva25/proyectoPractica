# views.py - SOLO APIS REALES, SIN DATOS SIMULADOS
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Importar servicios disponibles
try:
    from .acciones_yahoo import acciones_yahoo_service
    USE_YAHOO = True
    print("✅ Yahoo Finance service cargado (SOLO DATOS REALES)")
except ImportError as e:
    USE_YAHOO = False
    print(f"❌ Yahoo Finance service no disponible: {e}")

try:
    from .acciones import acciones_service
    USE_ALPHA_VANTAGE = True
    print("✅ Alpha Vantage service cargado (SOLO DATOS REALES)")
except ImportError as e:
    USE_ALPHA_VANTAGE = False
    print(f"❌ Alpha Vantage service no disponible: {e}")

@csrf_exempt
@require_http_methods(["GET"])
def obtener_acciones(request):
    """
    Endpoint para obtener datos de acciones - SOLO APIs REALES
    """
    try:
        simbolos_param = request.GET.get('simbolos', None)
        if simbolos_param:
            simbolos = [s.strip().upper() for s in simbolos_param.split(',')[:5]]
        else:
            simbolos = None
        
        resultado = None
        fuente_usada = None
        error_messages = []
        
        # Intentar Yahoo Finance primero
        if USE_YAHOO:
            print("🟡 Intentando Yahoo Finance (DATOS REALES)...")
            try:
                resultado = acciones_yahoo_service.obtener_todas_las_acciones(simbolos)
                # Verificar si al menos una acción fue exitosa
                if resultado.get("exitosas", 0) > 0:
                    fuente_usada = "yahoo_finance_real"
                    print(f"✅ Yahoo Finance exitoso: {resultado.get('exitosas')} acciones REALES")
                else:
                    print("⚠️ Yahoo Finance no devolvió datos válidos")
                    error_messages.append("Yahoo Finance: No se pudieron obtener datos válidos")
                    resultado = None
            except Exception as e:
                print(f"❌ Error con Yahoo Finance: {e}")
                error_messages.append(f"Yahoo Finance: {str(e)}")
                resultado = None
        
        # Fallback a Alpha Vantage si Yahoo Finance falla
        if not resultado and USE_ALPHA_VANTAGE:
            print("🔵 Intentando Alpha Vantage (DATOS REALES)...")
            try:
                resultado = acciones_service.obtener_todas_las_acciones(simbolos)
                if resultado.get("exitosas", 0) > 0:
                    fuente_usada = "alpha_vantage_real"
                    print(f"✅ Alpha Vantage exitoso: {resultado.get('exitosas')} acciones REALES")
                else:
                    error_messages.append("Alpha Vantage: No se pudieron obtener datos válidos")
                    resultado = None
            except Exception as e:
                print(f"❌ Error con Alpha Vantage: {e}")
                error_messages.append(f"Alpha Vantage: {str(e)}")
                resultado = None
        
        # Si no hay APIs disponibles o todas fallaron
        if not resultado:
            return JsonResponse({
                "status": "error",
                "error": "No se pudieron obtener datos reales de ninguna API",
                "errores_detallados": error_messages,
                "timestamp": int(time.time()),
                "mensaje": "Todas las APIs están temporalmente no disponibles. Intente más tarde."
            }, status=503)  # Service Unavailable
        
        # Filtrar solo acciones exitosas
        acciones_exitosas = [accion for accion in resultado["acciones"] if accion.get("success")]
        
        if not acciones_exitosas:
            return JsonResponse({
                "status": "error",
                "error": "No se pudieron obtener datos válidos para ninguna acción",
                "acciones_intentadas": resultado.get("simbolos_solicitados", []),
                "timestamp": int(time.time())
            }, status=404)
        
        response_data = {
            "acciones": acciones_exitosas,
            "status": "success",
            "timestamp": int(time.time()),
            "total": len(acciones_exitosas),
            "exitosas": len(acciones_exitosas),
            "fuente": fuente_usada,
            "source": fuente_usada,
            "auto_actualizacion": {
                "habilitada": True,
                "intervalo_minutos": 15,
                "ultima_actualizacion": resultado.get("ultima_actualizacion_automatica", "N/A"),
                "proxima_actualizacion": resultado.get("proxima_actualizacion", "N/A")
            },
            "mensaje": f"Datos reales obtenidos de {fuente_usada.replace('_', ' ').title()}"
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"❌ Error crítico en obtener_acciones: {e}")
        return JsonResponse({
            "status": "error",
            "error": f"Error interno del servidor: {str(e)}",
            "timestamp": int(time.time())
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def obtener_accion_individual(request, simbolo):
    """
    Endpoint para obtener una acción individual - SOLO DATOS REALES
    """
    try:
        print(f"🎯 Obteniendo acción individual REAL: {simbolo}")
        
        resultado = None
        
        # Intentar Yahoo Finance primero
        if USE_YAHOO:
            try:
                resultado = acciones_yahoo_service.obtener_cotizacion(simbolo.upper())
                if resultado.get("success"):
                    print(f"✅ Yahoo Finance exitoso para {simbolo}")
                else:
                    resultado = None
            except Exception as e:
                print(f"❌ Error con Yahoo Finance para {simbolo}: {e}")
        
        # Fallback a Alpha Vantage
        if not resultado and USE_ALPHA_VANTAGE:
            try:
                resultado = acciones_service.obtener_cotizacion(simbolo.upper())
                if not resultado.get("success"):
                    resultado = None
            except Exception as e:
                print(f"❌ Error con Alpha Vantage para {simbolo}: {e}")
        
        if resultado and resultado.get("success"):
            return JsonResponse({
                "accion": resultado,
                "status": "success",
                "timestamp": int(time.time()),
                "source": resultado.get("fuente", "api_real")
            })
        else:
            return JsonResponse({
                "error": f"No se pudieron obtener datos reales para {simbolo}",
                "status": "error",
                "simbolo": simbolo,
                "timestamp": int(time.time()),
                "mensaje": "APIs temporalmente no disponibles"
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
                "servicio": "APIs no disponibles",
                "auto_actualizacion": False,
                "mensaje": "Ninguna API de acciones está disponible"
            }
        
        return JsonResponse({
            "status": "success",
            "service_status": status,
            "apis_disponibles": {
                "yahoo_finance": USE_YAHOO,
                "alpha_vantage": USE_ALPHA_VANTAGE
            },
            "timestamp": int(time.time())
        })
        
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "status": "error",
            "timestamp": int(time.time())
        }, status=500)

# ... resto de funciones (noticias e indicadores) sin cambios ...