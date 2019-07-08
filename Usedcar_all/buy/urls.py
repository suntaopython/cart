from django.conf.urls import url
from django.contrib import admin
from buy import views

urlpatterns = [
    url(r'addorder', views.add_order, name='addorder'),
    url(r'buylist', views.buylist, name='buylist'),
    url(r'userinfo', views.user_info, name='userinfo'),
    url(r'confirmbuy', views.confirmbuy, name='confirmbuy'),
    url(r'delcart', views.del_order, name='delcart'),
    url(r'brandlist/$', views.brandlist, name='brandlist'),
    url(r'cancel_order/', views.cancel_order, name='cancelorder'),
    url(r'alter_info/', views.alter_info, name='alter_info'),
    url(r'reoffer/', views.reoffer, name='reoffer'),
]