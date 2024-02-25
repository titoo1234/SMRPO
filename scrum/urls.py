from scrum import views
# from django.conf.urls import url
from django.urls import path,re_path

urlpatterns = [
    path('user/', views.userApi,name='test'),
    # re_path(r'^login/$', views.userApi, name='user_login')
    # re_path(r'user/[0-9]+$', views.userApi,name='test1'),
    # path('user/', views.userApi),
]