from django.urls import path
from customer import views


urlpatterns = [
    path('user', views.user, name="user"),
    path('signin/<int:id_user>', views.user, name="useraftersignin"),
]
