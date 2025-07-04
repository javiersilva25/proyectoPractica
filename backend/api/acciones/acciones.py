# En tu archivo views.py o similar
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET"])
def obtener_acciones(request):
    try:
        # Usando Alpha Vantage API (gratuita)
        API_KEY = "4EKRBTI9W2VWXLK8"
        simbolos = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        
        resultados = []
        
        for simbolo in simbolos:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": simbolo,
                "apikey": API_KEY
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "Global Quote" in data:
                quote = data["Global Quote"]
                resultados.append({
                    "simbolo": simbolo,
                    "precio": float(quote["05. price"]),
                    "cambio": float(quote["09. change"]),
                    "porcentaje_cambio": quote["10. change percent"].replace("%", "")
                })
        
        return JsonResponse({"acciones": resultados})
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)