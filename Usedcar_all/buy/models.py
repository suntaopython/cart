from django.db import models
from userinfo.models import UserInfo
from sale.models import Carinfo


# Create your models here.
ORDERSTATUS = (
        (1, "未出价",),
        (2, "已出价"),
        (3, "订单关闭"),
    )


class Cart(models.Model):
    suser = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='买家')
    car = models.ForeignKey(Carinfo, on_delete=models.CASCADE, verbose_name='车辆')
    brand = models.CharField(max_length=30, null=False, verbose_name='车辆信息')
    picture = models.ImageField(default='normal.png', verbose_name='照片')
    price = models.CharField(max_length=30, null=False, verbose_name='成交价格')
    newprice = models.CharField(max_length=30, null=False, verbose_name='新车价格')
    mileage = models.CharField(max_length=30, null=False, verbose_name='公里数')

    def __str__(self):
        return self.brand

    class Meta:
        db_table = 'Cart'
        verbose_name='购物表'
        verbose_name_plural = verbose_name


class Orders(models.Model):
    sale_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='suser', verbose_name='卖家')
    buy_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='buser', verbose_name='买家')
    brand = models.CharField(max_length=30, null=False, verbose_name='车辆信息')
    picture = models.ImageField(default='normal.png', verbose_name='照片')
    price = models.CharField(max_length=30, null=False, verbose_name='成交价格')
    newprice = models.CharField(max_length=30, null=False, verbose_name='新车价格')
    mileage = models.CharField(max_length=30, null=False, verbose_name='公里数')
    orderNo = models.CharField(max_length=30, null=False, verbose_name='订单号')
    orderStatus = models.IntegerField(blank=True, choices=ORDERSTATUS, default='1', verbose_name='订单状态')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.brand

    def get_orderStatusDisplay(self):
        if self.orderStatus == 1:
            return u'未出价'
        elif self.orderStatus == 2:
            return u'已出价'
        elif self.orderStatus == 3:
            return u'订单关闭'
        else:
            return u''

    class Meta:
        db_table = 'Orders'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name