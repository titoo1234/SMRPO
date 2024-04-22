from django import forms
from django.contrib.auth.hashers import check_password
from .models import User,Project,AssignedRole,UserStory, Sprint, ProjectWall,Task,Documentation, TimeEntry
from django.utils import timezone
from django.forms.models import inlineformset_factory
from datetime import datetime, time
import hashlib

#from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=64)
    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, min_length=12, max_length=64,strip=False)
    class Meta:
        model = User
        fields = ['name','surname','mail', 'username', 'password','admin_user']

class UserRegisterForm1(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=12, max_length=64,strip=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=12, max_length=64, label='Confirm password')

    class Meta:
        model = User
        fields = ['name', 'surname', 'mail', 'username', 'password', 'confirm_password', 'admin_user']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")
        
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        # Hash the password before saving
        user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if commit:
            user.save()
        return user

    # def save(self, commit=True):
    #     user = super(UserRegisterForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
from django import forms

class UserUpdateForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput, max_length=64,label='Current password', required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=12, max_length=64, label='New password', required=False)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, min_length=12, max_length=64, label='Confirm new password', required=False)

    class Meta:
        model = User
        fields = ['name', 'surname', 'mail', 'username', 'current_password', 'new_password', 'confirm_new_password', 'admin_user']

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        # Proverimo, da je novo geslo enako potrjenemu novemu geslu
        if new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match. Please enter the same password in both fields.")

        # Ako su oba nova gesla prazna, ne radimo provjeru starog gesla
        if not new_password and not confirm_new_password:
            return

        # Proverimo da li je staro geslo tačno
        user = self.instance
        # print(user.password)
        if current_password and (current_password != user.password):
            raise forms.ValidationError( "Current password is incorrect. Please try again.")

        if new_password:
            user.password = new_password

        # Nastavimo posodobljeni objekt uporabnika nazaj v instance
        self.instance = user

        return cleaned_data


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creation_date'].initial = timezone.now().date()
        self.fields['creator'].widget = forms.HiddenInput() 
        #self.fields['creator'].disabled = True #TODO: zaenkrat je samo disablan, treba spremenit da bo fiksen
    class Meta:
        model = Project
        fields = ['name','creation_date','description',"creator"]
        widgets = {
            'creation_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProjectDisabledForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'creation_date', 'description', 'creator']
        widgets = {
            'name': forms.TextInput(attrs={'disabled': 'disabled'}),
            'creation_date': forms.DateInput(attrs={'disabled': 'disabled'}),
            'description': forms.Textarea(attrs={'disabled': 'disabled'}),
            'creator': forms.TextInput(attrs={'disabled': 'disabled'}),
        }

class IntegerVelocityField(forms.IntegerField):
    def to_python(self, value):
        value = super().to_python(value)
        if value is not None:
            try:
                return int(value)
            except (ValueError, TypeError):
                raise forms.ValidationError('Enter a valid integer.')

class VelocityInput(forms.TextInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs.update({'placeholder': 'Enter velocity in pts'})
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, {'type': self.input_type, 'name': name})
        if value != '':
            value = '%s pts' % value
        return super().render(name, value, final_attrs, renderer)

class SprintForm(forms.ModelForm):
    velocity = forms.IntegerField(label='Velocity (pts)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set project field as a TextInput widget and disable it
        self.fields['project'].widget = forms.TextInput(attrs={'readonly': True, 'style': 'pointer-events: none;'})
        self.fields['project'].initial = kwargs['initial']['project']
        self.fields['start_date'].initial = timezone.now().date()
        self.fields['end_date'].initial = timezone.now().date() + timezone.timedelta(days=14)
        if kwargs['initial']['edit']:
            self.fields['start_date'].initial = kwargs['initial']['start_date']
            self.fields['end_date'].initial = kwargs['initial']['end_date']
            if kwargs['initial']['active']:
                self.fields['start_date'].widget.attrs['disabled'] = True
                self.fields['end_date'].widget.attrs['disabled'] = True
            self.fields['velocity'].initial = kwargs['initial']['velocity']

    class Meta:
        model = Sprint
        fields = ['project','start_date','end_date','velocity']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }
        '''widgets = {
            'name': forms.TextInput(attrs={'disabled': 'disabled'}),
            'start_date': forms.DateInput(attrs={'disabled': 'disabled'}),
            'end_date': forms.Textarea(attrs={'disabled': 'disabled'}),
        }'''

class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = AssignedRole
        fields = ['user', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'] = forms.ChoiceField(choices=AssignedRole.ROLE_CHOICES)

class UserStoryForm(forms.ModelForm):
    class Meta:
        model = UserStory
        fields = ['name', 'description', 'project', 'sprint', 'priority', 'size', 'original_estimate', 'business_value', 'user', 'acceptance_tests']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Name'}), 
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'3', 'placeholder': 'Description'}), 
            'project': forms.HiddenInput(), 
            'sprint': forms.Select(attrs={'class':'form-control', 'placeholder': 'Choose sprint'}), 
            'priority': forms.Select(attrs={'class':'form-control', 'placeholder': 'Priority'}), 
            'size': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Size'}), 
            'business_value': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Business value'}), 
            'acceptance_tests': forms.Textarea(attrs={'class':'form-control', 'rows': 5, 'placeholder': '# test 1\n# test 2\n# test 3\n...'}), 
            'workflow': forms.Select(attrs={'class':'form-control', 'placeholder': 'Priority'}), 
            'user': forms.Select(attrs={'class':'form-control', 'placeholder': 'Choose user'}), 
            'original_estimate': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Original estimate'}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = self.initial['project']
        
        development_team_members = AssignedRole.objects.filter(project = self.project, role='development_team_member')
        users = [(object.user.id, str(object.user.username)) for object in development_team_members]
        users += [(None, '---------')]
        self.fields['user'].choices = users
        fields_from_meta = self._meta.fields
        product_owner = self.initial['product_owner']
        methodology_manager = self.initial['methodology_manager']
        development_team_member = self.initial['development_team_member']
        sprint = self.initial['sprint']
        if sprint is None:
            self.fields['sprint'].widget = forms.HiddenInput()
        edit = self.initial['edit']
        today = datetime.today()
        today = datetime.date(today)
        active_sprints = Sprint.objects.filter(project=self.project,start_date__lte=today, end_date__gte=today)
        # active_sprints = []
        self.fields['sprint'].queryset = active_sprints

        methodology_manager_not_in_sprint_fields = set(['name', 'description', 'priority', 'business_value', 'acceptance_tests', 'sprint', 'size', 'original_estimate', 'user'])
        product_owner_fields_not_in_sprint_fields = set(['name', 'description', 'priority', 'business_value', 'acceptance_tests'])
        development_team_fields_not_in_sprint_fields = set([])
        methodology_manager_in_sprint_fields = set(['sprint', 'user'])
        product_owner_fields_in_sprint_fields = set([])
        development_team_fields_in_sprint_fields = set(['workflow'])

        methodology_manager_fields = set(['name', 'description', 'priority', 'business_value', 'acceptance_tests'])
        product_owner_fields = set(['name', 'description', 'priority', 'business_value', 'acceptance_tests'])
        development_team_fields = set([])

        accepted = self.initial.get('accepted')
        if accepted:
            for field_name in self.fields.keys():
                self.fields[field_name].widget.attrs['disabled'] = True

        if edit:
            if methodology_manager and development_team_member and sprint is None:
                for field, value in self.fields.items():
                    if field not in methodology_manager_not_in_sprint_fields: self.fields[field].disabled = True
            elif methodology_manager and sprint is None:
                for field, value in self.fields.items():
                    if field not in methodology_manager_not_in_sprint_fields: self.fields[field].disabled = True
            elif product_owner and sprint is None:
                for field, value in self.fields.items():
                    if field not in product_owner_fields_not_in_sprint_fields: self.fields[field].disabled = True
            elif development_team_member and sprint is None:
                for field, value in self.fields.items():
                    if field not in development_team_fields_not_in_sprint_fields: self.fields[field].disabled = True
            elif methodology_manager and development_team_member and sprint is not None:
                for field, value in self.fields.items():
                    if field not in methodology_manager_in_sprint_fields: self.fields[field].disabled = True
            elif methodology_manager and sprint is not None:
                for field, value in self.fields.items():
                    if field not in methodology_manager_in_sprint_fields: self.fields[field].disabled = True
            elif product_owner and sprint is not None:
                for field, value in self.fields.items():
                    if field not in product_owner_fields_in_sprint_fields: self.fields[field].disabled = True
            elif development_team_member and sprint is not None:
                for field, value in self.fields.items():
                    if field not in development_team_fields_in_sprint_fields: self.fields[field].disabled = True
        else:
            if methodology_manager and development_team_member:
                for field, value in self.fields.items():
                    if field not in methodology_manager_fields: self.fields[field].disabled = True
            elif methodology_manager:
                for field, value in self.fields.items():
                    if field not in methodology_manager_fields: self.fields[field].disabled = True
            elif product_owner:
                for field, value in self.fields.items():
                    if field not in product_owner_fields: self.fields[field].disabled = True
            elif development_team_member:
                for field, value in self.fields.items():
                    if field not in development_team_fields: self.fields[field].disabled = True
                
