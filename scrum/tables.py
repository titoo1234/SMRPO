# tables.py
import django_tables2 as tables
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.utils.html import mark_safe
from datetime import datetime

class ProjectTable(tables.Table):
    id = tables.Column(orderable=False, verbose_name='#')
    name = tables.Column(orderable=False)
    creation_date = tables.Column(orderable=False)
    description = tables.Column(orderable=False, verbose_name='Description') 
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')

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
    username = tables.Column(orderable=False)
    name = tables.Column(orderable=False)
    surname = tables.Column(orderable=False)
    mail = tables.Column(orderable=False)
    admin_user = tables.Column(orderable=False)
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)
    
    def render_edit_button(self, record):
        if self.admin:
            edit_url = reverse('edit_user', kwargs={'user_id': record.id})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
            return format_html('<a class="btn btn-info btn-sm" href="{}"><i class="fas fa-pencil-alt" style="margin-right:2px"></i>Edit</a>', edit_url)
        else:
            return ''
        
    def render_delete_button(self, record):
        if self.admin:
            edit_url = reverse('delete_user', kwargs={'user_id': record.id})
            return format_html('<a class="btn btn-danger btn-sm" href="{}"><i class="fas fa-trash" style="margin-right:2px"></i>Delete</a>', edit_url)
        else:
            return ''

    class Meta:
        model = User
        fields = ('username','name', 'surname','mail','admin_user')
        template_name = "table-custom.html"


class DeletedUserTable(tables.Table):
    username = tables.Column(orderable=False)
    name = tables.Column(orderable=False)
    surname = tables.Column(orderable=False)
    mail = tables.Column(orderable=False)
    admin_user = tables.Column(orderable=False)
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)
    
    def render_edit_button(self, record):
        if self.admin:
            edit_url = reverse('edit_deleted_user', kwargs={'user_id': record.id})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
            return format_html('<a class="btn btn-info btn-sm" href="{}"><i class="fas fa-pencil-alt" style="margin-right:2px"></i>Edit</a>', edit_url)
        else:
            return ''

    class Meta:
        model = User
        fields = ('username','name', 'surname','mail','admin_user')
        template_name = "table-custom.html"

