from scrum import views
# from django.conf.urls import url
from django.urls import path,re_path
from .views import user_login,user_register
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('user/', views.userApi,name='test'),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # re_path(r'^login/$', views.userApi, name='user_login')
    # re_path(r'user/[0-9]+$', views.userApi,name='test1'),
    # path('user/', views.userApi),
]