# tables.py
import django_tables2 as tables
from .models import Project

class ProjectTable(tables.Table):
    name = tables.Column()
    creation_date = tables.Column()

    class Meta:
        model = Project
        fields = ('name', 'creation_date')
        template_name = "django_tables2/bootstrap5.html" 