from django.urls import path
from api.views import CustomUserCreateView, CustomUserRetrieveUpdateView

urlpatterns = [
    path('users/', CustomUserCreateView.as_view(), name='create_user'),
    path('users/<int:id>/', CustomUserRetrieveUpdateView.as_view(), name='retrieve_update_user'),
]

