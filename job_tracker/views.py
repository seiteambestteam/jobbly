from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import User, Contact, Landmark
from .forms import UserForm, ProfileForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'friendscollector'

def home(request):
    return render(request, 'home.html')

def index(request):
    # users = User.objects.filter(user=request.user)
    return render(request, 'users/index.html')
    
def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('edit_profile')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context={'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def profile(request):
    return render(request, 'profile.html', { 'user': request.user})

def edit_profile(request):
    error_message = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            error_message = 'Please correct the error below.'
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'error_message': error_message,
    })

class ContactCreate(CreateView):
    model = Contact
    fields = ['name', 'email', 'linkedin', 'notes', 'application']
    success = '/home/'

    # def form_valid(self, form):
    # form.instance.user = self.request.user

class ContactUpdate(UpdateView):
    model = Contact
    fields = ['name', 'email', 'linkedin', 'notes', 'application']
    success = '/home/'

class ContactDelete(DeleteView):
    model = Contact
    fields = ['name', 'email', 'linkedin', 'notes', 'application']
    success ='/home/'

def application(request):
    application = Application.objects.filter(user = request.user)
    profile_form = ProfileForm()
    return render(request, 'application/index.html', { 'applications': application, 'application_form': application_form })

class LandmarkList(ListView):
    model = Landmark

class LandmarkDetail(DetailView):
    model = Landmark

class LandmarkCreate(CreateView):
    model = Landmark
    fields = '__all__'

class LandmarkUpdate(UpdateView):
    model = Landmark
    fields = '__all__'

def assoc_landmark(request, application_id, landmark_id):
    Application.objects.get(id=application_id).landmark.add(landmark_id)
    return redirect('application', application_id=application_id)