# User story
# ==============================================
class UserStoryTable(tables.Table):
    story_number = tables.Column(orderable=False, verbose_name='#')
    name = tables.Column(orderable=False)
    priority = tables.Column(orderable=False)
    size = tables.Column(orderable=False)
    workflow = tables.Column(visible=False, orderable=False)
    comment = tables.Column(orderable=False)
    user = tables.Column(orderable=False)
    accepted = tables.Column(visible= False, orderable=False)
    sprint = tables.Column(visible= False, orderable=False)
    # add_to_sprint_button = tables.Column(empty_values=(), orderable=False, verbose_name='Add to sprint')
    # edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    # delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')
    task_info = tables.Column(empty_values=(), orderable=False, verbose_name='Completed tasks')
    actions_edit = tables.Column(empty_values=(), orderable=False, verbose_name='')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', 0)
        self.admin = kwargs.pop('admin', False)
        self.product_owner = kwargs.pop('product_owner', False)
        super().__init__(*args, **kwargs)
        if (not self.product_owner):
            self.exclude = ('finish_button',)

    def render_story_number(self, record):
        return format_html("#" +str(record.story_number))

    def before_render(self, request):
        for row in self.rows:
            if row.record.accepted:
                self.exclude = ('edit_button','delete_button')#finish_button
            # self.columns['edit_button'].visible = False
            if row.record.sprint:
                self.exclude = ('add_to_sprint_button')
        
    def render_comment(self, value):
        colored_value = '<span style="color: red;">{}</span>'.format(value)
        html_value = mark_safe(colored_value.replace('\n', '<br>'))
        return format_html(html_value)

    def render_workflow(self, value):
        if value == 'To Do':
            return format_html('<span style="color: red;">{}</span>', value)
        elif value == 'In Progress':
            return format_html('<span style="color: orange;">{}</span>', value)
        elif value == 'Done':
            return format_html('<span style="color: green;">{}</span>', value)
        else:
            return value  # Vrne vrednost brez sprememb, če ni ujemanja
    
    def _get_active_sprint(self, project_name):
        project = Project.objects.get(name=project_name)
        sprints = Sprint.objects.filter(project=project)
        today = datetime.today()
        today = datetime.date(today)
        active_sprint = False
        for sprint in sprints:
            if sprint.start_date <= today <= sprint.end_date:
                active_sprint = sprint
                break
        return active_sprint

    def render_add_to_sprint_button(self, record):
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.project.name)
        methodology_manager = AssignedRole.objects.get(project=project,role = 'methodology_manager').user
        active_sprint = self._get_active_sprint(project.name)
        user_stories_in_sprint = UserStory.objects.filter(sprint=active_sprint)
        print(user_stories_in_sprint)
        user_stories_size = sum([user_story.size if user_story.size is not None else 0 for user_story in user_stories_in_sprint])
        print(user_stories_size)
        correct_size = False
        record_size = record.size if record.size is not None else 0
        if active_sprint:
            if user_stories_size + record_size <= active_sprint.velocity and record.size is not None:
                correct_size = True
        if (self.admin or (user == methodology_manager)) and correct_size and record.sprint is None:
            edit_url = reverse('add_to_sprint', kwargs={'project_name': project.name, 'user_story_id': record.id})
            return format_html('<a href="{}" class="btn btn-outline-primary btn-sm" style="margin-right:1px"><i class="fa fa-plus-circle" style="margin-right:2px"></i>Add to sprint</a>', edit_url)
        else:
            return format_html('')

    def render_edit_button(self, record):
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.project.name)
        methodology_manager = AssignedRole.objects.filter(project=project,user=user, role = 'methodology_manager').first()
        product_owner = AssignedRole.objects.filter(project=project,user=user, role = 'product_owner').first()
        development_team_member = AssignedRole.objects.filter(project=project,user=user, role = 'development_team_member').first()
        if (self.admin or ((methodology_manager or product_owner) and record.sprint is None) or ((development_team_member or methodology_manager) and record.sprint is not None)) and (not record.accepted):
            edit_url = reverse('edit_user_story', kwargs={'project_name': record.project.name,'id': record.id})
            return format_html('<a class="btn btn-info btn-sm" style="margin-right:1px" href="{}"><i class="fas fa-pencil-alt" style="margin-right:2px"></i>Edit</a>', edit_url)
        else:
            return format_html('')
        
    def render_delete_button(self, record):
        user = User.objects.get(id = self.user_id)
        project = Project.objects.get(name = record.project.name)
        methodology_manager = AssignedRole.objects.filter(project=project,user=user,role = 'methodology_manager').first()
        product_owner = AssignedRole.objects.filter(project=project,user=user,role = 'product_owner').first()
        if (self.admin or ((methodology_manager or product_owner) and record.sprint is None)) and ((not record.accepted)):
            edit_url = reverse('delete_user_story', kwargs={'project_name': record.project.name, 'id': record.id})
            return format_html('<a class="btn btn-danger btn-sm" style="margin-right:1px" href="{}"><i class="fas fa-trash" style="margin-right:2px"></i>Delete</a>', edit_url)
        else:
            return format_html('')
        
    # def render_tasks_button(self, record):
    #     tasks_url = reverse('tasks', kwargs={'project_name': record.project.name, 'user_story_id': record.id})
    #     #return format_html(f'<a href="{record.project.name}/tasks/{record.id}" class="btn btn-info">Tasks</a>')#, tasks_url)
    #     return format_html('<a href="{}" class="btn btn-info">Tasks</a>', tasks_url)
    def render_task_info(self, record):
        tasks = Task.objects.filter(user_story = record.id,rejected = False,deleted = False).count()
        complete_tasks = Task.objects.filter(user_story = record.id,done = True,rejected = False,deleted = False).count()
        completed = int((complete_tasks/tasks)*100) if tasks != 0 else 0
        tasks_info = format_html('<div class="progress progress-sm"><div class="progress-bar bg-green" role="progressbar" aria-valuenow="{}" aria-valuemin="0" aria-valuemax="{}" style="width: {}%"></div></div><small>{}% Complete</small>', complete_tasks, tasks, completed, completed)
        return tasks_info

    def render_finish_button(self, record):
        tasks = Task.objects.filter(user_story = record.id,rejected = False,deleted = False).count()
        complete_tasks = Task.objects.filter(user_story = record.id,done = True,rejected = False,deleted = False).count()
            
        # tasks_info = format_html("<strong>{}/{}</strong>", complete_tasks, tasks)
        # if tasks == 0:#ČE NI NOBENE NALOGE ŠE NOT NE MORŠ KONČAT 
        #     return tasks_info
        if record.accepted == False and record.sprint:
            accept_url = reverse('accept_user_story', kwargs={'project_name': record.project.name, 'user_story_id': record.id})
            reject_url = reverse('reject_user_story', kwargs={'project_name': record.project.name, 'user_story_id': record.id})
            accept_button = format_html('<a href="{}" class="btn btn-outline-success btn-sm" style="margin-right:1px"><i class="fa fa-check" style="margin-right:2px"></i>Accept</a>', accept_url)
            reject_button = format_html('<a href="{}" class="btn btn-outline-danger btn-sm" style="margin-right:1px"><i class="fa fa-times" style="margin-right:2px"></i>Reject</a>', reject_url)
            if (tasks == complete_tasks) and tasks != 0:
                if self.product_owner:
                    return accept_button + reject_button #+tasks_info
                # else:
                #     return #tasks_info
            else:
                if self.product_owner:
                    return reject_button #+tasks_info
                #else:
                    #return tasks_info
        # return tasks_info
        return format_html('')
    
    def render_actions_edit(self, record):
        return self.render_add_to_sprint_button(record) + self.render_finish_button(record) + self.render_edit_button(record) + self.render_delete_button(record)
    
    class Meta:
        model = UserStory
        fields = ('story_number', 'name','priority', 'size', 'workflow', 'user', 'comment', 'task_info','actions_edit')#,'tasks_button')
        template_name = "table-custom.html"
        row_attrs = {
            "onClick": lambda record: "document.location.href='/project/{0}/tasks/{1}/';".format(record.project.name, record.id)
        }



