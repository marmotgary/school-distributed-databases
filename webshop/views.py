from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .forms import SignupForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def product(request):
    return render(request, 'product.html')

class SignUp(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

class Login(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'
