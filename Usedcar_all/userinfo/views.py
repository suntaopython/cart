from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.db import DataError, DatabaseError
from django.http import request, response
from django.contrib import messages
from .models import *
from sale.models import *
import logging
import random
import json
# Create your views here.csrf_protect

auth_check = 'MarcelArhut'


def signin(request):
    return render(request, 'login.html')


def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return render(request, 'register.html')


def login_(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('userpwd', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'message':"用户名或密码错误"})
    return HttpResponse(" ")


new_user = UserInfo()


def register_(request):
    if request.method == 'POST':
        new_user.username = request.POST.get('username')
        try:
            olduser = UserInfo.objects.filter(username=new_user.username)
            if len(olduser) > 0:
                return render(request, 'register.html', {'message': '用户名已经存在'})
        except ObjectDoesNotExist as e:
            logging.warning(e)
        if request.POST.get('userpwd') != request.POST.get('reuserpwd'):
            return render(request, 'register.html', {'message': '两次输入的密码不一致'})
        new_user.password = make_password(request.POST.get('userpwd'), auth_check, 'pbkdf2_sha1')
        if 'tobuy' in request.POST:
            return render(request, 'buyregister.html')
        if 'tosale' in request.POST:
            return render(request, 'info-message.html')
    # return HttpResponse(" ")


def buyinfo(request):
    if request.method == 'POST':
        new_user.realname = request.POST.get("realname")
        new_user.uidentity = request.POST.get("identity")
        new_user.address = request.POST.get("address")
        new_user.cellphone = request.POST.get("phone")
        new_user.sex = request.POST.getlist("gender")[0]
        try:
            new_user.save()
        except ObjectDoesNotExist as e:
            logging.warning(e)
        return redirect('/')


def logout_(request):
    auth.logout(request)
    return redirect('/')


def infomes(request):
    return render(request, 'info-message.html')


def infomes_(request):
    # if request.is_ajax():
    if request.method == 'POST':
        # print(request.POST)
        new_user.realname = request.POST.get("realname")
        new_user.uidentity = request.POST.get("identity")
        new_user.address = request.POST.get("address")
        new_user.cellphone = request.POST.get("phone")
        new_user.sex = request.POST.getlist("gender")[0]
        try:
            new_user.save()
        except ObjectDoesNotExist as e:
            logging.warning(e)

        brand = Brand()
        brand.btitle = request.POST.getlist("brands")[0]
        try:
            oldbrand = Brand.objects.filter(btitle=brand.btitle)
            if len(oldbrand) > 0:
                brand = oldbrand[0]
            else:
                brand.save()
        except DatabaseError as e:
            logging.warning(e)

        car = Carinfo()
        car.ctitle = request.POST.get("model")
        car.regist_date = request.POST.get("regist_date")
        car.engineNo = request.POST.get("engineNo")
        car.mileage = request.POST.get("mileage")
        car.maintenance_record = request.POST.getlist("isService")[0]
        car.price = request.POST.get("price")
        car.extractprice = int(car.price) * 0.02 + int(car.price)
        car.newprice = request.POST.get("newprice")
        car.picture = request.FILES.get('pic')
        car.formalities = request.POST.getlist("formalities")[0]
        car.debt = request.POST.getlist("isDebt")[0]
        car.promise = request.POST.get("promise")
        car.serbran = brand
        car.user = new_user
        try:
            car.save()
        except ObjectDoesNotExist as e:
            logging.warning(e)
        return redirect("/")
    return HttpResponse(" ")


def service(request):
    return render(request, 'service.html')




