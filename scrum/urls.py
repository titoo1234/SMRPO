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
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('deleted_user/<int:user_id>/edit/', views.edit_deleted_user, name='edit_deleted_user'),
    # project ============================================================
    path('new_project/', views.new_project, name='new_project'),
    path('project/<str:ime_projekta>/add_members/', views.add_members, name='add_members'),
    path('delete_project/<str:project_name>/', views.delete_project, name='delete_project'),
    path('project/<str:ime_projekta>/assign_roles/', views.assign_roles, name='assign_roles'),
    path('project/<str:project_name>/', views.project_view, name='project_name'),
    path('project/<str:project_name>/edit/', views.project_edit, name='project_edit'),
    path('project/<str:project>/add_member/<str:user_id>/', views.add_member_to_project, name='add_member_to_project'),
    path('project/<str:project>/remove_member/<str:user>/', views.remove_member, name='remove_member'),
    path('project/<str:ime_projekta>/edit_assign_roles/', views.edit_assign_roles, name='edit_assign_roles'),
    # sprint ============================================================
    path('project/<str:project_name>/sprints', views.sprints_list_handler, name='create_sprint'),
    path('project/<str:project_name>/sprint/<int:sprint_id>', views.sprint_details_handler, name='sprint_details'),
    path('project/<str:project_name>/new_sprint/', views.new_sprint, name='new_sprint'),
    path('project/<str:project_name>/sprint/<int:sprint_id>/edit', views.edit_sprint, name='sprint_edit'),
    path('delete_sprint/<str:project>/<int:id>', views.delete_sprint, name='delete_sprint'),
    # USER_STORY ============================================================
    path('project/<str:project_name>/new_user_story/', views.new_user_story, name='new_user_story'),
    path('project/<str:project_name>/edit_user_story/<int:id>/', views.edit_user_story, name='edit_user_story'),
    path('project/<str:project_name>/delete_user_story/<int:id>/', views.delete_user_story, name='delete_user_story'),
    path('project/<str:project_name>/accept_user_story/<int:user_story_id>/', views.accept_user_story, name='accept_user_story'),
    path('project/<str:project_name>/reject_user_story/<int:user_story_id>/', views.reject_user_story, name='reject_user_story'),
    # WALL ============================================================
    path('project/<str:project_name>/wall/', views.wall, name='wall'),
    # TASKS ============================================================
    path('project/<str:project_name>/tasks/<int:user_story_id>/', views.tasks, name='tasks'),
    path('project/<str:project_name>/new_task/<int:user_story_id>/', views.new_task, name='new_task'),
    path('project/<str:project_name>/tasks/<int:user_story_id>/<int:task_id>/accept/', views.accept_task, name='accept_task'),
    path('project/<str:project_name>/tasks/<int:user_story_id>/<int:task_id>/decline/', views.decline_task, name='decline_task'),
    path('project/<str:project_name>/tasks/<int:user_story_id>/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('project/<str:project_name>/tasks/<int:user_story_id>/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('project/<str:project_name>/tasks/<int:user_story_id>/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('project/<str:project_name>/tasks/<int:user_story_id>/<int:task_id>/start_stop/', views.start_stop_task, name='start_stop_task'),
    path('project/<str:project_name>/tasks/<int:user_story_id>/<int:task_id>/log_time/', views.log_time_task, name='log_time_task'),

    # DOCUMENTATION ============================================================
    path('project/<str:project_name>/documentation/', views.project_documentation, name='project_documentation'),
    path('project/<str:project_name>/documentation_import/', views.project_documentation_import, name='project_documentation_import'),
    path('project/<str:project_name>/documentation_export/', views.project_documentation_export, name='project_documentation_export'),
    path('project/<str:project_name>/documentation_delete/<int:doc_id>/', views.project_documentation_delete, name='project_documentation_delete'),
    path('project/<str:project_name>/documentation_edit/<int:doc_id>/', views.project_documentation_edit, name='project_documentation_edit')
    # re_path(r'^login/$', views.userApi, name='user_login')
    # re_path(r'user/[0-9]+$', views.userApi,name='test1'),
    # path('user/', views.userApi),
]