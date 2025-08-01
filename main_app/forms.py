
# forms.py
from django import forms
from .models import CourseFeedback, ContactModel, TeacherContact, Ticket,CustomUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
CustomUser=get_user_model()

#============================ فرم مدلی پرسش و پاسخ دوره ها ================================
class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['name', 'email', 'message', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'نام خود را وارد کنید ...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'ایمیل خود را وارد کنید ...'}),
            'message': forms.Textarea(attrs={'class': 'form-control w-100 rounded-lg p-3', 'placeholder': 'دیدگاه خود را وارد کنید ...', 'rows': 5}),
            'rating': forms.HiddenInput()  # مقدار ستاره از JS تنظیم می‌شود
        }
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise forms.ValidationError("لطفاً امتیاز خود را وارد کنید.")
        return rating
#=============================== فرم مدلی ارتباط با ما =====================================
class ContactForm(forms.ModelForm): 
    class Meta:
        model=ContactModel
        fields=['fname','lname','email','message']
        widgets={
            'fname':forms.TextInput(attrs={'class': 'form-control rounded-pill','placeholder': 'نام خود را وارد کنید ...'}),
            'lname':forms.TextInput(attrs={'class': 'form-control rounded-pill','placeholder': 'نام خانوادگی خود را وارد کنید ...'}),
            'email':forms.EmailInput(attrs={'class': 'form-control rounded-pill','placeholder': 'ایمیل خود را وارد کنید ...'}),
            'message':forms.Textarea(attrs={'class': 'form-control w-100 rounded-lg p-3','placeholder': 'پیام خود را وارد کنید ...','rows': 10})
        }
#==================================== فرم مدلی تیکت  ===========================================
class TicketForm(forms.ModelForm):  
    class Meta:
        model=Ticket
        fields=["subject","message"]
        widgets={
            'subject': forms.TextInput(attrs={'class': 'form-control rounded-pill'  ,'placeholder':'عنوان مورد نظر خود را وارد کنید...'}),
            'message': forms.Textarea(attrs={'class': 'form-control w-100 rounded-lg p-3','placeholder': 'پیام خود را وارد کنید...','rows': 10})
        }   
#==================================== فرم مدلی مدرسان ==========================================
class TeacherContactForm(forms.ModelForm):
    class Meta:
        model=TeacherContact
        fields=['fname','lname','phone','email','subject','options','link','description']
        widgets={
            'fname':forms.TextInput(attrs={'class': 'form-control rounded-pill' ,'placeholder':'نام خود را وارد کنید...'}),
            'lname':forms.TextInput(attrs={'class': 'form-control rounded-pill'  ,'placeholder':'نام خانوادگی خود را وارد کنید...'}),
            'phone':forms.TextInput(attrs={'class': 'form-control rounded-pill'  ,'placeholder':'شماره تماس خود را وارد کنید...'}),
            'email':forms.EmailInput(attrs={'class': 'form-control rounded-pill'  ,'placeholder':'ایمیل خود را وارد کنید...'}),
            'subject':forms.TextInput(attrs={'class': 'form-control rounded-pill'  ,'placeholder':'عنوان آموزش خود را وارد کنید...'}),
            'options':forms.Select(attrs={'class': 'form-control rounded-pill font-13'  ,'placeholder':''}),
            'link':forms.URLInput(attrs={'class': 'form-control rounded-pill' ,'placeholder':'لینک نمونه تدریس خود را وارد کنید...'}),
            'description':forms.Textarea(attrs={'class': 'form-control w-100 rounded-lg p-3'  ,'placeholder':'توضیحاتی مختصر درباره مطالبی که در این آموزش ارائه خواهید کرد...','rows': 5}),
        }
#==================================== فرم سفارشی فراموشی رمز عبور ============================
class ForgetPasswordForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control rounded-pill' ,'placeholder':'نام کاربری خود را وارد کنید...'}))
    email = forms.EmailField(max_length=50,widget=forms.EmailInput(attrs={'class': 'form-control rounded-pill' ,'placeholder':'ایمیل خود را وارد کنید...'}))     

class PasswordResetForm(forms.Form):
    newpassword1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'رمز عبور جدید را وارد کنید'}))  
    newpassword2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'رمز عبور جدید را دوباره وارد کنید'})) 
#=================================== فرم مدلی آپدیت اطلاعات کاربر ================================
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']  
