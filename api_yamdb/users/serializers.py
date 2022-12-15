from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Класс для преобразования данных пользователя."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для получения кода авторизации на почту."""
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете зарегистрироваться под именем me')
        return value
