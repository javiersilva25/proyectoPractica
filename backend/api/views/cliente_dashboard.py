# api/views/cliente_dashboard.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ClienteDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        return Response({
            "mensaje": f"Hola {usuario.first_name}, accediste al dashboard privado.",
            "username": usuario.username,
            "email": usuario.email,
            "id": usuario.id
        })
