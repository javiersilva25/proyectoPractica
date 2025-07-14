from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now

from ..models import DocumentoCliente, MensajeCliente
from usuarios.models import CustomUser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def indicadores_gerente(request):
    usuario = request.user

    # Verifica que sea gerente o superusuario
    if not (usuario.rol == 'gerente' or usuario.is_superuser):
        return Response({'detalle': 'No autorizado'}, status=403)

    hoy = now().date()

    # Total de documentos subidos hoy
    documentos_hoy = DocumentoCliente.objects.filter(fecha_subida__date=hoy).count()

    # Total de clientes con al menos un mensaje no leído
    clientes_con_mensajes_no_leidos = MensajeCliente.objects.filter(leido=False).values('cliente').distinct().count()

    # Total de clientes con al menos un documento cargado
    clientes_con_documentos = DocumentoCliente.objects.values('cliente').distinct().count()

    return Response({
        'documentos_hoy': documentos_hoy,
        'clientes_con_mensajes_no_leidos': clientes_con_mensajes_no_leidos,
        'clientes_con_documentos': clientes_con_documentos,
    })