class UserStoryInfoTable(tables.Table):
    #name = tables.Column()
    priority = tables.Column()
    size = tables.Column()
    comment = tables.Column()
    user = tables.Column()
    original_estimate = tables.Column()
    business_value = tables.Column()
    acceptance_tests = tables.Column()
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    sprint = tables.Column()


    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', 0)
        self.admin = kwargs.pop('admin', False)
        self.product_owner = kwargs.pop('product_owner', False)
        super().__init__(*args, **kwargs)
        if (not self.product_owner):
            self.exclude = ('finish_button',)

    def before_render(self, request):
        if self.product_owner:
            for row in self.rows:
                self.exclude = ('edit_button')

    def render_comment(self, value):
        colored_value = '<span style="color: red;">{}</span>'.format(value)
        html_value = mark_safe(colored_value.replace('\n', '<br>'))
        return format_html(html_value)

    def render_acceptance_tests(self, value):
        # Uporabi HTML oznake za prikaz odstavkov v opisu
        return mark_safe(value.replace('\n', '<br>'))
    

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

    class Meta:
        model = UserStory
        fields = ('comment','sprint', 'priority', 'size', 'user', 'original_estimate', 'business_value', 'acceptance_tests')
        template_name = "django_tables2/bootstrap5.html"

# Sprint
# ==============================================
class SprintTable(tables.Table):
    class Meta:
        model = Sprint
        template_name = "django_tables2/bootstrap4.html"
        


