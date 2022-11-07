"""
URL mappings for the user API.
"""
from django.urls import path
from user import views


app_name = 'user' # mapped to the 'reverse' in the test_user_api definition

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'), # .as_view() -- define as function, 'create' for reverse lookup
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]