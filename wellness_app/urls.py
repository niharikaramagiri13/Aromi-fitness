from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/',views.register,name='register'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('plan/', views.plan, name='plan'),
    path('profile/',views.profile,name='profile'),
    path('log/',views.log_activity,name='log_activity'),
    path('progress/',views.progress,name='progress'),
    path('history/',views.history,name='history'),
    path('logout/', views.logout_view, name='logout'),
]