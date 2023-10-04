from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('signup/', views.signup_user, name='signup_user'),
    path('history/', views.history, name='history'),
    path('delete_history/<record_id>', views.delete_history, name='delete_history'),
]
