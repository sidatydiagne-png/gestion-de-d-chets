from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'frontend/login.html'


class DashboardView(TemplateView):
    template_name = 'frontend/dashboard.html'


class CarteView(TemplateView):
    template_name = 'frontend/carte.html'


class SignalementsListView(TemplateView):
    template_name = 'frontend/signalements_list.html'


class SignalementCreateView(TemplateView):
    template_name = 'frontend/signalement_form.html'


class ZonesView(TemplateView):
    template_name = 'frontend/zones.html'


class CollectesView(TemplateView):
    template_name = 'frontend/collectes.html'


class RegisterPageView(TemplateView):
    template_name = 'frontend/register.html'


from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterView(APIView):
    """Inscription publique d'un nouvel utilisateur (citoyen)."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Compte créé avec succès. Vous pouvez maintenant vous connecter.'},
            status=status.HTTP_201_CREATED
        )