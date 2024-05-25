import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import RegistrantionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

@login_required(login_url= '/login')
def add_blogs(request):
    if request.method == "POST":
        form = Post(data = request.POST, files = request.FILES)
        if form.is_valid():
            blogpost = form.save(commit = False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "polls/add_blog.html", {'obj': obj, 'alert': alert})
        else:
            form = Post()
        return render(request, "polls/add_blog.html", {'form': form})

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems}
    return render(request, 'polls/home.html', context)

def Cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order , created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order': order,'cartItems':cartItems}
    return render(request, 'polls/cart.html', context)

def Detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order , created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    id = request.GET.get('id','')
    products = Product.objects.filter(id = id)
    context = {'items':items, 'order': order,'cartItems':cartItems,'products':products}
    return render(request, 'polls/detail.html', context)

def Checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'polls/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('added', safe=False)

def Register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
    return render(request, 'polls/register.html', {'form': form})

def LoginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully login")
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, "polls/login.html")
    return render(request, "polls/login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logout")
    return HttpResponseRedirect('/login')

def Search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    return render(request, "polls/search.html", {"searched":searched,"keys":keys,'products': products, 'cartItems': cartItems})