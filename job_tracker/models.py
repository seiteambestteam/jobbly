from django.db import models
from datetime import date, datetime

class JobUser(models.Model):
    #extend the user model to inlude links
    #extends user - michelle will figure out how to do this
    linkedin = models.CharField(max_length=200)
    github = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    jobsearch = models.CharField(max_length=200)

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
    user = models.ForeignKey(JobUser, on_delete=models.CASCADE)

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    linkedin = models.CharField(max_length=50)
    notes = models.TextField(max_length=300)
    application = models.ForeignKey(Application, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(JobUser, on_delete=models.CASCADE)

class Landmark(models.Model):
    #event is a python keyword, so ive gone with landmark. we can change this if yall want
    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    followup = models.DateTimeField()
    application = models.ForeignKey(Application, on_delete=models.CASCADE)