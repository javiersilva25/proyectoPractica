from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_perfil(request):
    usuario = request.user

    return Response({
        "nombre": usuario.get_full_name() or usuario.username,
        "correo": usuario.email,
        "rol": getattr(usuario, 'rol', None),         
        "is_superuser": usuario.is_superuser,         
    })
