# backend/acciones/views.py
import random
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET"])
def obtener_acciones(request):
    """
    Endpoint para obtener datos de acciones
    """
    try:
        # Datos simulados realistas
        simbolos = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        resultados = []
        
        precios_base = {
            "AAPL": 175.43,
            "GOOGL": 2845.67,
            "MSFT": 412.89,
            "TSLA": 248.50,
            "AMZN": 3456.78
        }
        
        for simbolo in simbolos:
            precio = precios_base.get(simbolo, 100) + random.uniform(-15, 15)
            cambio = random.uniform(-10, 10)
            porcentaje = (cambio / precio) * 100
            
            resultados.append({
                "simbolo": simbolo,
                "precio": round(precio, 2),
                "cambio": round(cambio, 2),
                "porcentaje_cambio": f"{porcentaje:.2f}"
            })
        
        return JsonResponse({
            "acciones": resultados,
            "status": "success",
            "timestamp": int(time.time()),
            "total": len(resultados)
        })
        
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "status": "error"
        }, status=500)