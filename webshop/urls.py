from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'order', views.OrderViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product/$', views.product, name='product'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^order/$', views.order, name='order'),    
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url('^', include('django.contrib.auth.urls')),
    url('^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/cart/$', views.Cart.as_view(), name='api_cart'),


]
