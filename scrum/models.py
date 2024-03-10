from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(default = '',max_length=100)
    mail = models.EmailField(blank = True,max_length = 100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    admin_user = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateField()
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

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
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    size = models.IntegerField()
    business_value = models.IntegerField()
    acceptance_tests = models.TextField()

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    time_spent = models.PositiveIntegerField(default=0)
    # STATUS_CHOICES = (
    #     ('To-Do', 'To-Do'),
    #     ('In Progress', 'In Progress'),
    #     ('Done', 'Done'),
    # )
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    def __str__(self):
        return self.name

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
        return f"{self.user.username} - {self.project.name} -"