class ProjectWallForm(forms.ModelForm):
    class Meta:
        model = ProjectWall
        fields = ["text"]



class NewTaskForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        project_name = kwargs.pop('project_name', None)
        user_story_id = kwargs.pop('user_story_id', None)
        super().__init__(*args, **kwargs)
        if user_story_id:
            story = UserStory.objects.get(id = user_story_id)
            self.fields['user_story'].initial = story
            self.fields['user_story'].widget = forms.HiddenInput()
        
        self.fields['assigned_user'].queryset = self.get_development_team_members(project_name)
               # Check if task is already accepted
    
        task = kwargs.get('instance', None)
        if task and task.accepted:
            del self.fields['assigned_user']

    def get_development_team_members(self, project_name):
        project = Project.objects.get(name = project_name)
        assigned_roles = AssignedRole.objects.filter(project=project,role = 'development_team_member')
        development_team_users = [role.user for role in assigned_roles]
        return User.objects.filter(id__in=[user.id for user in development_team_users])
        
    class Meta:
        model = Task
        fields = ['description','user_story' ,'assigned_user','estimate' ]#'time_spent' pri novem še ne rabimo?
        # [ 'name', 'description','user_story' ,'assigned_user' ,'start_date' ,'end_date' ,'time_spent' ]
        labels = {
        'estimate': 'Estimate[h]'
    }

