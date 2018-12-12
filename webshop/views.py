from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .forms import SignupForm
from .models import *
from .serializers import *

# DRF
from rest_framework import viewsets, permissions
from rest_framework.views import APIView

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

# class BaseViewSet ( viewsets . ModelViewSet ):
#     permission_classes = [permissions.IsAuthenticated, permissions.IsOwnerOrReadOnly]
#
#     def get_queryset(self):
#         qs = self.queryset.filter(owner=self.request.user)
#         return qs
#     def perform_create(self, serializer):
#         serializer.save(owner = self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        if category_id is None:
            queryset = Product.objects.all()
        else:
            queryset = Product.objects.filter(category_id=category_id)
        return queryset

class GetProductsByCategory(APIView):

    def get(self, request, format=None):
        return Response({"Test"})
