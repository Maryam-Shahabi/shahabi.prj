from django.shortcuts import render, HttpResponse
from .models import *
# Create your views here.
def layout(response):
    c=Product.objects.all()
    return render(response,"main_app/layout.html",context={"c":c})

def home(response):
    c=Product.objects.all()
    bl=Blog.objects.all()
    return render(response,"main_app/index.html",context={"c":c,"bl":bl})

def blog(response):
    c=Product.objects.all()
    bl=Blog.objects.all()
    return render(response,"main_app/blog.html",context={"c":c,"bl":bl})

def course(response,adad):
    c=Product.objects.all()
    c1=Product.objects.filter(id=adad)
    ch =Chapter.objects.all()
    return render(response, "main_app/course.html",context={"c":c,"c1":c1,"ch":ch})

def atricle(response,adad):
    c=Product.objects.all()
    bl=Blog.objects.all()
    ar=Blog.objects.filter(id=adad)
    return render(response, "main_app/article.html",context={"c":c,"ar":ar, "bl":bl})

def login(response):
    fname=""
    if (response.GET.get("fname")!=None):
        fname=response.GET.get("fname")+ " Welcom to my site "
    return render(response, "main_app/login.html",context={"fname":fname})

def category(response):
    return render(response,"main_app/category.html")
def contact_us(response):
    return render(response,"main_app/contact_us.html")
def news(response):
    return render(response, "main_app/news.html")
def sign_up(response):
    return render(response, "main_app/sign_up.html")
def panel_user(response):
    return render(response, "main_app/panel_user.html")
def search(response):
    return render(response, "main_app/search.html")
def teach(response):
    return render(response, "main_app/teach.html")
def error404(response):
    return render(response, "main_app/error404.html")
def login(response):
    return render(response, "main_app/login.html")