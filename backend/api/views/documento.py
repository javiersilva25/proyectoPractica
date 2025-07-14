from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import DocumentoCliente, DocumentoLeido
from ..serializers import DocumentoClienteSerializer

class DocumentoClienteViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentoClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DocumentoCliente.objects.filter(cliente=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.rol == 'gerente':
            serializer.save()  # El gerente debe incluir 'cliente' en el body
        else:
            serializer.save(cliente=self.request.user)


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def marcar_revisado(self, request, pk=None):
        documento = self.get_object()

        # Asegura que el cliente solo pueda marcar sus propios documentos
        if documento.cliente != request.user:
            return Response({'detalle': 'No autorizado.'}, status=status.HTTP_403_FORBIDDEN)

        DocumentoLeido.objects.get_or_create(documento=documento, cliente=request.user)
        return Response({'mensaje': 'Documento marcado como revisado'}, status=status.HTTP_200_OK)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context