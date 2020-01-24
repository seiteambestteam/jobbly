from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def index(request):
    # users = User.objects.filter(user=request.user)
    return render(request, 'users/index.html')