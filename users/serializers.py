from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Request

class RequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    subject = UserSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'sender', 'subject', 'accept')