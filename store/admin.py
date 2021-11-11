from django.contrib import admin

from .models import Category, Order, Product, Customer

class AdminProduct(admin.ModelAdmin):
    list_display=['id','title','description','category','stock','price','discount','image']
    
class AdminCategory(admin.ModelAdmin):
    list_display=['id','name','description','image']

class AdminSignup(admin.ModelAdmin):
    list_display=['id','first_name','last_name','phone','email','password']


class AdminOrder(admin.ModelAdmin):
    list_display=['id','product','customer','quantity','price','date']


# Register your models here.
admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customer,AdminSignup)
admin.site.register(Order,AdminOrder)