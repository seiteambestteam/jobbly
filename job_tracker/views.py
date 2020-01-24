from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Contact, Landmark

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

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

