from django.urls import path
from convosight.accounts.views import (
    CreateUserAPIView, AuthenticateUserAPIView
)


app_name = 'accounts'

urlpatterns = [
    path('create/', CreateUserAPIView.as_view(), name="create_account"),
    path('login/', AuthenticateUserAPIView.as_view(), name="login"),
]
