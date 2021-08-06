from django.urls import path
from authentication import views


urlpatterns = [
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout_user, name="logout"),
]
