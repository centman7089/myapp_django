from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, TestAuthenticationView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("verify-email/", VerifyUserEmail.as_view(), name="verify-email"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("test-auth/", TestAuthenticationView.as_view(), name="test-auth"),
]



# from django.urls import path
# from . import views


# urlpatterns = [
#     path('register/', views.RegisterUserView.as_view(), name='register'),
#     path('verify/', views.VerifyUserEmail.as_view(), name='register'),
#     path('login/', views.LoginUserView.as_view(), name='login'),
#     path('profile/', views.TestAuthenticationView.as_view(), name='granted')
# ]