from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            }

    def validate_email(self, value):
        # Normalize the email to lowercase
        email = value.lower()
        
        # Check if a user with this email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return email
    
    def create(self, validated_data):
        # Email is already normalized and validated in validate_email
        user = User.objects.create_user(**validated_data)
        return user
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid login credentials")
            attrs["user"] = user
        else:
            raise serializers.ValidationError("Both email and password are required")
        return attrs
        

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
        }

    def to_representation(self, instance):
        return super().to_representation(instance)