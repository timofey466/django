from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from permission_app.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""
        Advertisement.objects.create(
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            status=validated_data.get('status'),
            created_at=validated_data.get('created_at'),
            updated_at=validated_data.get('updated_at'),
        )
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if Advertisement.status == 'OPEN' in Advertisement.creator >= 10:
            raise ValidationError('у вас слишком много открытых обьявлений')
        return data
