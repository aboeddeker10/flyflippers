from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process', views.process),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard)
]

