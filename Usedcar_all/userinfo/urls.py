from django.conf.urls import url
from django.contrib import admin
from userinfo import views

urlpatterns = [
    url(r'login/$', views.signin, name='login'),
    url(r'loginin/', views.login_, name='login_in'),
    url(r'register/$', views.register, name='register'),
    url(r'registerin/', views.register_, name='register_in'),
    url(r'logout/$', views.logout_, name='logout'),
    url(r'buyinfo/$', views.buyinfo, name='buyinfo'),
    url(r'infomes/$', views.infomes, name='infomes'),
    url(r'infomesin/', views.infomes_, name='infomes_in'),
    url(r'service/$', views.service, name='service'),
]