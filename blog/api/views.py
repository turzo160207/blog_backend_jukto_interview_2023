from rest_framework import generics, status, views
from rest_framework.response import Response
from api.models import CustomUser, Post, Comment
from api.serializers import CustomUserSerializer, PostSerializer, CommentSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .permissions import IsModeratorOrOwner, IsAdminOrOwner
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import OrderingFilter


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

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title','body', 'customuser__user_name')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'GET':
            return  [AllowAny()]
        return [IsAuthenticated()]

    def get(self,request):
        queryset = Post.objects.all()
        serializer = self.get_serializer(queryset,many=True)
        return Response({'status' : 200, 'payload' : serializer.data})

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response({'status' : 200, 'payload' : serializer.data})

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsModeratorOrOwner()]
        elif self.request.method == 'GET':
            return  [AllowAny()]
        elif self.request.method == 'DELETE':
            return  [IsAdminOrOwner()]
        return [IsAuthenticated()]
    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status' : 200, 'payload' : serializer.data})
    
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post)
        post.views += 1
        post.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'GET':
            return  [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdminOrOwner()]
        elif self.request.method == 'GET':
            return  [AllowAny()]
        elif self.request.method == 'DELETE':
            return  [IsAdminOrOwner()]
        return [IsAuthenticated()]
    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status' : 200, 'payload' : serializer.data})
    
    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})
    
class TrendingPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.order_by('-views')[:5]
    
class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query is not None:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        return queryset