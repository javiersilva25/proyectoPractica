from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_perfil(request):
    usuario = request.user  # ya es instancia de CustomUser autenticado

    return Response({
        "nombre": f"{usuario.username}".strip(),
        "correo": usuario.email,
    })
