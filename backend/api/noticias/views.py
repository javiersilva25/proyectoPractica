from rest_framework.views import APIView
from rest_framework.response import Response
from .scraper_df import obtener_noticias

class NoticiasView(APIView):
    def get(self, request):
        noticias = obtener_noticias()
        return Response(noticias)
