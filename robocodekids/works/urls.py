from django.urls import path
from . import views

app_name = 'works'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create-contact/', views.create_contact, name='create-contact'),
    path('projects/', views.ProjectList.as_view(), name='project-list'),
    path('projects/create/', views.create_project, name='create-project'),
    path('projects/<str:username>/',
         views.MyProjectList.as_view(), name='my-project-list'),
    path('like/', views.likes_views, name='like-project'),
    path('project/<slug:slug>/', views.project_detail, name='project-detail'),
    path('project-update/<slug:slug>/',
         views.project_update, name='project-update'),
    path('project-delete/<slug:slug>/',
         views.project_delete, name='project-delete'),
    path('help/',
         views.help, name='help'),
]
