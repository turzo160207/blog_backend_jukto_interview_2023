from rest_framework import generics, status
from rest_framework.response import Response
from api.models import CustomUser
from api.serializers import CustomUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from api.models import Post
from rest_framework import serializers
from api.serializers import PostSerializer
from api.permissions import IsOwnerOrReadOnly
from api.models import Comment
from api.serializers import CommentSerializer
from .permissions import IsModerator
from .permissions import IsAdminOrModerator


class CustomUserCreateView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        elif self.request.method == 'GET':
            # return  [IsAdminOrModerator()]
            return  [IsAdminUser()]
        return [IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        print(request.data)
        # serializer_class = CustomUserSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token_obj , _ = Token.objects.get_or_create(user=user)
        return Response({'status' : 200, 'payload' : serializer.data, 'token' : str(token_obj)})
    
    def get(self,request):
        queryset = CustomUser.objects.all()
        serializer = self.get_serializer(queryset,many=True)
        return Response({'status' : 200, 'payload' : serializer.data})

    
class CustomUserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,
                          IsOwnerOrReadOnly]
