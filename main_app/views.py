from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from .forms import UserUpdateForm, TicketForm, ContactForm, CourseFeedbackForm, TeacherContactForm, ForgetPasswordForm, PasswordResetForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

token_generator = PasswordResetTokenGenerator()



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
    product = Product.objects.get(id=adad)
    positive_feedbacks = product.feedbacks.filter(rating__gt=3)
    same_grade_products = Product.objects.filter(book__grade=product.book.grade).exclude(id=adad)
    if (request.method =="POST"):
        f = CourseFeedbackForm(request.POST)
        if f.is_valid():
            feedback = f.save(commit=False)
            feedback.product = product
            feedback.save()
            messages.success(request, "دیدگاه شما با موفقیت ثبت شد.")
            return redirect("course", adad=adad)
    else:
        f = CourseFeedbackForm()
    return render(request, "main_app/course.html",context={"c":c,"c1":c1,"ch":ch,
    "f": f,"positive_feedbacks":positive_feedbacks,"same_grade_products":same_grade_products})

def atricle(request,adad):
    c=Product.objects.all()
    bl=Blog.objects.all()
    ar=Blog.objects.filter(id=adad)
    return render(request, "main_app/article.html",context={"c":c,"ar":ar, "bl":bl})
   
def category(request):
    sort = request.GET.get('sort')
    type_filter = request.GET.get('type')
    c = Product.objects.all()
    
    if type_filter == 'free':
        c = c.filter(videos__is_free=True).distinct()
    elif type_filter == 'paid':
        c = c.exclude(videos__is_free=True).distinct()
    if sort == 'new':
        c = c.order_by('-id')
    elif sort == 'old':
        c = c.order_by('id')
    elif sort == 'active':
        c = c.filter(is_active='active')
    elif sort == 'inactive':
        c = c.filter(is_active='inactive')
    return render(request,"main_app/category.html",context={"c":c})



def contactus(request):
    c=Product.objects.all()
    f=ContactForm()
    if (request.method=="POST"):
        f=ContactForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد.")
            return redirect("/contactus/")
    return render(request,"main_app/contactus.html",context={"f":f,"c":c})


def signup(request):
    c=Product.objects.all()
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
         # اعتبارسنجی رمز عبور
        try:
            validate_password(pss1)
        except ValidationError as e:
            for error in e:
                error_text = str(error)
                if "This password is too short" in error_text:
                    messages.error(request, "رمز عبور خیلی کوتاه است. لطفاً حداقل ۸ کاراکتر وارد کنید.")
                elif "This password is too common" in error_text:
                    messages.error(request, "رمز عبور بسیار رایج است. لطفاً رمز قوی‌تری انتخاب کنید.")
                elif "This password is entirely numeric" in error_text:
                    messages.error(request, "رمز عبور نباید فقط شامل اعداد باشد.")
                else:
                    messages.error(request, error_text)  # پیام اصلی اگر چیزی جدید بود
            return render(request, "main_app/signup.html")    
        # ایجاد کاربر جدید
        CustomUser.objects.create_user(usr, eml, pss1, first_name=fname, last_name=lname, is_staff=False)
        return redirect("/login/") 
    return render(request, "main_app/signup.html",context={"c":c})

def login(request):
    c=Product.objects.all()
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
        return render(request, "main_app/login.html",context={"c":c})
        
def logout(request):
    auth_logout(request)
    return redirect("/login/")

@login_required
def addcart(request,pid):
    product=get_object_or_404(Product, id=pid)
    ord,created=Order.objects.get_or_create(user=request.user, status="cart")
    orditm,created=Orderitem.objects.get_or_create(order=ord, product=product)
    orditm.save()
    return redirect('/paneluser/')

@login_required
def deletecart(request,itmid):
    orderitm=get_object_or_404(Orderitem,id=itmid, order__user=request.user, order__status="cart")
    orderitm.delete()
    return redirect("/paneluser/")

@login_required
def paneluser(request):
    if request.user.role != "customer":
        return HttpResponse("شما اجازه دسترسی به این صفحه را ندارید.")
    c=Product.objects.all()
    ordercart=Order.objects.filter(user=request.user,status="cart")
    orders=ordercart.first()
    ordersfinal=Order.objects.filter(user=request.user,status="final")
    sm=0
    if orders:
        for itm in orders.items.all():
            price = itm.product.price
            if price is not None:
                sm += int(price)
    ordercart_count = sum([order.items.count() for order in ordercart]) 
    orderfinalcart_count = sum([order.items.count() for order in ordersfinal])       
    f=TicketForm()
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')  
    if (request.method == "POST"):
        if "send_ticket" in request.POST:
            f=TicketForm(request.POST)
            if f.is_valid():
                ticket=f.save(commit=False)
                ticket.user=request.user
                ticket.save()
                messages.success(request, "پیام شما با موفقیت ارسال شد.")
                return redirect("/paneluser/")
        elif "update_user" in request.POST:  
            uf = UserUpdateForm(request.POST, instance=request.user)
            if uf.is_valid():  
                uf.save()
                messages.success(request, "اطلاعات شما با موفقیت به‌روزرسانی شد.")  
                return redirect("/paneluser/")       
    return render(request, "main_app/paneluser.html",context={
        "c":c,
        "o":orders,
        "of":ordersfinal,
        "sm":sm,
        "f":f,
        "tickets":tickets,
        "ordercart_count": ordercart_count,
        "orderfinalcart_count":orderfinalcart_count})


