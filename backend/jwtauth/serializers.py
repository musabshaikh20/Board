
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")
    account_type = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "account_type"
        ]
        extra_kwargs = {"password": {"write_only": True},"account_type": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        account_type = validated_data["account_type"]
        if account_type  not in ["premium","free"]:
            raise serializers.ValidationError(
                {"account_type": "Account Type must be premium or free"})

        if (username and User.objects.filter(username=username).exists()):
            raise serializers.ValidationError(
                {"username": "Username Taken"})
        
        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError(
                {"email": "Email address is already registered"})
        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        if user and account_type:
            UserProfile.objects.create( user=user,user_type=account_type)
        return user
