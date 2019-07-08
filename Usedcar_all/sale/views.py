from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import logging
from .models import *
from userinfo.models import *
import random

# Create your views here.

def protection(request):
    return render(request, 'protection.html')


# 首页展示
def index(request):
    brand = request.GET.get('brand')
    if brand == None:
        try:
            car_list = Carinfo.objects.filter(isPurchase=False, isDelete=False)
            car_five = random.sample(list(car_list), 5)
            brandlist = Brand.objects.all().order_by('id')

        except ObjectDoesNotExist as e:
            logging.warning(e)
    else:
        brand = Brand.objects.get(btitle=brand)
    return render(request, 'index.html', {'carlist':locals()})


# 详情页
def detail_one(request):
    car_id = request.GET.get("carid")
    try:
        carone = Carinfo.objects.filter(id=car_id)
    except ObjectDoesNotExist as e:
        logging.warning(e)

    if request.COOKIES.get('Recently_Viewed'):
        cookie_car = request.COOKIES.get('Recently_Viewed')
        list_car = cookie_car.split(',')
        if car_id in list_car:
            list_car.remove(car_id)
        if len(list_car) >= 2:
            list_car.pop()
        list_car = [car_id] + list_car
        cookie_car_new = ','.join(list_car)
    else:
        cookie_car_new = car_id

    # cookie处理数据添加的位置
    response = render(request, 'detail.html', {'carone':carone[0]})
    response.set_cookie('Recently_Viewed', cookie_car_new, max_age=3000)
    return response


def price0_10(request):
    brand = request.GET.get("brand")
    brandlist = Brand.objects.all().order_by('id')
    if brand == 'None':
        try:
            carlist = Carinfo.objects.filter(isPurchase=False, isDelete=False, extractprice__lt=10, extractprice__gt=0)
            brandlist = Brand.objects.all().order_by('id')
        except ObjectDoesNotExist as e:
            logging.warning(e)
    else:
        try:
            brand_id = Brand.objects.filter(btitle=brand)[0].id
            carlist = Carinfo.objects.filter(serbran_id=brand_id, isPurchase=False, isDelete=False, extractprice__lt=10, extractprice__gt=0)
        except ObjectDoesNotExist as e:
            logging.warning(e)
    return render(request, 'list.html', {'carlist':locals()})


def price10_30(request):
    brand = request.GET.get("brand")
    brandlist = Brand.objects.all().order_by('id')
    if brand == 'None':
        try:
            carlist = Carinfo.objects.filter(isPurchase=False, isDelete=False, extractprice__lt=30, extractprice__gt=10)
            brandlist = Brand.objects.all().order_by('id')
        except ObjectDoesNotExist as e:
            logging.warning(e)
    else:
        try:
            brand_id = Brand.objects.filter(btitle=brand)[0].id
            carlist = Carinfo.objects.filter(serbran_id=brand_id, isPurchase=False, isDelete=False, extractprice__lt=30,extractprice__gt=10)
        except ObjectDoesNotExist as e:
            logging.warning(e)
    return render(request, 'list.html', {'carlist':locals()})


def price30_80(request):
    brand = request.GET.get("brand")
    brandlist = Brand.objects.all().order_by('id')
    if brand == 'None':
        try:
            carlist = Carinfo.objects.filter(isPurchase=False, isDelete=False, extractprice__lt=80, extractprice__gt=30)
            brandlist = Brand.objects.all().order_by('id')
        except ObjectDoesNotExist as e:
            logging.warning(e)
    else:
        try:
            brand_id = Brand.objects.filter(btitle=brand)[0].id
            carlist = Carinfo.objects.filter(serbran_id=brand_id, isPurchase=False, isDelete=False, extractprice__lt=80,
                                             extractprice__gt=30)
        except ObjectDoesNotExist as e:
            logging.warning(e)
    return render(request, 'list.html', {'carlist': locals()})


def price80_(request):
    brand = request.GET.get("brand")
    brandlist = Brand.objects.all().order_by('id')
    if brand == 'None':
        try:
            carlist = Carinfo.objects.filter(isPurchase=False, isDelete=False, extractprice__gt=80)
            brandlist = Brand.objects.all().order_by('id')
        except ObjectDoesNotExist as e:
            logging.warning(e)
    else:
        try:
            brand_id = Brand.objects.filter(btitle=brand)[0].id
            carlist = Carinfo.objects.filter(serbran_id=brand_id, isPurchase=False, isDelete=False, extractprice__gt=80)
        except ObjectDoesNotExist as e:
            logging.warning(e)
    return render(request, 'list.html', {'carlist': locals()})


