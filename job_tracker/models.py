from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

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
    joblisting = models.CharField(max_length=300, blank=True)
    resume = models.CharField(max_length=200, blank=True)
    resumekey = models.CharField(max_length=50, blank=True)
    applied = models.BooleanField()
    applicationDate = models.DateField(blank=True, null=True)
    dueDate = models.DateField(blank=True, null=True)
    notes = models.TextField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("applications_detail", kwargs={"application_id": self.id})

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    notes = models.TextField(max_length=400, blank=True)
    application = models.ForeignKey(Application, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("contacts_detail", kwargs={"contact_id": self.id})
    

class Landmark(models.Model):
    #drop down
    name = models.CharField(max_length=50)
    start_date_time = models.DateTimeField(blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    followup = models.DateTimeField(blank=True, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("landmarks_detail", kwargs={'pk': self.id})
