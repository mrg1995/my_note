from django.contrib.auth import get_user_model
from .models import Post
from rest_framework import serializers
User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=11, min_length=2, required=True)
    password = serializers.CharField(max_length=12, min_length=2, required=True,write_only=True)


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username','password')

class PostSerialzier(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('user','post','id')

















