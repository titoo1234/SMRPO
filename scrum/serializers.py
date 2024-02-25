
from .models import User,Project,Sprint

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=(
            'id',
            'name',
            'username',
            'password')
        
