from rest_framework import serializers
from .models import Noticia, DocumentoCliente, DocumentoLeido, MensajeContacto
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
        read_only_fields = ['fecha_subida']

    def get_revisado(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return DocumentoLeido.objects.filter(documento=obj, cliente=request.user).exists()
    
    def validate_cliente(self, value):
        request = self.context.get('request')
        if request.user.rol != 'gerente' and value != request.user:
            raise serializers.ValidationError("No puedes asignar documentos a otros usuarios.")
        return value
    
class MensajeClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeCliente
        fields = '__all__'
        read_only_fields = ['fecha']

    def validate_cliente(self, value):
        request = self.context.get('request')
        if request.user.rol != 'gerente' and value != request.user:
            raise serializers.ValidationError("No puedes enviar mensajes a otros usuarios.")
        return value


class MensajeContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeContacto
        fields = '__all__'
        read_only_fields = ['leido', 'creado_en']
