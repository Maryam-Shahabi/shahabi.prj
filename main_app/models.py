from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
# ==================== Grade Model ====================
class Grade(models.Model):  # پایه
    name = models.CharField(max_length=30, verbose_name="پایه")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "پایه"
        verbose_name_plural = "پایه‌ها"
        ordering = ["id"]

# ==================== Book Model ====================
class Book(models.Model):  # کتاب
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name="پایه",related_name="books")
    title = models.CharField(max_length=100, verbose_name="نام کتاب")
    description = models.TextField(max_length=500, verbose_name="توضیحات کتاب",null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"
        ordering = ["title"]

# ==================== Chapter Model ====================
class Chapter(models.Model):  # فصل
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="کتاب", related_name="chapters")
    title = models.CharField(max_length=100, verbose_name="عنوان فصل")
    order = models.PositiveIntegerField(verbose_name="ترتیب فصل")

    def __str__(self):
        return f"فصل {self.order}: {self.title} ({self.book.title})"

    class Meta:
        verbose_name = "فصل"
        verbose_name_plural = "فصل‌ها"
        ordering = ["book"]

# ==================== Lesson Model ====================
class Lesson(models.Model):  # درس
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name="فصل",null=True)
    title = models.CharField(max_length=100, verbose_name="عنوان درس")
    order = models.PositiveIntegerField(verbose_name="ترتیب درس")

    def __str__(self):
        return f"درس {self.order}: {self.title} ({self.chapter})"

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"
        ordering = ["order"]

# ==================== Product Model ====================
class Product(models.Model):  # محصول
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="کتاب")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True, verbose_name="فصل")
    title = models.CharField(max_length=150, verbose_name="عنوان محصول")
    teacher=models.CharField(max_length=150, verbose_name="مدرس",null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت (تومان)", null=True)
    discount_price=models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت  با تخفیف (تومان)", null=True, blank=True)
    cho=[("active","فعال"),("inactive","غیرفعال")]
    is_active = models.CharField(max_length=10, choices=cho, default="active", verbose_name="وضعیت دوره")
    choi=[("full","کل کتاب"),("part","یک فصل کتاب"),("summary","جمع بندی")]
    product_type = models.CharField(max_length=10, choices=choi, default="full", verbose_name="نوع محصول")
    description = models.TextField(blank=True, verbose_name="توضیحات محصول")
    image=models.ImageField(upload_to="photos",null=True,blank=True,verbose_name="تصویر محصول")

    def __str__(self):
        return f"{self.title} - {self.get_product_type_display()}"

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["title"]

# ==================== Video Model ====================
class Video(models.Model):  # ویدئو
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name="درس مربوطه")
    title = models.CharField(max_length=150, verbose_name="عنوان ویدئو")
    video_file = models.FileField(
        upload_to="videos",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "mov", "avi"])],
        verbose_name="فایل ویدئو"
    )
    purchase_link = models.URLField(blank=True, null=True, verbose_name="لینک خرید (اسپات پلیر)")
    is_free = models.BooleanField(default=False, verbose_name="رایگان است؟")
    description = models.TextField(blank=True, verbose_name="توضیحات ویدئو")
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="محصول مرتبط", related_name="videos")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ویدئو"
        verbose_name_plural = "ویدئوها"
        ordering = ["title"]

# ==================== SampleQuestion Model ====================
class SampleQuestion(models.Model):  # نمونه سوال
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="کتاب")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True, verbose_name="فصل")
    title = models.CharField(max_length=150, verbose_name="عنوان سوال")
    file = models.FileField(
        upload_to="sample_questions",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        verbose_name="فایل سوال"
    )
    is_full_book = models.BooleanField(default=False, verbose_name="برای کل کتاب است؟")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "نمونه سوال"
        verbose_name_plural = "نمونه سوالات"

# ==================== Blog Model ====================
class Blog(models.Model):  # مقاله
    title = models.CharField(max_length=100, verbose_name="عنوان مقاله")
    description = RichTextField(verbose_name="توضیحات مقاله", null=True, default="مقاله ریاضی")
    image = models.ImageField(upload_to="photos", null=True, blank=True, verbose_name="عکس مقاله")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-created_at"]

# =================== Contact Model ===================
class ContactModel(models.Model):
    fname=models.CharField(max_length=20, verbose_name="نام")
    lname=models.CharField(max_length=20, verbose_name="نام خانوادگی")
    email=models.EmailField(verbose_name="ایمیل")
    message=models.CharField(max_length=500, verbose_name="متن پیام")     

    def __str__(self):
        return self.fname
    
    class Meta:
        verbose_name="نامه"
        verbose_name_plural="نامه ها"
#===================== Tickets Model ====================
class Ticket(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True, verbose_name="کاربر")
    subject = models.CharField(max_length=30, verbose_name=" عنوان تیکت")  
    message = models.CharField(max_length=500, verbose_name="متن تیکت")    
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد") 

    def __str__(self):
        return  f"{self.user} - {self.subject}"
    
    class Meta:
        verbose_name="تیکت"
        verbose_name_plural="تیکت ها"
        
#===================== Course Feedback ==================
class CourseFeedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول",related_name="feedbacks")
    name = models.CharField(max_length=50, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="متن دیدگاه")
    rating = models.PositiveSmallIntegerField(verbose_name="امتیاز", null=True, blank=True, choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.name} - {self.product.title}"

    class Meta:
        verbose_name = "نظرسنجی دوره"
        verbose_name_plural = "نظرسنجی دوره‌ها"

#===================== Teacher Contact Model =============================================
class TeacherContact(models.Model):
    cht=(("1","تدریس ریاضیات متوسطه اول"),("2","تدریس ریاضیات متوسطه دوم"))
    fname = models.CharField(max_length=20, verbose_name="نام")
    lname = models.CharField(max_length=20, verbose_name="نام خانوادگی")
    phone = models.CharField(max_length=11,verbose_name="شماره تماس")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=50,verbose_name="عنوان آموزش")
    options = models.CharField(max_length=30, verbose_name="دسته بندی", choices=cht, default="1")
    link = models.URLField(blank=True,null=True, verbose_name="لینک نمونه")
    description = models.CharField(max_length=500,verbose_name="توضیحات")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = " مدرس"
        verbose_name_plural = "مدرسان "

# ==================== Users Model ========================================================
class CustomUser(AbstractUser):#کاربران
    roleitem=(("seller","فروشنده"),("customer","مشتری"))
    role=models.CharField(max_length=20, choices=roleitem, default="customer")

    class Meta:
        verbose_name="کاربر"
        verbose_name_plural="کاربران"

#===================== Order Model =====================================================
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="orders", verbose_name="کاربر")
    statusitems=(("cart","سبدخرید"),("final","سفارش نهایی"))
    status=models.CharField(max_length=20, choices=statusitems,default="cart")
    tracking_code=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ خرید")

    def __str__(self):
        return f"{self.tracking_code} - {self.status}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ['-created_at']
#====================================== Orderitem Model ==========================================
class Orderitem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items",verbose_name="سفارش")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="محصول")  

    def __str__(self):
        return str(self.order)
    
    class Meta:
        verbose_name = "ریز سفارش"
        verbose_name_plural = "ریز سفارش ها"
        ordering = ['order']