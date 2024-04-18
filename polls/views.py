from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistrantionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url= '/login')
def add_blogs(request):
    if request.method == "POST":
        form = BlogPostForm(data = request.POST, files = request.FILES)
        if form.is_valid():
            blogpost = form.save(commit = False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "polls/add_blog.html", {'obj': obj, 'alert': alert})
        else:
            form = BlogPostForm()
        return render(request, "polls/add_blog.html", {'form': form})

def home(request):
    context = {}
    return render(request, 'polls/home.html', context)

def Cart(request):
    context = {}
    return render(request, 'polls/cart.html', context)

def Checkout(request):
    context = {}
    return render(request, 'polls/checkout.html', context)

def Register(request):
    form = RegistrantionForm()
    if request.method == 'POST':
        form = RegistrantionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'polls/register.html', {'form': form})

def Login(request):
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
