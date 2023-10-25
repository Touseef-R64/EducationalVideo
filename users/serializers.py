from rest_framework import serializers
from .models import User  # Import your User model

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)  # Hide password in response

    def create(self, validated_data):
        # Create and return a new user instance using the validated data
        return User.objects.create_user(**validated_data)


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'payment_picture')  # Include the fields you want to serialize
