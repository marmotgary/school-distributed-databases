from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .forms import SignupForm
from .models import *
from .serializers import *
from decimal import *
import json

# DRF
from rest_framework import viewsets, permissions
from rest_framework.views import APIView

# Create your views here.
def index(request):
    return render(request, 'index.html')

def product(request):
    return render(request, 'product.html')

def cart(request):
    return render(request, 'cart.html')

class SignUp(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

class Login(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

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


class Cart(APIView):
    def post(self, request, format=None):
        productId = request.data['productId']
        try:
            product = Product.objects.get(id=productId)
            # For whatever reason using int keys with dictionary saved to session caused problems. => using str instead.
            productId = str(productId)
            cart = request.session.get('cart', {})
            if productId in cart:
                cart[productId] += 1
            else:
                cart[productId] = 1
            request.session['cart'] = cart

            success = True
        except Exception as e:
            print("Exception", e)
            success = False
        print("success: ", success)
        return HttpResponse(json.dumps({'success': success}))

    def get(self, request, format=None):
        cart = request.session.get('cart', {})
        ids = cart.keys()
        queryset = Product.objects.filter(pk__in=ids)
        serializer = ProductSerializer(queryset, many=True)
        data = serializer.data
        grandTotal = 0
        for product in data:
            qty = cart[str(product['id'])]
            product['inCart'] = qty
            totalPrice = Decimal(product['price']) * qty
            product['totalPrice'] = str(totalPrice)
            grandTotal += totalPrice

        account = Account.objects.get(id=request.user.id)
        accountBalance = account.balance
        sufficientFunds = accountBalance > grandTotal
        balanceAfterPurchase = accountBalance - grandTotal
        balance = {
            "accountBalance": str(accountBalance),
            "grandTotal": str(grandTotal),
            'sufficientFunds': sufficientFunds,
            'balanceAfterPurchase': str(balanceAfterPurchase)
        }

        message = {"products": data, "balance": balance}
        return HttpResponse(json.dumps(message))
        # return HttpResponse(json.dumps(message))
