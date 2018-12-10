from django.conf.urls import url, include
# from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product/$', views.product, name='product'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url('^', include('django.contrib.auth.urls')),
]
