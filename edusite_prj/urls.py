"""
URL configuration for edusite_prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from main_app.views import home,signup, course,blog,atricle,category,contactus,paneluser,search,teach,login,logout,layout,dashboard,forgetpassword,passwordreset,addcart,deletecart,samplequestion
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("layout/", layout),
    path("", home),
    path("course/<adad>", course ,name="course"),
    path("blog/", blog , name="blog"),
    path("article/<adad>", atricle , name="atricle"),
    path("login/",login, name="login"),  
    path("logout/",logout, name="logout"), 
    path("category/", category , name="category"),
    path("contactus/", contactus , name="contactus"),
    path("signup/", signup, name="signup"),
    path("paneluser/",paneluser, name="paneluser"),
    path("dashboard/",dashboard, name="dashboard"),
    path("search/",search , name="search"), 
    path("teach/",teach , name="teach"),
    path("forgetpassword/", forgetpassword, name="forgetpassword"),
    path("passwordreset/<uidb64>/<token>/", passwordreset, name="passwordreset"),
    path("addcart/<pid>",addcart , name="addcart"),
    path("deletecart/<itmid>", deletecart, name="deletecart"),
     path("samplequestion/", samplequestion , name="samplequestion")

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
