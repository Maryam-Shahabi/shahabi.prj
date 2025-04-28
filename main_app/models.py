from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
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
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name="پایه")
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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="کتاب")
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
    PRODUCT_TYPE_CHOICES = [
        ('full', 'کل کتاب'),
        ('chapter', 'فصل خاص'),
        ('summary', 'جمع‌بندی'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="کتاب")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True, verbose_name="فصل")
    title = models.CharField(max_length=150, verbose_name="عنوان محصول")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت (تومان)")
    is_active = models.BooleanField(default=True, verbose_name="فعال؟")
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default='full', verbose_name="نوع محصول")
    description = models.TextField(blank=True, verbose_name="توضیحات محصول")
    image=models.ImageField(upload_to="photos",null=True,blank=True,verbose_name="تصویر محصول",)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.title} - {self.get_product_type_display()}"

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

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
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="محصول مرتبط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ویدئو"
        verbose_name_plural = "ویدئوها"
        ordering = ["created_at"]

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "نمونه سوال"
        verbose_name_plural = "نمونه سوالات"
        ordering = ["-created_at"]

# ==================== Blog Model ====================
class Blog(models.Model):  # مقاله
    title = models.CharField(max_length=100, verbose_name="عنوان مقاله")
    description = models.TextField(verbose_name="توضیحات مقاله", null=True, default="مقاله ریاضی")
    image = models.ImageField(upload_to="photos", null=True, blank=True, verbose_name="عکس مقاله")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-created_at"]
       
