from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class RegistroClienteView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "Todos los campos son obligatorios."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya existe."}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return Response({"mensaje": "Usuario registrado con éxito"}, status=status.HTTP_201_CREATED)
