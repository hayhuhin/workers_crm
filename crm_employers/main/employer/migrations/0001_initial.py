# Generated by Django 4.1.13 on 2023-12-30 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '__first__'),
        ('tasks', '0005_alter_task_additional_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=50, null=True)),
                ('rank', models.IntegerField(null=True)),
                ('started_at', models.DateTimeField()),
                ('salary', models.IntegerField()),
                ('task', models.ManyToManyField(blank=True, to='tasks.departmenttask')),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('profile_pic', models.ImageField(default='profile_pics/profile_picture.jpeg', upload_to='profile_pics')),
                ('graph_permission', models.ManyToManyField(to='dashboard.graphpermission')),
                ('insights_permission', models.ManyToManyField(to='dashboard.graphinsights')),
                ('job_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employer.department')),
                ('lead', models.ManyToManyField(to='tasks.lead')),
                ('task', models.ManyToManyField(to='tasks.task')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
