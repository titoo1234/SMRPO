# tables.py
import django_tables2 as tables
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.utils.html import mark_safe

class ProjectTable(tables.Table):
    name = tables.Column()
    creation_date = tables.Column()
    description = tables.Column(orderable=False, verbose_name='Description')
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')


    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', 0)
        self.admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)
    
    def render_description(self, value):
        # Uporabi HTML oznake za prikaz odstavkov v opisu
        return mark_safe(value.replace('\n', '<br>'))
    
    def render_name(self, record):
        project_url = reverse('project_name', kwargs={'project_name': record.name})
        return format_html('<a style="font-size: 22px;" href="{}">{}</a>'.format(project_url, "#" +str(record.id)+" "+ record.name))

    def render_edit_button(self, record):
        
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.name)
        methodology_manager = AssignedRole.objects.get(project=project,role = 'methodology_manager').user
        
        if self.admin or (user == methodology_manager):
            edit_url = reverse('project_edit', kwargs={'project_name': record.name})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
            return format_html('<a href="{}" class="btn btn-primary">Edit</a>', edit_url)
        else:
            return ''
    def render_delete_button(self, record):
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.name)
        methodology_manager = AssignedRole.objects.get(project=project,role = 'methodology_manager').user
        if self.admin or (user == methodology_manager):
            edit_url = reverse('delete_project', kwargs={'project_name': record.name})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
            return format_html('<a href="{}" class="btn btn-danger">Delete</a>', edit_url)
        else:
            return ''
    class Meta:
        model = Project
        fields = ('name', 'creation_date','description')
        template_name = "django_tables2/bootstrap5.html"


class UserTable(tables.Table):
    username = tables.Column()
    name = tables.Column()
    surname = tables.Column()
    mail = tables.Column()
    admin_user = tables.Column()
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)
    
    def render_edit_button(self, record):
        if self.admin:
            edit_url = reverse('edit_user', kwargs={'user_id': record.id})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
            return format_html('<a href="{}" class="btn btn-primary">Edit</a>', edit_url)
        else:
            return ''

    class Meta:
        model = User
        fields = ('username','name', 'surname','mail','admin_user')
        template_name = "django_tables2/bootstrap5.html"


class DeletedUserTable(tables.Table):
    username = tables.Column()
    name = tables.Column()
    surname = tables.Column()
    mail = tables.Column()
    admin_user = tables.Column()
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)
    
    def render_edit_button(self, record):
        if self.admin:
            edit_url = reverse('edit_deleted_user', kwargs={'user_id': record.id})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
            return format_html('<a href="{}" class="btn btn-primary">Edit</a>', edit_url)
        else:
            return ''

    class Meta:
        model = User
        fields = ('username','name', 'surname','mail','admin_user')
        template_name = "django_tables2/bootstrap5.html"

# User story
# ==============================================
class UserStoryTable(tables.Table):
    name = tables.Column()
    priority = tables.Column()
    size = tables.Column()
    workflow = tables.Column()
    user = tables.Column()
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')
    tasks_button = tables.Column(empty_values=(), orderable=False, verbose_name='Tasks')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', 0)
        self.admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)

    def render_name(self, record):
        user_story_url = reverse('edit_user_story', kwargs={'project_name': record.project.name,'id': record.id})
        return format_html(f'<a style="font-size: 22px;" href="{user_story_url}">#{record.story_number} - {record.name}</a>')
    
    def render_edit_button(self, record):
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.project.name)
        methodology_manager = AssignedRole.objects.filter(project=project,user=user, role = 'methodology_manager').first()
        product_owner = AssignedRole.objects.filter(project=project,user=user, role = 'product_owner').first()
        development_team_member = AssignedRole.objects.filter(project=project,user=user, role = 'development_team_member').first()
        if self.admin or ((methodology_manager or product_owner) and record.sprint is None) or ((development_team_member or methodology_manager) and record.sprint is not None):
            edit_url = reverse('edit_user_story', kwargs={'project_name': record.project.name,'id': record.id})
            return format_html('<a href="{}" class="btn btn-primary">Edit</a>', edit_url)
        else:
            return ''
        
    def render_delete_button(self, record):
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.project.name)
        methodology_manager = AssignedRole.objects.filter(project=project,user=user,role = 'methodology_manager').first()
        product_owner = AssignedRole.objects.filter(project=project,user=user,role = 'product_owner').first()
        if self.admin or ((methodology_manager or product_owner) and record.sprint is None):
            edit_url = reverse('delete_user_story', kwargs={'project_name': record.project.name, 'id': record.id})
            return format_html('<a href="{}" class="btn btn-danger">Delete</a>', edit_url)
        else:
            return ''
        
    def render_tasks_button(self, record):
        tasks_url = reverse('tasks', kwargs={'project_name': record.project.name, 'user_story_id': record.id})
        #return format_html(f'<a href="{record.project.name}/tasks/{record.id}" class="btn btn-info">Tasks</a>')#, tasks_url)
        return format_html('<a href="{}" class="btn btn-info">Tasks</a>', tasks_url)

    class Meta:
        model = UserStory
        fields = ('name','priority', 'size', 'workflow', 'user', 'edit_button','delete_button','tasks_button')
        template_name = "django_tables2/bootstrap5.html"

# Sprint
# ==============================================
class SprintTable(tables.Table):
    class Meta:
        model = Sprint
        template_name = "django_tables2/bootstrap4.html"


class TaskTable(tables.Table):
    class Meta:
        model = Task
        template_name = "django_tables2/bootstrap4.html"
