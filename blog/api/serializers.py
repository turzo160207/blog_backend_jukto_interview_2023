from rest_framework import serializers
from api.models import CustomUser, Post, Comment

class CustomUserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_name' ,'first_name', 'last_name', 'password', 'posts', 'comments']

    def create(self, validated_data):
        user = CustomUser.objects.create(email = validated_data['email'], 
                                         user_name = validated_data['user_name'],
                                         first_name = validated_data['first_name'],
                                         last_name = validated_data['last_name'],
                                         )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user_name')
    email = serializers.ReadOnlyField(source='owner.email')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'email', 'title', 'body', 'owner', 'comments', 'views' ]

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user_name')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post']

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

