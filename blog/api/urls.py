from django.urls import path
from api.views import CustomUserCreateView, CustomUserRetrieveUpdateView
from api import views

urlpatterns = [
    path('userlist/', views.CustomUserList.as_view()),
    path('users/', CustomUserCreateView.as_view(), name='create_user'),
    path('users/<int:id>/', CustomUserRetrieveUpdateView.as_view(), name='retrieve_update_user'),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
]

