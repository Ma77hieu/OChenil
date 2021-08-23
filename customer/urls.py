from django.urls import path
from customer import views


urlpatterns = [
    path('user', views.user, name="user"),
    path('booking', views.book_dates, name="booking"),
    path('signin/<int:id_user>', views.user, name="useraftersignin"),
]
