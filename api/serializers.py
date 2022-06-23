from rest_framework import serializers
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'password', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True}
        }
