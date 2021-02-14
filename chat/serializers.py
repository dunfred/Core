from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'last_login'
        ]

        extra_kwargs = {
            'username' : {'read_only':True},
            'last_login' : {'read_only':True},
        }