@login_required
def dashboard(request):
    if (request.user.role=="seller"):
        products = Product.objects.all()
        videos = Video.objects.select_related("lesson", "product").all()
        orders = Order.objects.filter(status="final").select_related("user")
        users = CustomUser.objects.all()
        contacts = ContactModel.objects.all()
        total_products = products.count()
        total_videos = videos.count()
        total_orders = orders.count()
        total_users = users.count()
        total_contacts = contacts.count()
        stats = [
            {"label": "محصولات", "count": total_products, "icon": "main_app/images/product-icon.png"},
            {"label": "ویدیوها", "count": total_videos, "icon": "main_app/images/video-icon.png"},
            {"label": "سفارش‌ها", "count": total_orders, "icon": "main_app/images/order-icons.png"},
            {"label": "کاربران", "count": total_users, "icon": "main_app/images/user-icons.png"},
            {"label": "پیام‌ها", "count": total_contacts, "icon": "main_app/images/contact-icon.png"},
        ]
        return render(request, "main_app/dashboard.html",context={
            "products": products,
            "videos": videos,
            "orders": orders,
            "users": users,
            "contacts": contacts,
            "total_products": total_products,
            "total_videos": total_videos,
            "total_orders": total_orders,
            "total_users": total_users,
            "total_contacts": total_contacts,
            "stats": stats,
        }) 
    else:
        return redirect("/login/")    

    
def search(request):
    c=Product.objects.all()
    if(request.method=="GET"):
        s=request.GET.get("src")
        if(s):
            r=Product.objects.filter( Q(title__icontains=s) | Q(description__icontains=s))# جستجو بدون حساسیت به حروف بزرگ و کوچک
            return render(request,"main_app/search.html",context={"c":c,"r":r})
    return render(request, "main_app/search.html",context={"c":c})


def teach(request):
    c=Product.objects.all()
    f=TeacherContactForm()
    if (request.method == "POST"):
        f=TeacherContactForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد.")
            return redirect("/teach/")
    return render(request, "main_app/teach.html",context={"f":f,"c":c})


def forgetpassword(request):
    f=ForgetPasswordForm()
    if (request.method == "POST"):
        f = ForgetPasswordForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data['username']
            email = f.cleaned_data['email']
            try:
                user = CustomUser.objects.get(username=username, email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)

                reset_url = request.build_absolute_uri(
                    reverse('passwordreset', kwargs={'uidb64': uid, 'token': token})
                )

                send_mail(
                    subject="بازیابی رمز عبور",
                    message=f"برای تغییر رمز عبور خود، روی لینک زیر کلیک کنید:\n{reset_url}",
                    from_email='noreply@example.com',
                    recipient_list=[email],
                )
                messages.success(request, "ایمیل ارسال شد.")
                return redirect("/forgetpassword/")
            except CustomUser.DoesNotExist:
                messages.error(request,"کاربری با این مشخصات یافت نشد.")
    else:
        f = ForgetPasswordForm()
    return render(request, "main_app/forgetpassword.html",context={"f": f})


def passwordreset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (CustomUser.DoesNotExist, ValueError):
        user = None

    if user and token_generator.check_token(user, token):
        if request.method == 'POST':
            f = PasswordResetForm(request.POST)
            if f.is_valid():
                newpassword1 = f.cleaned_data['newpassword1']
                newpassword2 = f.cleaned_data['newpassword2']

                if newpassword1 != newpassword2:
                    messages.error(request," رمزهای عبور یکسان نیست.")
                    return render(request, "main_app/passwordreset.html", context={"f": f})

                try:
                    validate_password(newpassword1, user=user)
                except ValidationError as e:
                    for error in e:
                        error_text = str(error)
                        if "This password is too short" in error_text:
                            messages.error(request, "رمز عبور خیلی کوتاه است. لطفاً حداقل ۸ کاراکتر وارد کنید.")
                        elif "This password is too common" in error_text:
                            messages.error(request, "رمز عبور بسیار رایج است. لطفاً رمز قوی‌تری انتخاب کنید.")
                        elif "This password is entirely numeric" in error_text:
                            messages.error(request, "رمز عبور نباید فقط شامل اعداد باشد.")
                        else:
                            messages.error(request, error_text)
                    return render(request, "main_app/passwordreset.html", context={"f": f})

                # اگر همه‌چیز اوکی بود:
                user.set_password(newpassword1)
                user.save()
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
                return redirect("/login/")
        else:
            f = PasswordResetForm()

        return render(request, "main_app/passwordreset.html", context={"f": f})

    # توکن نامعتبر یا کاربر پیدا نشد
    return render(request, "main_app/passwordreset.html", context={"f": PasswordResetForm(), "invalid_token": True})

def samplequestion(request):
    c=Product.objects.all()
    books = Book.objects.prefetch_related('samplequestion_set', 'grade').all()
    return render(request, "main_app/samplequestion.html", {'books': books,"c":c})
