from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .forms import SignupForm
from .models import *
from .serializers import *
from decimal import *
import json
from django.db import transaction

# DRF
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Create your views here.
def index(request):
    return render(request, 'index.html')

def product(request):
    return render(request, 'product.html')

def cart(request):
    if request.user.is_authenticated():
        return render(request, 'cart.html')
    else:
        return HttpResponseRedirect(reverse('index'))


def order(request):
    if request.user.is_authenticated():
        return render(request, 'order.html')
    else:
        return HttpResponseRedirect(reverse('index'))

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

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    # def get_serializer_context(self):
    #     return {'request': self.request}

@permission_classes((IsAuthenticated, ))
class Cart(APIView):
    def post(self, request, format=None):
        tag = request.data['tag']
        if tag == "addCart":
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
        if tag == "buy":
            cart = request.session.get('cart', {})
            if cart == {}:
                return HttpResponse(json.dumps({'success': False, 'status': 'no_items_cart'}))
            ids = cart.keys()
            queryset = Product.objects.filter(pk__in=ids)
            grandTotal = 0
            for p in queryset:
                qty = cart[str(p.id)]
                if qty > p.stock:
                    return HttpResponse(json.dumps({'success': False, 'status': 'not_in_stock'}))
                totalPrice = p.price * qty
                grandTotal += totalPrice
            account = Account.objects.get(id=request.user.id)
            with transaction.atomic():
                if(grandTotal < account.balance):
                    for p in queryset:
                        qty = cart[str(p.id)]
                        p.stock -= qty
                        p.save()
                    account.balance -= grandTotal
                    account.save()
                    Order.objects.create(user=account, total_price=grandTotal)
                    request.session['cart'] = {}
                    success = True
                    status = "ok"
                else:
                    status = 'insufficient_funds'
                    success = False
                return HttpResponse(json.dumps({'success': success, 'status': status}))

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
