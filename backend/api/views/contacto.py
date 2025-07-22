# contacto/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from api.models import MensajeContacto
from api.serializers import MensajeContactoSerializer

class MensajeContactoCreateView(generics.CreateAPIView):
    queryset = MensajeContacto.objects.all()
    serializer_class = MensajeContactoSerializer

    def perform_create(self, serializer):
        mensaje = serializer.save()
        try:
            send_mail(
                subject=f"Nuevo mensaje de contacto de {mensaje.nombre}",
                message=mensaje.mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACTO_ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print("ERROR EN ENVÍO DE CORREO:", e)


class ListaMensajesContacto(generics.ListAPIView):
    queryset = MensajeContacto.objects.order_by('-creado_en')
    serializer_class = MensajeContactoSerializer

class ActualizarMensajeContacto(generics.UpdateAPIView):
    queryset = MensajeContacto.objects.all()
    serializer_class = MensajeContactoSerializer
