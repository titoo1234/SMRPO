from scrum import views
# from django.conf.urls import url
from django.urls import path,re_path
from .views import user_login,user_register
from django.contrib.auth.views import LogoutView
urlpatterns = [
    # path('user/', views.userApi,name='test'),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('allusers/', views.allusers, name='allusers'),
    path('user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('new_project/', views.new_project, name='new_project'),
    path('/project/<str:ime_projekta>/assign_roles/', views.assign_roles, name='assign_roles'),
    path('project/<str:project_name>/', views.project_view, name='project_name'),
    path('project/<str:project_name>/edit/', views.project_edit, name='project_edit'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('deleted_user/<int:user_id>/edit/', views.edit_deleted_user, name='edit_deleted_user'),

    # re_path(r'^login/$', views.userApi, name='user_login')
    # re_path(r'user/[0-9]+$', views.userApi,name='test1'),
    # path('user/', views.userApi),
]