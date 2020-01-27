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
        fields = ('linkedin', 'github', 'website', 'jobsearch')

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'linkedin', 'notes')