class TimeEntryForm(forms.ModelForm):
    time_to_finish = forms.IntegerField(label='Time to finish[h]')  
    def __init__(self, *args, **kwargs):
        user_assigned = kwargs.pop('user_assigned', True)
        logged_time = kwargs.pop('logged_time', 0)
        super().__init__(*args, **kwargs)
        # self.fields['date'].initial = kwargs['initial']['date']
        # # self.fields['logged_time'].initial = kwargs['initial']['logged_time']
        # self.fields['logged_time'].initial = self.instance.logged_time if self.instance else None
        instance = kwargs.get('instance')
        if instance:
            task = instance.task
            initial = kwargs.get('initial', {})
            initial['time_to_finish'] = task.time_to_finish
            kwargs['initial'] = initial
        if logged_time:
            initial['logged_time'] = logged_time
            kwargs['initial'] = initial
          
        
        super().__init__(*args, **kwargs)
        if not user_assigned:

            self.fields['time_to_finish'].widget.attrs['hidden'] = True
        
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['task'].widget = forms.HiddenInput()
        self.fields['start_time'].widget = forms.HiddenInput()
        self.fields['end_time'].widget = forms.HiddenInput()
        self.fields['date'].widget.attrs['disabled'] = True
        self.fields['logged_time'].label = 'Logged Time[h]'
        

    class Meta:
        model = TimeEntry
        fields = ['user', 'task', 'date', 'start_time', 'end_time', 'logged_time']#, 'time_to_finish'
        # [ 'name', 'description','user_story' ,'assigned_user' ,'start_date' ,'end_date' ,'time_spent' ]
        # fields = ['date', 'start_time', 'end_time', 'time_to_finish']

# time_to_finish
#       self.fields['time_to_finish'].initial = kwargs['initial']['time_to_finish']
class KomentarObrazec(forms.Form):
    komentar = forms.CharField(label='Komentar', widget=forms.Textarea)


class UvozForm(forms.Form):
    title = forms.CharField(max_length=100)

    # document = forms.FileField()
    document = forms.FileField(label=('Select File'),help_text='Only .txt formats are allowed',  widget=forms.ClearableFileInput(attrs={'accept': '.txt'}))

class DocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = ['title', 'content']
    



