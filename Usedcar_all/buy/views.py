from django.shortcuts import render, redirect
from django.http import HttpResponse
from userinfo.models import *
from sale.models import Carinfo
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from .models import *
from sale.models import *
import json
import datetime
import logging

# Create your views here.
def add_order(request):
    if request.user.is_authenticated():
        car_id = request.GET.get('carid')
        try:
            car_ = Carinfo.objects.get(id=car_id)
            brand = str(car_.serbran) + car_.ctitle
            picture = car_.picture
            price = car_.extractprice
            newprice = car_.newprice
            mileage = car_.mileage
            Cart.objects.create(suser=request.user, car=car_, brand=brand, picture=picture, price=price, newprice=newprice, mileage=mileage)
        except ObjectDoesNotExist as e:
            logging.warning(e)
        return render(request, 'order.html', {'car':locals()})
    else:
        return redirect('/user/login/')


def confirmbuy(request):
    if request.user.is_authenticated():
        car_id = request.GET.get('carid')
        print(car_id)
        orderNo = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            car_ = Cart.objects.filter(car_id=car_id)
            car = Carinfo.objects.filter(id=car_id)
            # print(car[0].user)
            brand = car_[0].brand
            # print(brand)
            picture = car_[0].picture
            price = car_[0].price
            newprice = car_[0].newprice
            mileage = car_[0].mileage
            Orders.objects.create(sale_user=car[0].user, buy_user=request.user, brand=brand, picture=picture, price=price, newprice=newprice, mileage=mileage, orderNo=orderNo)
            Carinfo.objects.filter(id=car_id).update(isPurchase='True')
            # car[0].isPurchase == 'True'
        except ObjectDoesNotExist as e:
            logging.warning(e)
        # 最近浏览
        try:
            rec_view_list = list()
            if request.COOKIES.get('Recently_Viewed', None):
                rec_view = request.COOKIES.get('Recently_Viewed', None)
                list_view = rec_view.split(',')
                for i in list_view:
                    rec_view_list.append(Carinfo.objects.get(id=i))
            else:
                rec_view_list = []
        except ObjectDoesNotExist as e:
            logging.warning(e)

        user_id = request.user.id
        orders = Orders.objects.filter(buy_user=user_id).order_by("-id")[:4]
        user = UserInfo.objects.filter(id=user_id)[0]
        car = Carinfo.objects.filter(user_id=user_id, isPurchase=False)[:4]
        return render(request, 'user-info.html', {'orders': locals()})
    else:
        return redirect('/user/login/')

# 取消订单
def del_order(request):
    user_id = request.user.id
    car_id = request.GET.get('carid')
    try:
        Cart.objects.filter(suser_id=user_id, car_id=car_id).delete()
    except BaseException as e:
        logging.warning(e)
    return redirect('/')


# 买车列表
def buylist(request):
    carlist = Carinfo.objects.filter(isPurchase=False, isDelete=False)[:8]
    brandlist = Brand.objects.all().order_by('id')
    return render(request, 'list.html', {'carlist':locals()})


# 个人中心
def user_info(request):
    if request.user.is_authenticated():
        try:
            rec_view_list = list()
            if request.COOKIES.get('Recently_Viewed', None):
                rec_view = request.COOKIES.get('Recently_Viewed', None)
                list_view = rec_view.split(',')
                for i in list_view:
                    rec_view_list.append(Carinfo.objects.get(id=i))
            else:
                rec_view_list = []
        except ObjectDoesNotExist as e:
            logging.warning(e)

        user_id = request.user.id
        orders = Orders.objects.filter(buy_user=user_id).order_by("-id")[:4]
        user = UserInfo.objects.filter(id=user_id)[0]
        car = Carinfo.objects.filter(user_id=user_id, isDelete=False, isPurchase=False).order_by("-id")[:4]
        return render(request, 'user-info.html', {'orders': locals()})
    else:
        return redirect('/user/login/')


# 取消订单
def cancel_order(request):
    user_id = request.user.id
    car_id = request.GET.get('carid')
    try:
        Carinfo.objects.filter(user_id=user_id, id=car_id).update(isDelete=True)
    except ObjectDoesNotExist as e:
        logging.warning(e)
    return redirect('/buy/userinfo/')


# 重新出价
def reoffer(request):
    if request.method == 'POST':
        user_id = request.user.id
        car_id = request.POST.get('carid')
        alterprice = request.POST.get("alterprice")
        extractprice = int(alterprice) * 0.02 + int(alterprice)
    try:
        Carinfo.objects.filter(user_id=user_id, id=car_id).update(price=alterprice, extractprice=extractprice)
    except ObjectDoesNotExist as e:
        logging.warning(e)
    return redirect('/buy/userinfo/')


# 车辆品牌列表
def brandlist(request):
    brand = request.GET.get('brand')
    try:
        brand = Brand.objects.get(btitle=brand)
        carlist = brand.carinfo_set.filter(isPurchase=False, isDelete=False)
        brandlist = Brand.objects.all().order_by('id')
    except ObjectDoesNotExist as e:
        logging.warning(e)
    return render(request, 'list.html', {'carlist':locals()})


# 个人信息修改
def alter_info(requset):
    if requset.method == 'POST':
        realname = requset.POST.get("name")
        sex = requset.POST.get("sex")
        if sex == '男':
            sex = 0
        elif sex == '女':
            sex = 1
        phone = requset.POST["phone"]
        userid = requset.user.id
        UserInfo.objects.filter(id=userid).update(realname=realname, sex=sex, cellphone=phone)
        return redirect("/buy/userinfo/")





