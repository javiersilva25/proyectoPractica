from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import MensajeCliente
from ..serializers import MensajeClienteSerializer

class MensajeClienteViewSet(viewsets.ModelViewSet):
    serializer_class = MensajeClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MensajeCliente.objects.filter(cliente=self.request.user).order_by('-fecha')

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_leido(self, request, pk=None):
        mensaje = self.get_object()
        if mensaje.cliente != request.user:
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        mensaje.leido = True
        mensaje.save()
        return Response({'mensaje': 'Mensaje marcado como leído'}, status=status.HTTP_200_OK)
