from django.urls import path, include
from .views import LogoutView, LoginView, UserView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
]
