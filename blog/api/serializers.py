from rest_framework import serializers
from api.models import CustomUser
from api.models import Post
from django.shortcuts import get_object_or_404

class CustomUserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_name' ,'first_name', 'last_name', 'password', 'posts']

    def create(self, validated_data):
        user = CustomUser.objects.create(email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user_name')
    email = serializers.ReadOnlyField(source='owner.email')
    # first_name = serializers.ReadOnlyField(source='owner.first_name')

    class Meta:
        model = Post
        fields = ['id', 'email', 'title', 'body', 'owner' ]


