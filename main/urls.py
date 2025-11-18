from django.urls import path
from .views import (
    index, profile, BBLoginView, BBLogoutView,
    ChangeUserInfoView, RegisterUserView,
    CreateRequestView, DeleteRequestView, user_requests,
    change_request_status, manage_categories, create_category,
    edit_category, delete_category
)

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('requests/create/', CreateRequestView.as_view(), name='create_request'),
    path('requests/my/', user_requests, name='user_requests'),
    path('requests/<int:pk>/delete/', DeleteRequestView.as_view(), name='delete_request'),
    path('requests/<int:pk>/change-status/', change_request_status, name='change_request_status'),
    path('categories/', manage_categories, name='manage_categories'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/<int:pk>/edit/', edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', delete_category, name='delete_category'),
]