# Generated by Django 2.2.9 on 2020-01-24 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobtitle', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=50)),
                ('joblisting', models.CharField(max_length=300)),
                ('resume', models.CharField(max_length=200)),
                ('resumekey', models.CharField(max_length=50)),
                ('applied', models.BooleanField()),
                ('applicationDate', models.DateField()),
                ('dueDate', models.DateField()),
                ('notes', models.TextField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin', models.CharField(blank=True, max_length=200)),
                ('github', models.CharField(blank=True, max_length=200)),
                ('website', models.CharField(blank=True, max_length=200)),
                ('jobsearch', models.CharField(default='Web Developer', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Landmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('datetime', models.DateTimeField()),
                ('location', models.CharField(max_length=200)),
                ('followup', models.DateTimeField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_tracker.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=100)),
                ('linkedin', models.CharField(max_length=100)),
                ('notes', models.TextField(max_length=400)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='job_tracker.Application')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
