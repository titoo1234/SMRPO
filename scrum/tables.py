# tables.py
import django_tables2 as tables
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.utils.html import mark_safe

class ProjectTable(tables.Table):
    id = tables.Column(orderable=False, verbose_name='#')
    name = tables.Column(orderable=False)
    creation_date = tables.Column(orderable=False)
    description = tables.Column(orderable=False, verbose_name='Description')
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='')
    delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', 0)
        self.admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)

    def render_id(self, record):
        return format_html("#" +str(record.id))
    
    def render_description(self, value):
        # Uporabi HTML oznake za prikaz odstavkov v opisu
        return mark_safe(value.replace('\n', '<br>'))
    
    def render_edit_button(self, record):
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.name)
        methodology_manager = AssignedRole.objects.get(project=project,role = 'methodology_manager').user
        
        if self.admin or (user == methodology_manager):
            edit_url = reverse('project_edit', kwargs={'project_name': record.name})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
            return format_html('<a class="btn btn-info btn-sm" href="{}"><i class="fas fa-pencil-alt" style="margin-right:2px"></i>Edit</a>', edit_url)
        else:
            return ''
        
    def render_delete_button(self, record):
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.name)
        methodology_manager = AssignedRole.objects.get(project=project,role = 'methodology_manager').user
        if self.admin or (user == methodology_manager):
            edit_url = reverse('delete_project', kwargs={'project_name': record.name})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
            return format_html('<a class="btn btn-danger btn-sm" href="{}"><i class="fas fa-trash" style="margin-right:2px"></i>Delete</a>', edit_url)
        else:
            return ''
        
    class Meta:
        model = Project
        fields = ('id', 'name', 'creation_date','description')
        template_name = "table-custom.html"
        row_attrs = {
            "onClick": lambda record: "document.location.href='project/{0}/';".format(record.name)
        }


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
    workflow = tables.Column(visible=False)
    comment = tables.Column()
    user = tables.Column()
    accepted = tables.Column(visible= False)
    sprint = tables.Column(visible= False)
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')
    tasks_button = tables.Column(empty_values=(), orderable=False, verbose_name='Tasks')
    
    finish_button = tables.Column(empty_values=(), orderable=False, verbose_name='Finish|completed tasks')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', 0)
        self.admin = kwargs.pop('admin', False)
        self.product_owner = kwargs.pop('product_owner', False)
        super().__init__(*args, **kwargs)
        if (not self.product_owner):
            self.exclude = ('finish_button',)
    def before_render(self, request):
        for row in self.rows:
            if row.record.accepted:
                self.exclude = ('edit_button','delete_button')#finish_button
            # self.columns['edit_button'].visible = False
        
    def render_comment(self, value):
        colored_value = '<span style="color: red;">{}</span>'.format(value)
        html_value = mark_safe(colored_value.replace('\n', '<br>'))
        return format_html(html_value)

    def render_name(self, record):
        user_story_url = reverse('edit_user_story', kwargs={'project_name': record.project.name,'id': record.id})
        return format_html(f'<a style="font-size: 22px;" href="{user_story_url}">#{record.story_number} - {record.name}</a>')
    def render_workflow(self, value):
        if value == 'To Do':
            return format_html('<span style="color: red;">{}</span>', value)
        elif value == 'In Progress':
            return format_html('<span style="color: orange;">{}</span>', value)
        elif value == 'Done':
            return format_html('<span style="color: green;">{}</span>', value)
        else:
            return value  # Vrne vrednost brez sprememb, če ni ujemanja
    
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
    
    def render_finish_button(self, record):
        # user = User.objects.get(id = self.user_id)
        # project = Project.objects.get(name = record.project.name)
        # print(record.workflow)
        tasks = Task.objects.filter(user_story = record.id,rejected = False,deleted = False).count()
        complete_tasks = Task.objects.filter(user_story = record.id,done = True,rejected = False,deleted = False).count()
            
        tasks_info = format_html("<strong>{}/{}</strong>", complete_tasks, tasks)
        if record.accepted == False and record.sprint:
            accept_url = reverse('accept_user_story', kwargs={'project_name': record.project.name, 'user_story_id': record.id})
            reject_url = reverse('reject_user_story', kwargs={'project_name': record.project.name, 'user_story_id': record.id})
            #return format_html(f'<a href="{record.project.name}/tasks/{record.id}" class="btn btn-info">Tasks</a>')#, tasks_url)
            accept_button = format_html('<a href="{}" class="btn btn-success">Accept</a>', accept_url)
            reject_button = format_html('<a href="{}" class="btn btn-danger">Reject</a>', reject_url)
            if tasks == complete_tasks:

                return accept_button + reject_button +tasks_info
            # return accept_button + reject_button +tasks_info

        return tasks_info

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
    description = tables.Column()
    # user_story = tables.Column()
    assigned_user = tables.Column()
    #assigned_user = tables.Column(empty_values=(1))
    estimate = tables.Column()
    time_spent = tables.Column()
    accepted = tables.Column()
    user_story = tables.Column(visible= False)
    started = tables.Column(visible= False)
    accept_button = tables.Column(empty_values=(), orderable=False, verbose_name='Accept')
    decline_button = tables.Column(empty_values=(), orderable=False, verbose_name='Decline')
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')
    start_button = tables.Column(empty_values=(), orderable=False, verbose_name='Start/Stop')
    log_button = tables.Column(empty_values=(), orderable=False, verbose_name='loged time')
    complete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Complete')
    
    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', 0)
        self.product_owner = kwargs.pop('product_owner', False)
        self.active_sprint = kwargs.pop('active_sprint', False)
        self.deleted = kwargs.pop('deleted', False)
        super().__init__(*args, **kwargs)
        if self.product_owner:
            self.exclude = ('edit_button','delete_button','decline_button','accept_button','complete_button','log_button','start_button')
        if not self.active_sprint:
            self.exclude = ('edit_button','delete_button','decline_button','accept_button','complete_button','log_button','start_button')
        if self.deleted:
            self.exclude = ('edit_button','delete_button','decline_button','accept_button','complete_button','start_button','accepted','assigned_user')
    def render_description(self, value):
        # Uporabi HTML oznake za prikaz odstavkov v opisu
        return mark_safe(value.replace('\n', '<br>'))


    def before_render(self, request):
        for row in self.rows:
            user_story = UserStory.objects.get(id = row.record.user_story.id)
            if user_story.accepted:
                self.exclude = ('accept_button','decline_button','edit_button','complete_button','delete_button','log_button','start_button')#finish_button
    
    def render_accept_button(self, record):
        if record.assigned_user:
            if (record.assigned_user.id == self.user_id) and (not record.accepted):
                project = record.user_story.project
                url = reverse('accept_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                return format_html('<a href="{}" class="btn btn-success">Accept</a>', url)    
        if (not record.assigned_user) and (not record.accepted):
            project = record.user_story.project
            development_team_member = AssignedRole.objects.filter(project = project, user=self.user_id,role = 'development_team_member')
            if development_team_member:
                
                url = reverse('accept_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                return format_html('<a href="{}" class="btn btn-success">Accept</a>', url)   
        return ''
    
    def render_log_button(self, record):
        # if record.assigned_user and  record.accepted:
        #     if record.assigned_user.id == self.user_id:
        project = record.user_story.project
        url = reverse('log_time_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
        return format_html('<a href="{}" class="btn btn-secondary">Loged time</a>', url)
        return ''
    def render_start_button(self, record):
        if record.assigned_user and record.accepted:
            if record.assigned_user.id == self.user_id:
                project = record.user_story.project
                if not record.started:
                    url = reverse('start_stop_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                    return format_html('<a href="{}" class="btn btn-success">Start</a>', url)
                else:
                    url = reverse('start_stop_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                    return format_html('<a href="{}" class="btn btn-danger">Stop</a>', url)
        return ''
    
    def render_decline_button(self, record):
        if record.assigned_user:
            if record.assigned_user.id == self.user_id:
                project = record.user_story.project
                url = reverse('decline_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                return format_html('<a href="{}" class="btn btn-danger">Decline</a>', url)
        return ''
    def render_edit_button(self, record):
        project = record.user_story.project
        edit_url = reverse('edit_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
        return format_html('<a href="{}" class="btn btn-primary">Edit</a>', edit_url)
    
    def render_delete_button(self, record):
        project = record.user_story.project
        edit_url = reverse('delete_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
        return format_html('<a href="{}" class="btn btn-danger">Delete</a>', edit_url)
    
    def render_complete_button(self, record):
        if record.assigned_user:
            if (record.assigned_user.id == self.user_id) and (record.accepted): 
                project = record.user_story.project
                url = reverse('complete_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                return format_html('<a href="{}" class="btn btn-warning" onclick="return confirm(\'Ali ste prepričani, da želite zaključiti nalogo?\')">Complete</a>', url)
        return ''
        

    
    class Meta:
        model = Task
        fields = ('description', 'assigned_user', 'estimate','time_spent', 'accepted', 'accept_button','decline_button','edit_button')
        template_name = "django_tables2/bootstrap4.html"



class TimeEntryTable(tables.Table):
    user = tables.Column()
    task = tables.Column()
    start_time = tables.Column()
    end_time = tables.Column()
    logged_time = tables.Column()
    
    def render_task(self, value):
        # Uporabi HTML oznake za prikaz odstavkov v opisu
        return mark_safe(value.description)
    class Meta:
        model = TimeEntry
        fields = ('user', 'task', 'start_time', 'end_time', 'logged_time')
        template_name = "django_tables2/bootstrap4.html"