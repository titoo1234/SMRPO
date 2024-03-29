from django import forms
from django.contrib.auth.hashers import check_password
from .models import User,Project,AssignedRole,UserStory, Sprint, ProjectWall
from django.utils import timezone
from django.forms.models import inlineformset_factory

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
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
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User
        fields = ['name', 'surname', 'mail', 'username', 'password', 'confirm_password', 'admin_user']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")

    # def save(self, commit=True):
    #     user = super(UserRegisterForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
from django import forms

class UserUpdateForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput, label='Current password', required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, label='New password', required=False)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label='Confirm new password', required=False)

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
        fields = ['name', 'workflow', 'description', 'project', 'sprint', 'priority', 'size', 'original_estimate', 'business_value', 'user', 'acceptance_tests']
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
        edit = self.initial['edit']

        methodology_manager_not_in_sprint_fields = set(['name', 'description', 'priority', 'business_value', 'acceptance_tests', 'sprint', 'size', 'original_estimate', 'user'])
        product_owner_fields_not_in_sprint_fields = set(['name', 'description', 'priority', 'business_value', 'acceptance_tests'])
        development_team_fields_not_in_sprint_fields = set([])
        methodology_manager_in_sprint_fields = set(['sprint', 'user'])
        product_owner_fields_in_sprint_fields = set([])
        development_team_fields_in_sprint_fields = set(['workflow'])

        methodology_manager_fields = set(['name', 'description', 'priority', 'business_value', 'acceptance_tests'])
        product_owner_fields = set(['name', 'description', 'priority', 'business_value', 'acceptance_tests'])
        development_team_fields = set([])

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




