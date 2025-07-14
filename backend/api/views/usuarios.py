from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_clientes(request):
    if not request.user.rol == 'gerente':
        return Response({'detalle': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

    clientes = User.objects.filter(rol='cliente').values('id', 'username', 'first_name', 'last_name')
    return Response(list(clientes))
