from django.urls import path
from generic import views
from administration import views


urlpatterns = [
    # path('', views.homepage, name="home"),
    path('management', views.management, name="management"),
]
