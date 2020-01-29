from django.forms import ModelForm
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

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone_number', 'linkedin', 'notes')

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ('jobtitle', 'company', 'joblisting', 'resume', 'applied', 'applicationDate', 'dueDate', 'notes')

class LandmarkForm(ModelForm):
    class Meta:
        model = Landmark
        fields = ('name', 'start_date_time', 'end_date_time', 'location', 'followup')