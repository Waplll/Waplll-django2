from django.urls import path
from .views import index, create_request, view_requests, delete_request
from .views import BBLoginView
from .views import profile
from .views import BBLogoutView
from .views import ChangeUserInfoView
from .views import BBPasswordChangeView
from .views import RegisterDoneView, RegisterUserView
from .views import DeleteUserView

app_name = 'main'

urlpatterns = [
   path('', index, name='index'),
   path('accounts/login', BBLoginView.as_view(), name='login'),
   path('accounts/profile/', profile, name='profile'),
   path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
   path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
   path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
   path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
   path('accounts/register/', RegisterUserView.as_view(), name='register'),
   path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
   path('create/', create_request, name='create_request'),
   path('requests/', view_requests, name='view_requests'),
   path('delete/<int:request_id>/', delete_request, name='delete_request'),
]