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


class Person(models.Model):
    """ 这个模型在Django中相当于执行了如下建表语句
    CREATE TABLE myapp_person (
        "id" serial NOT NULL PRIMARY KEY,
        "first_name" varchar(30) NOT NULL,
        "last_name" varchar(30) NOT NULL
    );
    # ==========================自定义表名================================
    该表的名称 myapp_person 是自动从某些模型元数据中派生出来，但可以被改写
    在类中的class Meta下增加db_table属性，例如：db_table = 'july_person'
    # ==========================自动设置主键==============================
    默认情况下， Django 会给每一个模型添加下面的字段：
    id = models.AutoField(primary_key=True)
    这是一个自增的主键。
    如果你想自己指定主键， 在你想要设置为主键的字段上设置参数 primary_key=True。
    如果 Django 看到你显式地设置了 Field.primary_key，将不会自动在表（模型）中添加 id 列。
    每个模型都需要拥有一个设置了 primary_key=True 的字段（无论是显式的设置还是 Django 自动设置）。

    """
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large')
    )
    person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    shirt_sizes = models.CharField(max_length=1, choices=SHIRT_SIZES)


    class Meta:
        db_table = 'july_person'


class Musician(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    instrument = models.CharField(max_length=100)


class Album(models.Model):

    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
