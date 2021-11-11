from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse, request

from store.middleware.auth import auth_middleware
from .models import Category, Customer, Order, Product
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        minuscart = request.POST.get('minuscart')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if minuscart:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        # print(request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        products = None
        # request.session.get('cart').clear()
        categories = Category.get_all_categories()
        categoryid = request.GET.get('category')
        if categoryid:
            products = Product.get_products_by_id(categoryid)
        else:
            products = Product.get_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'index.html', data)


class OrderView(View):

    def get(self, request):
        customer = request.session.get('customer') 
        orders = Order.get_orders_by_customer_id(customer)
        print(orders)
        return render(request, 'order.html', {'orders':orders})


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        pro = Product.get_products_by_id_in_cart(ids)
        return render(request, 'cart.html',{'products':pro})

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id_in_cart(list(cart.keys()))
        # print(address,phone,customer, cart ,products)
        


        for product in products:
            order = Order(customer = Customer(id = customer),product = Product(id = product.id),price = product.price,address = address,phone = phone,quantity = cart.get(str(product.id)))
            order.placeorder(order)

        request.session['cart'] = {}
            
        
        return redirect('cart')

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postdata = request.POST
        first_name = postdata.get('firstname')
        last_name = postdata.get('lastname')
        phone = postdata.get('phone')
        email = postdata.get('email')
        password = postdata.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password': password
        }
        customer = Customer(first_name=first_name, last_name=last_name,
                            phone=phone, email=email, password=password)

        error_msg = self.ValidateCustomer(customer)

        if not error_msg:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_msg,
                'values': value

            }
            return render(request, 'signup.html', data)

    def ValidateCustomer(self, customer):
        error_msg = None

        if not customer.first_name:
            error_msg = "FirstName Required!"
        elif not customer.last_name:
            error_msg = "LastName Required!"
        elif not customer.phone:
            error_msg = "Phone Number Required!"
        elif len(customer.phone) > 15:
            error_msg = "Phone length must be less than 15"
        elif not customer.email:
            error_msg = "Email Required!"
        elif not customer.password:
            error_msg = "Password Required!"
        elif len(customer.password) < 8:
            error_msg = "Password must be 8 or greater"
        elif customer.isExists():
            error_msg = "Email already exists"

        return error_msg


class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_msg = None
        if customer:
            flag = check_password(password, customer.password)
            print(flag)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_msg = "Email or Password Invalid!"
        else:
            error_msg = "Email  Password Invalid!"

        return render(request, 'login.html', {'error': error_msg})


def logout(request):
    request.session.clear()
    return redirect('homepage')