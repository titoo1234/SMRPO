from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Upper
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(default = '',max_length=100)
    mail = models.EmailField(blank = True,max_length = 100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    admin_user = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100,unique=True)
    creation_date = models.DateField()
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    def clean(self):
        # Preveri, ali obstaja projekt z enakim imenom (brez razlik v velikosti črk)
        existing_projects = Project.objects.filter(name__iexact=self.name).exclude(pk=self.pk)
        if existing_projects.exists():
            raise ValidationError(_('Project with this name already exists.'))

    def save(self, *args, **kwargs):
        # Preveri, ali obstaja projekt z enakim imenom (brez razlik v velikosti črk)
        existing_projects = Project.objects.filter(name__iexact=self.name).exclude(pk=self.pk)
        if existing_projects.exists():
            raise ValidationError(_('Project with this name already exists.'))
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    velocity = models.PositiveIntegerField(default=14)

    def __str__(self):
        return f"Sprint({self.start_date},{self.end_date})"

class UserStory(models.Model):
    must_have = 'must_have'
    could_have = 'could_have'
    should_have = 'should_have'
    wont_have_this_time = "wont_have_this_time"
    PRIORITY_CHOICES = [
        (must_have, 'Must have'),
        (could_have, 'Could have'),
        (should_have, 'Should have'),
        (wont_have_this_time, "Won't have this time"),
    ]
    to_do = 'to_do'
    in_progress = 'in_progress'
    done = 'done'
    WORKFLOW = [
        (to_do, 'To Do'),
        (in_progress, 'In Progress'),
        (done, 'Done'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, blank=True, null=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, blank=True)
    size = models.PositiveIntegerField(blank=True, null=True)
    original_estimate = models.PositiveIntegerField(blank=True, null=True)
    workflow = models.CharField(max_length=50, choices=WORKFLOW, default=to_do)
    business_value = models.PositiveIntegerField(blank=True, null=True)
    acceptance_tests = models.TextField(blank=True)
    story_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['story_number']  # Razvrščanje zgodbe po številki zgodbe v padajočem vrstnem redu
        unique_together = ('name', 'project')
        constraints = [
            models.UniqueConstraint(Upper('name'), name='unique_upper_name_category', violation_error_message='Name already exists.')
        ]

    @classmethod
    def get_next_story_number(cls, project_id):
        last_story = cls.objects.filter(project_id=project_id).last()
        if last_story:
            return last_story.story_number + 1
        else:
            return 1  # Če ni nobene zgodbe, začnemo z 1
    
    def clean(self):
        current = UserStory.objects.filter(id=self.id).first()
        if self.workflow in [self.in_progress, self.done] and not self.sprint:
            raise ValidationError("Cannot set workflow to 'In Progress' or 'Done' without a sprint.")
        if self.acceptance_tests:
            lines = self.acceptance_tests.split('\n')
            for line in lines:
                if not line.startswith('# '):
                    raise ValidationError("Acceptance tests should start with '# ' character.")
        if self.sprint and not self.original_estimate:
            raise ValidationError("Original estimate must be provided before adding user story to the sprint.")
        if current and current.sprint and current.original_estimate != self.original_estimate:
            raise ValidationError("Original estimate can not be changed while in sprint.")

        super().clean() 

    def save(self, *args, **kwargs):
        if not self.story_number:
            self.story_number = self.get_next_story_number(self.project_id)
        super().save(*args, **kwargs)

class Task(models.Model):
    ## tega pomojm ne rabmo
    # name = models.CharField(max_length=100)
    # =============
    description = models.TextField()
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)#Ni ga treba dodeltiti od začetka
    ## tega pomojm ne rabmo
    # start_date = models.DateField()
    # end_date = models.DateField()
    # =============
    time_spent = models.PositiveIntegerField(default=0)
    accepted = models.BooleanField(default=False)
    estimate = models.PositiveIntegerField(default=1)
    done = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)#ko rejectaš zgodbo da rejectaš tudi vse naloge, da jih kasneje lahko prikažeš kot "stare"
    started = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['description', 'user_story'], name='unique_task_user_story_description')
        ]


    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    logged_time = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.end_time:
            # Izračunajte porabljeni čas, če je končni čas nastavljen
            time_spent = (self.end_time - self.start_time).seconds #// 60  # Pretvorite čas v minute
            self.logged_time = time_spent
        super().save(*args, **kwargs) 
    

class ProjectWall(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    post = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    post_date = models.DateTimeField()

class Documentation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_edit_date = models.DateTimeField()



#ZA DODELJEVANJE VLOG NA PROJEKTU
class AssignedRole(models.Model):
    ROLE_CHOICES = [
        ('product_owner', 'Product Owner'),
        ('methodology_manager', 'Methodology Manager'),
        ('development_team_member', 'Development Team Member'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.project.name} - {self.role}"
    

#ZA EVIDENCO ČLANOV V PROJEKTU
class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    class Meta:
        # Unikatna kombinacija uporabnika in projekta
        unique_together = ['user', 'project']

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"