from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import User, Contact, Landmark
from .forms import UserForm, ProfileForm
import requests
from bs4 import BeautifulSoup

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

def job_search(request):
    url = request.GET.get('url')
    if request.user:
        location = request.user.profile.joblocation
        location_string = location.replace(' ', '+').replace(',', '%2C')
        url = url + '&l=' + location_string
    base_url = 'https://www.simplyhired.ca'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='job-list')
    job_elems = results.find_all('div', class_='SerpJob-jobCard')
    job_data = []

    for job in job_elems:
        title_elem = job.find('a', class_='card-link')
        info = {
            'job_link' : base_url + title_elem['href'],
            'title' : title_elem.text,
            'company' : job.find('span', class_='jobposting-company').text,
            'location' : job.find('span', class_='jobposting-location').text,
            'description' : job.find('p', class_='jobposting-snippet').text,
        }
        job_data.append(info)
    return JsonResponse(job_data, safe=False)

class ContactCreate(CreateView):
    model = Contact
    fields = ['name', 'email', 'linkedin', 'notes', 'application']
    success = '/home/'

class ContactUpdate(UpdateView):
    model = Contact
    fields = ['name', 'email', 'linkedin', 'notes', 'application']
    success = '/home/'

class ContactDelete(DeleteView):
    model = Contact
    fields = ['name', 'email', 'linkedin', 'notes', 'application']
    success ='/home/'