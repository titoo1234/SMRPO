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
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = User
        fields = ['name','surname','mail', 'username', 'password','admin_user']

class UserRegisterForm1(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User
        fields = ['name', 'surname', 'mail', 'username', 'password', 'confirm_password', 'admin_user']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Gesli se ne ujemata. Prosim vnesite isto geslo v obeh poljih.")

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
            raise forms.ValidationError("Novi gesli se ne ujemata. Prosim vnesite isto geslo v obeh poljih.")

        # Ako su oba nova gesla prazna, ne radimo provjeru starog gesla
        if not new_password and not confirm_new_password:
            return

        # Proverimo da li je staro geslo tačno
        user = self.instance
        # print(user.password)
        if current_password and (current_password != user.password):
            raise forms.ValidationError("Trenutno geslo ni pravilno. Preverite in poskusite ponovno.")

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
        # labels = {
        #     'name': "", 
        #     'description': "",
        #     'project': "",
        #     'sprint': "",
        #     'priority': "",
        #     'size': "",
        #     'business_value': "",
        #     'acceptance_tests': ""
        # }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Name'}), 
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'3', 'placeholder': 'Description'}), 
            'project': forms.HiddenInput(), 
            'sprint': forms.Select(attrs={'class':'form-control', 'placeholder': 'Choose sprint'}), 
            'priority': forms.Select(attrs={'class':'form-control', 'placeholder': 'Priority'}), 
            'size': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Size'}), 
            'business_value': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Business value'}), 
            'acceptance_tests': forms.Textarea(attrs={'class':'form-control', 'rows': 5, 'placeholder': 'Acceptance tests'}), 
        }

class ProjectWallForm(forms.ModelForm):
    class Meta:
        model = ProjectWall
        fields = ["text"]




