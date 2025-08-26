from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser
from projects.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "status"]

class CustomUserSerializer(serializers.ModelSerializer):
    assigned_projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name", "role", "gender", "assigned_projects"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError({"error": "Invalid Email or Password. "})
        
        token, created = Token.objects.get_or_create(user=user)

        return {
            "user": CustomUserSerializer(user).data,
            "token": token.key
        }
    
class UserUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=CustomUser.ROLES)
    assigned_projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    