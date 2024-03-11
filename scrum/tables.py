# tables.py
import django_tables2 as tables
from .models import Project,User,AssignedRole
from django.urls import reverse
from django.utils.html import format_html
from django.utils.html import mark_safe
class ProjectTable(tables.Table):
    name = tables.Column()
    creation_date = tables.Column()
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', 0)
        self.admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)
    
    def render_name(self, record):
        project_url = reverse('project_name', kwargs={'project_name': record.name})
        return format_html('<a href="{}">{}</a>'.format(project_url, record.name))

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
        fields = ('name', 'creation_date')
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