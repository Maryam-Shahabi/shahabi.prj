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
from main_app.views import home,news,signup, course,blog,atricle,category,contact_us,paneluser,search,teach,error404,login,logout,layout,dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("layout/", layout),
    path("", home),
    path("course/<adad>", course),
    path("blog/", blog),
    path("article/<adad>", atricle),
    path("login/",login, name="login"),  
    path("logout/",logout, name="logout"), 
    path("category/", category),
    path("contact_us/", contact_us),
    path("news/", news),
    path("signup/", signup, name="signup"),
    path("paneluser/",paneluser, name="paneluser"),
    path("dashboard/",dashboard, name="dashboard"),
    path("search/",search), 
    path("teach/",teach),
    path("error404/",error404),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
