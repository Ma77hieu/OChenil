from django.urls import path
from administration import views


urlpatterns = [
    path('management', views.management, name="management"),
]
