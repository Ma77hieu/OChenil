from django.urls import path
from generic import views


urlpatterns = [
    path('', views.homepage, name="home"),
]
