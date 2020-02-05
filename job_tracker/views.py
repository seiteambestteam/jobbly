from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django import forms
from .models import User, Contact, Landmark, Application
from .forms import *
from .packages import CareerjetAPIClient
import requests
from django.forms import Textarea
import os
import uuid
import boto3


S3_BASE_URL = 'https://s3.amazonaws.com/'
BUCKET = 'jobbly'

def home(request):
    return render(request, 'home.html')
@login_required
def index(request):
    news_key = os.environ['NEWS_API_KEY']
    news_url = ('https://newsapi.org/v2/top-headlines?''country=ca&''category=technology&' 'page=1&' 'pageSize=15&' f'apiKey={news_key}')
    news_response = requests.get(news_url)
    news = news_response.json()
    return render(request, 'users/index.html', { 'news':news })
    
def about(request):
    return render(request, 'about.html')

def team(request):
    return render(request, 'team.html')

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

@login_required
def profile(request):
    return render(request, 'profile.html', { 'user': request.user})

@login_required
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

@login_required
def delete(request):
    user = request.user
    user.is_active = False
    user.save()
    return redirect('home')

@login_required
def confirm_delete(request):
    return render(request, 'users/account_confirm_delete.html')

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
        if event.followup:
            data.append({
                'title': f'Follow up for {event.application.company} {event.name}',
                'start': event.followup,
                'url': f'/applications/{event.application.id}',
            })
    return JsonResponse(data, safe=False)

@login_required
def calendar(request):
    return render(request, 'calendar.html')

@login_required
def contacts_index(request):
    contacts = Contact.objects.filter(user=request.user).order_by('name')
    return render(request, 'contacts/index.html', {'contacts': contacts })

def get_contacts(request):
    contacts = Contact.objects.filter(user=request.user)
    contacts_data = []
    for contact in contacts:
        if contact.application:
            contacts_data.append({
                'name': f'{contact.name}',
                'email': f'{contact.email}',
                'linkedin': f'{contact.linkedin}',
                'notes': f'{contact.notes}',
                'company': f'{contact.application.company}',
                'application': f'{contact.application.jobtitle}',
                'id':f'{contact.id}'
            })
        else:
            contacts_data.append({
                'name': f'{contact.name}',
                'email': f'{contact.email}',
                'linkedin': f'{contact.linkedin}',
                'notes': f'{contact.notes}',
                'id':f'{contact.id}'
            })


    return JsonResponse(contacts_data, safe=False)

@login_required
def add_contact(request, application_id):
    form = ContactForm(request.POST)
    if form.is_valid():
        new_contact = form.save(commit=False)
        new_contact.application_id = application_id
        new_contact.user_id = request.user.id
        new_contact.save()
    return redirect('applications_detail', application_id = application_id)

class ContactCreate(LoginRequiredMixin, CreateView):
    model = Contact
    success_url = '/contacts/index/'
    form_class = ContactForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class ContactUpdate(LoginRequiredMixin, UpdateView):
    model = Contact
    success_url = '/contacts/index/'
    form_class = ContactForm

