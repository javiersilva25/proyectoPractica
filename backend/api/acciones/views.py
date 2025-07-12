import time
import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# Importar servicios
try:
    from .acciones_yahoo import acciones_yahoo_service
    USE_YAHOO = True
    logger.info("✅ Yahoo Finance service cargado")
except ImportError as e:
    USE_YAHOO = False
    logger.error(f"❌ Yahoo Finance service no disponible: {e}")

try:
    from .acciones import acciones_service
    USE_ALPHA_VANTAGE = True
    logger.info("✅ Alpha Vantage service cargado")
except ImportError as e:
    USE_ALPHA_VANTAGE = False
    logger.error(f"❌ Alpha Vantage service no disponible: {e}")

@api_view(['GET'])
def obtener_acciones(request):
    """Obtener datos de acciones"""
    try:
        simbolos_param = request.GET.get('simbolos', None)
        if simbolos_param:
            simbolos = [s.strip().upper() for s in simbolos_param.split(',')[:5]]
        else:
            simbolos = None
        
        resultado = None
        fuente_usada = None
        
        # Intentar Yahoo Finance primero
        if USE_YAHOO:
            try:
                resultado = acciones_yahoo_service.obtener_todas_las_acciones(simbolos)
                if resultado.get("exitosas", 0) > 0:
                    fuente_usada = "yahoo_finance"
                    logger.info(f"✅ Yahoo exitoso: {resultado.get('exitosas')} acciones")
                else:
                    resultado = None
            except Exception as e:
                logger.error(f"❌ Error con Yahoo: {e}")
                resultado = None
        
        # Fallback a Alpha Vantage
        if not resultado and USE_ALPHA_VANTAGE:
            try:
                resultado = acciones_service.obtener_todas_las_acciones(simbolos)
                if resultado.get("exitosas", 0) > 0:
                    fuente_usada = "alpha_vantage"
                    logger.info(f"✅ Alpha Vantage exitoso: {resultado.get('exitosas')} acciones")
                else:
                    resultado = None
            except Exception as e:
                logger.error(f"❌ Error con Alpha Vantage: {e}")
                resultado = None
        
        # Si no hay datos
        if not resultado:
            return Response({
                "status": "error",
                "error": "No se pudieron obtener datos",
                "timestamp": int(time.time())
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Filtrar solo exitosas
        acciones_exitosas = [accion for accion in resultado["acciones"] if accion.get("success")]
        
        if not acciones_exitosas:
            return Response({
                "status": "error",
                "error": "No hay datos válidos disponibles",
                "timestamp": int(time.time())
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "acciones": acciones_exitosas,
            "status": "success",
            "timestamp": int(time.time()),
            "total": len(acciones_exitosas),
            "exitosas": len(acciones_exitosas),
            "fuente": fuente_usada,
            "auto_actualizacion": {
                "habilitada": True,
                "intervalo_minutos": 15,
                "ultima_actualizacion": resultado.get("ultima_actualizacion_automatica", "N/A"),
                "proxima_actualizacion": resultado.get("proxima_actualizacion", "N/A")
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        return Response({
            "status": "error",
            "error": f"Error interno: {str(e)}",
            "timestamp": int(time.time())
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def obtener_accion_individual(request, simbolo):
    """Obtener una acción individual"""
    try:
        resultado = None
        
        # Intentar Yahoo primero
        if USE_YAHOO:
            try:
                resultado = acciones_yahoo_service.obtener_cotizacion(simbolo.upper())
                if not resultado.get("success"):
                    resultado = None
            except Exception as e:
                logger.error(f"❌ Error Yahoo para {simbolo}: {e}")
        
        # Fallback a Alpha Vantage
        if not resultado and USE_ALPHA_VANTAGE:
            try:
                resultado = acciones_service.obtener_cotizacion(simbolo.upper())
                if not resultado.get("success"):
                    resultado = None
            except Exception as e:
                logger.error(f"❌ Error Alpha Vantage para {simbolo}: {e}")
        
        if resultado and resultado.get("success"):
            return Response({
                "accion": resultado,
                "status": "success",
                "timestamp": int(time.time())
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": f"No se pudieron obtener datos para {simbolo}",
                "status": "error",
                "simbolo": simbolo,
                "timestamp": int(time.time())
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"❌ Error obteniendo {simbolo}: {e}")
        return Response({
            "error": f"Error: {str(e)}",
            "status": "error",
            "timestamp": int(time.time())
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def obtener_status(request):
    """Estado de los servicios"""
    try:
        status_info = {}
        
        if USE_YAHOO:
            status_info["yahoo"] = acciones_yahoo_service.get_status()
        
        if USE_ALPHA_VANTAGE:
            status_info["alpha_vantage"] = {
                "servicio": "Alpha Vantage",
                "ultima_consulta": acciones_service.last_update.strftime('%Y-%m-%d %H:%M:%S') if acciones_service.last_update else "Nunca",
                "consultando_ahora": acciones_service.is_updating,
            }
        
        return Response({
            "status": "success",
            "servicios": status_info,
            "apis_disponibles": {
                "yahoo_finance": USE_YAHOO,
                "alpha_vantage": USE_ALPHA_VANTAGE
            },
            "timestamp": int(time.time())
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo status: {e}")
        return Response({
            "error": str(e),
            "status": "error",
            "timestamp": int(time.time())
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)