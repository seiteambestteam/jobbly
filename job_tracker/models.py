from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=200, blank=True)
    github = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)
    jobsearch = models.CharField(max_length=200, default='Web Developer')
    joblocation = models.CharField(max_length=200, default='Toronto, ON')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Application(models.Model):
    jobtitle = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    joblisting = models.CharField(max_length=300)
    resume = models.CharField(max_length=200)
    resumekey = models.CharField(max_length=50)
    applied = models.BooleanField()
    applicationDate = models.DateField()
    dueDate = models.DateField()
    notes = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    notes = models.TextField(max_length=400)
    application = models.ForeignKey(Application, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Landmark(models.Model):
    #drop down
    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    followup = models.DateTimeField()
    application = models.ForeignKey(Application, on_delete=models.CASCADE)