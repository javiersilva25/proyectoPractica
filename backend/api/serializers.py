from rest_framework import serializers
from .models import Noticia, DocumentoCliente, DocumentoLeido
from django.contrib.auth.models import User
from .models import MensajeCliente

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = '__all__'

class RegistroClienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class DocumentoClienteSerializer(serializers.ModelSerializer):
    revisado = serializers.SerializerMethodField()

    class Meta:
        model = DocumentoCliente
        fields = '__all__'  # o explícitamente: ['id', 'titulo', 'mensaje', 'archivo', 'fecha_subida', 'revisado']
        read_only_fields = ['cliente', 'fecha_subida']

    def get_revisado(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return DocumentoLeido.objects.filter(documento=obj, cliente=request.user).exists()
    
class MensajeClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeCliente
        fields = '__all__'
        read_only_fields = ['cliente', 'fecha']

