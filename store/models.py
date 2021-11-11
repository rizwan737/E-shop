from django.db import models
from django.db.models.aggregates import Max
from django.db.models.deletion import CASCADE
from django.utils.translation import deactivate
import datetime
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/category/')
    

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all() 


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='category', on_delete=CASCADE,default=1)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.0,max_digits=6,decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.title


    @staticmethod
    def get_products_by_id_in_cart(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_products():
        return Product.objects.all() 

    @staticmethod
    def get_products_by_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_products()

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    def __str__(self):
        return self.first_name

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False



    def isExists(self):
        try:
            if Customer.objects.get(email = self.email):
                return True
        except:
            return False


class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=CASCADE)
    customer = models.ForeignKey(Customer, related_name='customer', on_delete=CASCADE,default=1)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=50,default='',blank=True)
    phone = models.CharField(max_length=50,default='',blank=True)
    price = models.IntegerField(max_length=50)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)


    @staticmethod
    def placeorder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer_id(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')