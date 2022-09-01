from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render


class SignupView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("account:login")
    template_name = "account/signup.html"


class MyLoginView(LoginView):
    template_name = "account/login.html"

    def get_success_url(self):
        return reverse("chat:main")


class MyLogoutView(LogoutView):
    template_name = "account/logout.html"

    def get_success_url(self):
        return reverse("chat:main")

    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name="account/logout.html",
            status=200,
        )

    # def post(self, request, *args, **kwargs):
    #     """Logout may be done via POST."""
    #     auth_logout(request)
    #     redirect_to = self.get_success_url()
    #     if redirect_to != request.get_full_path():
    #         # Redirect to target page once the session has been cleared.
    #         return HttpResponseRedirect(redirect_to)
    #     return super().get(request, *args, **kwargs)
