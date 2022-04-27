from django.urls import path

from login import views

app_name = 'login'

urlpatterns = [
    path('user/', views.user_login, name="user-login"),
    path('user1/', views.manager_login, name='manager-login'),
    path('signup/', views.user_signup, name="user-signup"),
    path('signup1/', views.manager_signup, name='manager-signup'),
    path('logout/', views.logout, name='logout'),
]
