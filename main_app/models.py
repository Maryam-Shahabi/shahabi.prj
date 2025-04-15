from django.db import models

# Create your models here.
class course(models.Model):
    course_title=models.CharField(max_length=30,unique=True)
    course_img=models.ImageField(upload_to="photo",null=True)
    course_descreption=models.CharField(max_length=500,blank=True,null=True)
    course_price=models.IntegerField(blank=True,null=True)
    course_discount_price=models.IntegerField(blank=True,null=True)
    course_teacher=models.CharField(max_length=50,null=True)
    course_level=models.CharField(max_length=50,help_text="سطح دوره را مشخص کنید",null=True)
    ch=[("1","در انتظار برگزاری"),("2","در حال برگزاری"),("3","به اتمام رسیده")]
    course_situation=models.CharField(max_length=50,choices=ch,null=True)
    course_number=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.course_title
class blog (models.Model):
    blog_title=models.CharField(max_length=30)
    blog_descreption=models.TextField()
    blog_img=models.ImageField(upload_to="photo",null=True)
    def __str__(self):
        return self.blog_title