class TaskTable(tables.Table):
    # task_number = tables.Column(orderable=False, verbose_name='#')
    description = tables.Column(orderable=False)
    # user_story = tables.Column()
    assigned_user = tables.Column(orderable=False)
    #assigned_user = tables.Column(empty_values=(1))
    # estimate = tables.Column(orderable=False, verbose_name='Estimate[h]')
    # time_spent = tables.Column(orderable=False, verbose_name='Time spent[h]')
    # time_to_finish = tables.Column(orderable=False, verbose_name='Time left[h]')
    accepted = tables.Column(orderable=False, visible=False)
    user_story = tables.Column(visible= False, orderable=False)
    started = tables.Column(visible= False, orderable=False)
    # accept_button = tables.Column(empty_values=(), orderable=False, verbose_name='Accept')
    # decline_button = tables.Column(empty_values=(), orderable=False, verbose_name='Decline')
    # edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')
    # delete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Delete')
    # start_button = tables.Column(empty_values=(), orderable=False, verbose_name='Start/Stop')
    # log_button = tables.Column(empty_values=(), orderable=False, verbose_name='')
    # complete_button = tables.Column(empty_values=(), orderable=False, verbose_name='Complete')
    status = tables.Column(empty_values=(), orderable=False, verbose_name='Status')
    time_spent_left = tables.Column(empty_values=(), orderable=False, verbose_name='')
    actions_edit = tables.Column(empty_values=(), orderable=False, verbose_name='')
    actions_accept = tables.Column(empty_values=(), orderable=False, verbose_name='')
    actions_logging = tables.Column(empty_values=(), orderable=False, verbose_name='')
    
    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info', False)
        self.user_id = kwargs.pop('user_id', 0)
        self.product_owner = kwargs.pop('product_owner', False)
        self.active_sprint = kwargs.pop('active_sprint', False)
        self.deleted = kwargs.pop('deleted', False)
        super().__init__(*args, **kwargs)
        if self.product_owner:
            self.exclude = ('edit_button','delete_button','actions_accept','complete_button','start_button','log_button')
        if not self.active_sprint:
            self.exclude = ('edit_button','delete_button','actions_accept','complete_button','start_button')
        if self.deleted:
            self.exclude = ('edit_button','delete_button','actions_accept','complete_button','status', 'start_button','accepted','assigned_user')
    def render_description(self, value):
        # Uporabi HTML oznake za prikaz odstavkov v opisu
        return mark_safe(value.replace('\n', '<br>'))


    def before_render(self, request):
        for row in self.rows:
            user_story = UserStory.objects.get(id = row.record.user_story.id)
            if user_story.accepted:
                self.exclude = ('accept_button','decline_button','edit_button','complete_button','delete_button','start_button')#finish_button
    
    def render_accept_button(self, record):
        if record.assigned_user:
            if (record.assigned_user.id == self.user_id) and (not record.accepted):
                project = record.user_story.project
                url = reverse('accept_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                return format_html('<a href="{}"><i class="fa fa-check" style="color:green"></i></a>', url)    
        if (not record.assigned_user) and (not record.accepted):
            project = record.user_story.project
            development_team_member = AssignedRole.objects.filter(project = project, user=self.user_id,role = 'development_team_member')
            if development_team_member:
                
                url = reverse('accept_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                return format_html('<a href="{}"><i class="fa fa-check" style="color:green"></i></a>', url)   
        return format_html('')

    def render_log_button(self, record):
        # if record.assigned_user and  record.accepted:
        #     if record.assigned_user.id == self.user_id:
        project = record.user_story.project
        url = reverse('log_time_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
        return format_html('<a href="{}"><i title="Logged Time" class="fas fa-clock" style="color:black; margin: 3px"></i></a>', url)

    def render_start_button(self, record):
        if record.assigned_user and record.accepted:
            if record.assigned_user.id == self.user_id:
                project = record.user_story.project
                if not record.started:
                    url = reverse('start_stop_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                    return format_html('<a href="{}" disabled><i title="Stop Time" class="fa fa-stop" style="color:red; margin: 3px; pointers-events:none; opacity:0.5"></i></a><a href="{}"><i title="Start Time" class="fa fa-play" style="color:green; margin: 3px"></i></a>', '#', url)
                else:
                    url = reverse('start_stop_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                    return format_html('<a href="{}"><i title="Stop Time"  class="fa fa-stop" style="color:red; margin: 3px"></i></a><a href="{}" disabled><i title="Start Time"  class="fa fa-play" style="color:green; margin: 3px; pointers-events:none; opacity:0.5"></i></a>', url, '#')
        return format_html('')
    
    def render_decline_button(self, record):
        if record.assigned_user:
            if record.assigned_user.id == self.user_id:
                project = record.user_story.project
                url = reverse('decline_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                return format_html('<a href="{}"><i class="fa fa-times" style="color:red"></i></a>', url)
        return format_html('')

    def render_edit_button(self, record):
        project = record.user_story.project
        edit_url = reverse('edit_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
        return format_html('<a class="btn btn-info btn-sm" style="margin-right:1px" href="{}"><i class="fas fa-pencil-alt" style="margin-right:2px"></i>Edit</a>', edit_url)
    
    def render_delete_button(self, record):
        project = record.user_story.project
        edit_url = reverse('delete_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
        return format_html('<a class="btn btn-danger btn-sm" style="margin-right:1px" href="{}"><i class="fas fa-trash" style="margin-right:2px"></i>Delete</a>', edit_url)
    
    def render_complete_button(self, record):
        if record.assigned_user:
            if (record.assigned_user.id == self.user_id) and (record.accepted): 
                project = record.user_story.project
                url = reverse('complete_task', kwargs={'project_name': project.name,'user_story_id': record.user_story.id,'task_id': record.id}) #project_name,user_story_id,task_id
                return format_html('<a href="{}" class="btn btn-warning btn-sm" style="margin-right:1px" onclick="return confirm(\'Do you really want to complete this task?\')"><i class="fa fa-check-circle-o" style="margin-right:2px"></i>Complete</a>', url)
        return format_html('')
        
    def render_time_spent(self, value):
        return value//3600
    
    def render_actions_edit(self, record):
        return self.render_complete_button(record) + self.render_edit_button(record) + self.render_delete_button(record)
    
    def render_actions_accept(self, record):
        return self.render_accept_button(record) + self.render_decline_button(record)
    
    def render_actions_logging(self, record):
        if self.product_owner:
            return self.render_log_button(record)
        else:
            return self.render_start_button(record) + self.render_log_button(record)
        
    def render_time_spent_left(self, record):
        time_spent = self.render_time_spent(record.time_spent)
        time_left = record.time_to_finish
        time_estimate = record.estimate
        return format_html('<span title="Time Estimate" class="badge badge-success" style="margin: 3px">{} points</span>', time_estimate) + format_html('<span title="Time Spent / Time Left" class="badge badge-warning" style="margin: 3px">{} / {} hours</span>', time_spent,  time_left)
    
    def render_status(self, record):
        if record.done:
            return format_html('<span class="badge badge-info">Completed</span>')
        if record.accepted:
            if record.started:
                return format_html('<span class="badge badge-success">Active</span>')
            else:
                return format_html('<span class="badge badge-secondary">Accepted</span>')
        else:
            return format_html('<span class="badge badge-danger">Unaccepted</span>')



    # def render_time_to_finish(self, record):
    #     # time_entries = TimeEntry.objects.filter(task = record.id)
    #     # time_to_finish = 0
    #     # for time_entry in time_entries:
    #     #     time_to_finish += time_entry.time_to_finish
    #     # return time_to_finish//3600
    #     try:
    #         time_entry = TimeEntry.objects.get(task=record.id, date=datetime.now().date())
    #     except Exception as e:
    #         print("NE DELA")
    class Meta:
        model = Task
        fields = ('assigned_user','description',  'status', 'time_spent_left', 'actions_accept', 'actions_logging')
        template_name = "table-custom.html"



class TimeEntryTable(tables.Table):
    user = tables.Column(orderable=False)
    task = tables.Column(orderable=False)
    date = tables.Column(orderable=False)
    logged_time = tables.Column(orderable=False)
    # time_to_finish = tables.Column()
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')


    def __init__(self, *args, **kwargs):
        self.other = kwargs.pop('other', False)

        super().__init__(*args, **kwargs)
        if self.other:
            self.exclude = ('edit_button')
        


    def before_render(self, request):
        for row in self.rows:
            task = row.record.task
            stori = task.user_story
            if stori.accepted:
                self.exclude = ('edit_button')




    def render_task(self, value):
        # Uporabi HTML oznake za prikaz odstavkov v opisu
        return mark_safe(value.description)

    #def render_date(self, value):
    #    return format_html("{}", value)

    def render_logged_time(self, value):
        return format_html("{}", value//3600)

    # def render_time_to_finish(self, value):
    #     return format_html("{}", value)#//3600

    def render_edit_button(self, record):

        edit_url = reverse('edit_time_entry', kwargs={'project_name': record.task.user_story.project.name,'user_story_id': record.task.user_story.id,'task_id': record.task.id, 'time_entry_id': record.id}) #project_name,user_story_id,task_id
        return format_html('<a class="btn btn-info btn-sm" style="margin-right:1px" href="{}"><i class="fas fa-pencil-alt" style="margin-right:2px"></i>Edit</a>', edit_url)
    #def render_start_time(self, value):
    #    return format_html(value.strftime('%H:%M:%S'))

    class Meta:
        model = TimeEntry
        fields = ('user', 'task', 'date', 'logged_time')
        template_name = "table-custom.html"



class DocumentationTable(tables.Table):
    

    project =  tables.Column(visible=False)
    title =  tables.Column(visible = False)
    content =  tables.Column(orderable=False, verbose_name='')
    author =  tables.Column(visible=False)
    last_edit_date =  tables.Column(visible=False)
    edit_button = tables.Column(empty_values=(), orderable=False, verbose_name='Edit')

    def render_edit_button(self, record):
        # <a href="/project/{{ project.name }}/documentation_edit/{{ dokument.id }}/"><button class="btn">Edit Documentation</button></a>
        edit_url = reverse('project_documentation_edit', kwargs={'project_name': record.project.name,'doc_id':record.id})  # Nadomestite 'ime_pogleda' s pravim imenom pogleda
        return format_html('<a class="btn btn-info btn-sm" href="{}"><i class="fas fa-pencil-alt" style="margin-right:2px"></i>Edit</a>', edit_url)
        
    def render_content(self, value):
        # Uporabi HTML oznake za prikaz odstavkov v opisu
        return mark_safe(value.replace('\n', '<br>'))
    class Meta:
        model = Documentation
        fields = ('content','edit_button')
        template_name = "table-custom.html"