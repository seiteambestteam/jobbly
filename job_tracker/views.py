from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core import serializers
from .models import User, Contact, Landmark, Application
from .forms import *
from .packages import CareerjetAPIClient
import requests
from bs4 import BeautifulSoup
import os
import uuid
import boto3


S3_BASE_URL = 'https://s3.amazonaws.com/'
BUCKET = 'jobbly'

def home(request):
    return render(request, 'home.html')

def index(request):
    # users = User.objects.filter(user=request.user)
    news_key = os.environ['NEWS_API_KEY']
    news_url = ('https://newsapi.org/v2/top-headlines?''country=ca&''category=technology&' 'page=1&' 'pageSize=15&' f'apiKey={news_key}')
    news_response = requests.get(news_url)
    news = news_response.json()
    return render(request, 'users/index.html', { 'news':news })
    
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


def job_search_api(request):
    search_term = request.GET.get('searchTerm')
    location = request.GET.get('location') 
    cj  =  CareerjetAPIClient("en_CA")
    job_data = cj.search({
                        'location'    : location,
                        'keywords'    : search_term,
                        'affid'       : os.environ['CAREERJET_API_KEY'],
                        'user_ip'     : '72.143.53.170',
                        'url'         : 'http://localhost:8000/jobsearch?q=python&l=london',
                        'user_agent'  : 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
    })
    return JsonResponse(job_data, safe=False)

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

def get_calendar(request):
    user = request.user
    event_qs = Landmark.objects.filter(application__user_id=user.id)
    data = []
    for event in event_qs:
        data.append({
            'title': f'{event.name}, {event.application.company}',
            'start': event.start_date_time,
            'end': event.end_date_time,
            'url': f'/applications/{event.application.id}',
        })
    return JsonResponse(data, safe=False)

def calendar(request):
    return render(request, 'calendar.html')

def contacts_index(request):
    contacts = Contact.objects.filter(user=request.user)
    return render(request, 'contacts/index.html', { 'contacts': contacts})

def contacts_detail(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    return render(request, 'contacts/detail.html', { 'contact': contact })

class ContactCreate(CreateView):
    model = Contact
    fields = ['name', 'email', 'linkedin', 'notes', 'application']
    success_url = '/contacts/index/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ContactUpdate(UpdateView):
    model = Contact
    fields = ['name', 'email', 'linkedin', 'notes']
    success_url = '/contacts/index/'

class ContactDelete(DeleteView):
    model = Contact
    success_url ='/contacts/index/'

def application(request):
    application = Application.objects.filter(user = request.user)
    profile_form = ProfileForm()
    return render(request, 'applications/index.html', { 'applications': application })

def applications_detail(request, application_id):
    application = Application.objects.get(id=application_id)
    return render(request, 'applications/detail.html', { 'application': application })

class ApplicationCreate(CreateView):
    model = Application
    fields = ['jobtitle', 'company', 'joblisting', 'applied', 'applicationDate', 'dueDate', 'notes']

# 'resume',

    def form_valid(self, form):
        form.instance.user = self.request.user
        resume_file = self.request.FILES.get('resume-file', None)
        if resume_file:
            session = boto3.Session(profile_name='jobbly')
            jobbly_s3 = session.client('s3')
            key = uuid.uuid4().hex[:6] + resume_file.name[resume_file.name.rfind('.'):]
            try:
                jobbly_s3.upload_fileobj(resume_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                form.instance.resume = url
                form.instance.resumekey = key                
            except Exception as e:
                # return error handling here if it doesn't upload
                print(e)
                print('Sorry, an error occurred uploading the file to AWS S3')
        return super().form_valid(form)

class ApplicationUpdate(UpdateView):
    model = Application
    fields = ['jobtitle', 'company', 'joblisting', 'resume', 'applied', 'applicationDate', 'dueDate', 'notes']

class ApplicationDelete(DeleteView):
    model = Application
    fields = ['jobtitle', 'company', 'joblisting', 'resume', 'applied', 'applicationDate', 'dueDate', 'notes']
    success_url = '/applications/'

class LandmarkList(ListView):
    model = Landmark

class LandmarkDetail(DetailView):
    model = Landmark

class LandmarkCreate(CreateView):
    model = Landmark
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LandmarkUpdate(UpdateView): 
    model = Landmark
    fields = '__all__'

class LandmarkDelete(DeleteView):
    model = Landmark
    success_url = '/landmarks/'

def assoc_landmark(request, application_id, landmark_id):
    Application.objects.get(id=application_id).landmark.add(landmark_id)
    return redirect('application', application_id=application_id)
