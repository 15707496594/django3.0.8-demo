from django.db import models
from django.contrib.auth.models import User


class Demo(models.Model):
    """
    模型类
    """
    # char类型字段
    name = models.CharField(max_length=100, blank=True, default='')
    # 布尔型字段
    active = models.BooleanField(default=True)
    # 时间类型字段
    created_time = models.DateTimeField(auto_now_add=True)

    # 内部类，用于定义一些Django模型类的行为特性
    class Meta:
        # 这个字段是告诉Django模型对象返回的记录结果集是按照哪个字段排序的。这是一个字符串的元组或列表，没有一个字符串都是一个字段和用一个可选的表明降序的'-'构成。当字段名前面没有'-'时，将默认使用升序排列。使用'?'将会随机排列
        #     ordering=['order_date'] # 按订单升序排列
        #     ordering=['-order_date'] # 按订单降序排列，-表示降序
        #     ordering=['?order_date'] # 随机排序，？表示随机
        #     ordering=['-pub_date','author'] # 以pub_date为降序，在以author升序排列
        ordering = ('-created_time', )

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    # 生成token时客户端的ip地址
    address = models.CharField(max_length=20)

class SaleOrder(models.Model):

    # 单号
    name = models.CharField(max_length=20,)
