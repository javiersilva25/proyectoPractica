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

try:
    from .indices_globales import indices_globales_service
    USE_INDICES_GLOBALES = True
    logger.info("✅ Índices Globales service cargado")
except ImportError as e:
    USE_INDICES_GLOBALES = False
    logger.error(f"❌ Índices Globales service no disponible: {e}")

def mapear_simbolo_a_yahoo(simbolo_amigable: str) -> str:
    """Mapea símbolos amigables para URL a símbolos de Yahoo Finance"""
    mapeo = {
        'sp500': '^GSPC',
        'dowjones': '^DJI', 
        'nasdaq': '^IXIC',
        'ftse': '^FTSE',
        'dax': '^GDAXI',
        'bovespa': '^BVSP',
        'ibex35': '^IBEX',
        'nikkei': '^N225',
        # También permitir símbolos directos sin ^
        'gspc': '^GSPC',
        'dji': '^DJI',
        'ixic': '^IXIC',
        'gdaxi': '^GDAXI',
        'bvsp': '^BVSP',
        'ibex': '^IBEX',
        'n225': '^N225'
    }
    simbolo_procesado = mapeo.get(simbolo_amigable.lower(), simbolo_amigable.upper())
    print(f"🔍 Mapeo: '{simbolo_amigable}' -> '{simbolo_procesado}'")
    return simbolo_procesado

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
def obtener_indices_globales(request):
    """Obtener datos de índices globales"""
    try:
        print("🌍 REQUEST: obtener_indices_globales")
        
        if not USE_INDICES_GLOBALES:
            print("❌ Servicio de índices no disponible")
            return Response({
                "status": "error",
                "error": "Servicio de índices no disponible",
                "timestamp": int(time.time())
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        print("🔄 Obteniendo todos los índices...")
        resultado = indices_globales_service.obtener_todos_los_indices()
        print(f"📊 Resultado obtenido: {resultado.get('exitosos', 0)} exitosos de {resultado.get('total', 0)}")
        
        if not resultado or resultado.get("exitosos", 0) == 0:
            return Response({
                "status": "error",
                "error": "No se pudieron obtener datos de índices",
                "timestamp": int(time.time())
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Filtrar solo exitosos
        indices_exitosos = [indice for indice in resultado["indices"] if indice.get("success")]
        
        if not indices_exitosos:
            return Response({
                "status": "error",
                "error": "No hay datos válidos de índices disponibles",
                "timestamp": int(time.time())
            }, status=status.HTTP_404_NOT_FOUND)
        
        print(f"✅ Enviando {len(indices_exitosos)} índices exitosos")
        
        return Response({
            "indices": indices_exitosos,
            "status": "success",
            "timestamp": int(time.time()),
            "total": len(indices_exitosos),
            "exitosos": len(indices_exitosos),
            "fuente": "yahoo_finance",
            "auto_actualizacion": {
                "habilitada": True,
                "intervalo_minutos": 15,
                "ultima_actualizacion": resultado.get("ultima_actualizacion_automatica", "N/A"),
                "proxima_actualizacion": resultado.get("proxima_actualizacion", "N/A")
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"❌ Error crítico en índices: {e}")
        print(f"❌ Error crítico en índices: {e}")
        return Response({
            "status": "error",
            "error": f"Error interno: {str(e)}",
            "timestamp": int(time.time())
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def obtener_indice_individual(request, simbolo):
    """Obtener un índice individual"""
    try:
        print(f"🌍 REQUEST: obtener_indice_individual para '{simbolo}'")
        
        if not USE_INDICES_GLOBALES:
            return Response({
                "status": "error",
                "error": "Servicio de índices no disponible",
                "timestamp": int(time.time())
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Mapear el símbolo amigable al símbolo de Yahoo Finance
        simbolo_yahoo = mapear_simbolo_a_yahoo(simbolo)
        print(f"🔍 Símbolo mapeado: '{simbolo}' -> '{simbolo_yahoo}'")
        
        resultado = indices_globales_service.obtener_indice(simbolo_yahoo)
        
        if resultado and resultado.get("success"):
            return Response({
                "indice": resultado,
                "status": "success",
                "timestamp": int(time.time())
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": f"No se pudieron obtener datos para {simbolo} ({simbolo_yahoo})",
                "status": "error",
                "simbolo": simbolo,
                "simbolo_yahoo": simbolo_yahoo,
                "timestamp": int(time.time())
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"❌ Error obteniendo índice {simbolo}: {e}")
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
        
        if USE_INDICES_GLOBALES:
            status_info["indices_globales"] = indices_globales_service.get_status()
        
        return Response({
            "status": "success",
            "servicios": status_info,
            "apis_disponibles": {
                "yahoo_finance": USE_YAHOO,
                "alpha_vantage": USE_ALPHA_VANTAGE,
                "indices_globales": USE_INDICES_GLOBALES
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