from django.contrib import admin
from .models import Grade, Book, Chapter, Lesson,Product, Video, SampleQuestion, Blog, CustomUser, ContactModel, CourseFeedback, TeacherContact, Order, Orderitem, Ticket
# Register your models here.
admin.site.register(Grade)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Product)
admin.site.register(Video)
admin.site.register(SampleQuestion)
admin.site.register(Blog)
admin.site.register(CustomUser)
admin.site.register(ContactModel)
admin.site.register(CourseFeedback)
admin.site.register(TeacherContact)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Ticket)