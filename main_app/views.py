from django.shortcuts import render, HttpResponse , redirect
from .models import *
from django.contrib import messages 
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def layout(request):
    c=Product.objects.all()
    return render(request,"main_app/layout.html",context={"c":c})

def home(request):
    c=Product.objects.all()
    bl=Blog.objects.all()
    return render(request,"main_app/index.html",context={"c":c,"bl":bl})

def blog(request):
    c=Product.objects.all()  
    bl=Blog.objects.all()
    if (request.method=="POST"):
        s=request.POST.get("srch")
        if(s):
            r=Blog.objects.filter(title__contains=s)
            return render(request,"main_app/blog.html",context={"c":c,"r":r})
    return render(request,"main_app/blog.html",context={"c":c,"bl":bl})

def course(request,adad):
    c=Product.objects.all()
    c1=Product.objects.filter(id=adad)
    ch =Chapter.objects.all()
    return render(request, "main_app/course.html",context={"c":c,"c1":c1,"ch":ch})

def atricle(request,adad):
    c=Product.objects.all()
    bl=Blog.objects.all()
    ar=Blog.objects.filter(id=adad)
    return render(request, "main_app/article.html",context={"c":c,"ar":ar, "bl":bl})
   
def category(request):
    return render(request,"main_app/category.html")

def contact_us(request):
    return render(request,"main_app/contact_us.html")

def news(request):
    return render(request, "main_app/news.html")

def signup(request):
    if (request.method=="POST"):
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        eml=request.POST.get("eml")
        usr=request.POST.get("usr")
        pss1=request.POST.get("pss1")
        pss2=request.POST.get("pss2")
        # بررسی یکسان بودن رمزهای عبور وارد شده
        if (pss1 != pss2):
            messages.error(request, "رمزهای عبور یکسان نیستند.")
            return render(request, "main_app/signup.html")
        # بررسی تکراری نبودن نام کاربری    
        if CustomUser.objects.filter(username=usr).exists():
            messages.error(request, "نام کاربری قبلا ثبت شده است. لطفا نام کاربری دیگری انتخاب کنید.")
            return render(request, "main_app/signup.html")
        # ایجاد کاربر جدید
        CustomUser.objects.create_user(usr, eml, pss1, first_name=fname, last_name=lname, is_staff=False)
        return redirect("/login/") 
    return render(request, "main_app/signup.html")


def login(request):
    if(request.method=="POST"):
        usr=request.POST.get("usr")
        pss1=request.POST.get("pss1")
        u=authenticate(username=usr, password=pss1)
        if u is not None:
            auth_login(request, u)
            if (u.role=="seller"):
                return redirect("/dashboard")
            else:    
                return redirect("/paneluser")
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
            return render(request, "main_app/login.html")    
    else:     
        return render(request, "main_app/login.html")
        
def logout(request):
    auth_logout(request)
    return redirect("/login/")


@login_required
def paneluser(request):
    return render(request, "main_app/paneluser.html")

@login_required
def dashboard(request):
    if (request.user.role=="seller"):
        return render(request, "main_app/dashboard.html") 
    else:
        return redirect("/login/")    

    
def search(request):
    c=Product.objects.all()
    if(request.method=="POST"):
        s=request.POST.get("src")
        if(s):
            r=Product.objects.filter(title__contains=s)
            return render(request,"main_app/search.html",context={"c":c,"r":r})
    return render(request, "main_app/search.html",context={"c":c})


def teach(request):
    return render(request, "main_app/teach.html")

def error404(request):
    return render(request, "main_app/error404.html")
