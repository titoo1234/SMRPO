from django import forms
from .models import User,Project,AssignedRole
from django.utils import timezone

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','surname','mail', 'username', 'password','admin_user']


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creation_date'].initial = timezone.now().date()
        # self.fields['creator'].disabled = True
    class Meta:
        model = Project
        fields = ['name','creation_date','description', 'creator']


class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = AssignedRole
        fields = ['user', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'] = forms.ChoiceField(choices=AssignedRole.ROLE_CHOICES)


