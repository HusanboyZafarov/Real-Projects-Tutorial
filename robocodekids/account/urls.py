from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.AccountLogin.as_view(), name='login'),
    path('logout/', views.AccountLogout.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('student/<str:username>/', views.profile, name='profile'),
]
