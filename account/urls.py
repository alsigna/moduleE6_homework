from django.urls import path

from .views import SignupView, MyLoginView, MyLogoutView


app_name = "account"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", MyLoginView.as_view(), name="login"),
    # path("logoff/", MyLoginView.as_view(), name="logoff"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
]
