# Generated by Django 5.0.2 on 2024-02-26 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0004_alter_user_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mail',
            field=models.EmailField(blank=True, max_length=100),
        ),
    ]