class ContactDelete(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url ='/contacts/index/'

@login_required
def application(request):
    application = Application.objects.filter(user = request.user)
    profile_form = ProfileForm()
    return render(request, 'applications/index.html', { 'applications': application })

@login_required
def applications_detail(request, application_id):
    application = Application.objects.get(id=application_id)
    landmark_form = LandmarkForm()
    contact_form = ContactForm()
    return render(request, 'applications/detail.html', { 'application': application, 'landmark_form': landmark_form, 'contact_form': contact_form })

def remove_resume(request, application_id):
    application = Application.objects.get(pk=application_id)
    #switch sessions to profile if running on local host
    #session = boto3.Session(profile_name='jobbly')
    session = boto3.Session()
    jobbly_s3 = session.client('s3')
    try:
        jobbly_s3.delete_object(Bucket=BUCKET, Key=application.resumekey)
    except Exception as e:
        print(e)
    return redirect('applications_update', pk=application_id)

@login_required
def application_create_from_search(request):
    application_form = ApplicationForm()
    
    return render(request, 'job_tracker/application_form_populated.html', {'application_form': application_form, 'jobtitle': request.POST['jobtitle'], 'company': request.POST['company'], 'joblisting': request.POST['joblisting']})


class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    success_url = '/applications/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        resume_file = self.request.FILES.get('resume-file', None)

        if resume_file:
            #switch sessions to profile if running on local host
            #session = boto3.Session(profile_name='jobbly')
            session = boto3.Session()
            jobbly_s3 = session.client('s3')
            key = uuid.uuid4().hex[:6] + resume_file.name[resume_file.name.rfind('.'):]
            try:
                jobbly_s3.upload_fileobj(resume_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                form.instance.resume = url
                form.instance.resumekey = key                
            except Exception as e:
                print(e)
                print('Sorry, an error occurred uploading the file to AWS S3')
        return super().form_valid(form)

class ApplicationUpdate(LoginRequiredMixin, UpdateView):
    model = Application
    form_class = ApplicationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        resume_file = self.request.FILES.get('resume-file', None)

        if resume_file:
            #switch sessions to profile if running on local host
            #session = boto3.Session(profile_name='jobbly')
            session = boto3.Session()
            jobbly_s3 = session.client('s3')
            key = uuid.uuid4().hex[:6] + resume_file.name[resume_file.name.rfind('.'):]
            try:
                jobbly_s3.upload_fileobj(resume_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"

                if self.object.resumekey:
                    jobbly_s3.delete_object(Bucket=BUCKET, Key=self.object.resumekey)
                form.instance.resume = url
                form.instance.resumekey = key
            except Exception as e:
                print(e)
                print('Sorry, an error occurred uploading the file to AWS S3')
        return super().form_valid(form)

    def remove_resume(request, application_id):
        application = Application.objects.get(id=application_id)
        #switch sessions to profile if running on local host
        #session = boto3.Session(profile_name='jobbly')
        session = boto3.Session()
        jobbly_s3 = session.client('s3')
        try:
            jobbly_s3.delete_object(Bucket=BUCKET, Key=application.resumekey)
        except Exception as e:
            print(e)
        return redirect('applications_update', pk=application_id)

class ApplicationDelete(LoginRequiredMixin, DeleteView):
    model = Application
    fields = ['jobtitle', 'company', 'joblisting', 'resume', 'applied', 'applicationDate', 'dueDate', 'notes']
    success_url = '/applications/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.resume):
            application = Application.objects.get(id=self.object.id)
            #switch sessions to profile if running on local host
            #session = boto3.Session(profile_name='jobbly')
            session = boto3.Session()
            jobbly_s3 = session.client('s3')
            try:
                jobbly_s3.delete_object(Bucket=BUCKET, Key=application.resumekey)
            except Exception as e:
                print(e)
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

@login_required
def add_landmark(request, application_id):
    print('add landmark route')
    form = LandmarkForm(request.POST)
    if form.is_valid():
        print('is valid')
        new_landmark = form.save(commit=False)
        new_landmark.application_id = application_id
        new_landmark.save()
    return redirect('applications_detail', application_id = application_id)

class LandmarkUpdate(LoginRequiredMixin, UpdateView): 
    model = Landmark
    form_class = LandmarkForm

    def get_success_url(self):
        return reverse('applications_detail', kwargs={'application_id': self.object.application_id})

class LandmarkDelete(LoginRequiredMixin, DeleteView):
    model = Landmark
    form_class = LandmarkForm
    def get_success_url(self):
        return reverse('applications_detail', kwargs={'application_id': self.object.application_id})

def assoc_landmark(request, application_id, landmark_id):
    Application.objects.get(id=application_id).landmark.add(landmark_id)
    return redirect('application', application_id=application_id)

def unassoc_landmark(request, application_id, landmark_id):
    Application.objects.get(id=application_id).landmarks.remove(landmark_id)
    return redirect('detail', application_id=application_id)
