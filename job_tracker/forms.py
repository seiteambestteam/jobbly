from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('linkedin', 'github', 'website', 'jobsearch', 'joblocation')
        labels = {
            'jobsearch': 'Ideal Job Position',
            'joblocation': 'Desired Job Location',
        }

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone_number', 'linkedin', 'notes')

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ('jobtitle', 'company', 'joblisting', 'applied', 'applicationDate', 'dueDate', 'notes')
        labels = {
            'jobtitle': 'Position',
            'joblisting': 'Job Listing URL',
            'applicationDate': 'Application Date',
            'dueDate': 'Application Due Date',
        }
        # widgets = {
        #     'jobtitle':TextField(attrs={'class': 'edit-form-labels'})
        # }

class LandmarkForm(ModelForm):
    class Meta:
        model = Landmark
        fields = ('name', 'start_date_time', 'end_date_time', 'location', 'followup')
        labels = {
            'start_date_time': 'Event Start Time',
            'end_date_time': 'Event End Time',
            'followup': 'Follow-up Date',
        }