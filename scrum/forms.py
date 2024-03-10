from django import forms

from .models import User,Project,AssignedRole,UserStory, Sprint
from django.utils import timezone
from django.forms.models import inlineformset_factory

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = User
        fields = ['name','surname','mail', 'username', 'password','admin_user']

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creation_date'].initial = timezone.now().date()
        self.fields['creator'].disabled = False #TODO: zaenkrat je samo disablan, treba spremenit da bo fiksen
    class Meta:
        model = Project
        fields = ['name','creation_date','description', 'creator']

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

class SprintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].initial = timezone.now().date()
        self.fields['end_date'].initial = timezone.now().date() + timezone.timedelta(days=14)
    class Meta:
        model = Sprint
        fields = ['project','start_date','end_date','duration']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
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
        fields = ('name', 'description', 'project', 'sprint', 'priority', 'size', 'business_value', 'acceptance_tests')
        labels = {
            'name': "", 
            'description': "",
            'project': "",
            'sprint': "",
            'priority': "",
            'size': "",
            'business_value': "",
            'acceptance_tests': ""
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ime'}), 
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'3', 'placeholder': 'Opis'}), 
            'project': forms.Select(attrs={'class':'form-control', 'placeholder': 'Izberi projekt'}), 
            'sprint': forms.Select(attrs={'class':'form-control', 'placeholder': 'Izberi sprint'}), 
            'priority': forms.Select(attrs={'class':'form-control', 'placeholder': 'Prioriteta'}), 
            'size': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Dolžina'}), 
            'business_value': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Poslovna vrednost'}), 
            'acceptance_tests': forms.Textarea(attrs={'class':'form-control', 'rows': 5, 'placeholder': 'Sprejemni testi'}), 
        }

    def __init__(self, *args, **kwargs):
        super(UserStoryForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = None
        self.fields['sprint'].empty_label = None
        self.fields['priority'].empty_label = None






