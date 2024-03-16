from django.urls import path
from .views import LoginView, get_csrf_token, check_authentication, LogoutView


urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('csrftoken', get_csrf_token),
    path('authenticate', check_authentication)
]