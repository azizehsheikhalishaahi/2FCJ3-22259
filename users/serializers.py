from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')

        # if email and password:
        #     user = authenticate(request=self.context.get('request'), email=email, password=password)

        #     if user is None:
        #         raise serializers.ValidationError(_('Invalid login credentials.'))

        #     if not user.is_active:
        #         raise serializers.ValidationError(_('User account is disabled.'))

        # else:
        #     raise serializers.ValidationError(_('Must include "email" and "password".'))

        # data['user'] = user
        # return data
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid email or password.')

        return {
            'email': email,
            'password': password,
            'user': user
        }

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return token
    
    def save(self, **kwargs):
        request = self.context.get('request')
        if request and request.user and hasattr(request.user, 'auth_token'):
            token = request.user.auth_token
            token.delete() 
        else:
            raise serializers.ValidationError('User not authenticated or no token found.')

class LogoutSerializer(serializers.Serializer):
    pass
