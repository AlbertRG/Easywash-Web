from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required # for functions
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin #for classes
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .helpers import send_forget_password_mail

class SignupView(CreateView):
  form_class = UserCreationForm
  template_name = 'home/register.html'
  #success_url = '/smart/notes'
  
  def get(self, request, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('home/index.html')
    return super().get(request, *args, **kwargs)


class LogoutInterfaceView(LogoutView):
  template_name = 'home/logout.html'


# Create your views here.
class LoginInterfaceView(LoginView):
  template_name = 'home/login.html'
  
  
class HomeView(LoginRequiredMixin, TemplateView):
  template_name = 'home/index.html'
  login_url = 'login'
  #extra_context = {'today': datetime.today()}

#class AuthorizedView(LoginRequiredMixin,TemplateView):
#  template_name = 'home/authorized.html'
#  login_url = '/admin'
def ChangePassword(request , token):
    context = {}
    
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'home/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'home/change-password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('home')  
        
    except Exception as e:
        print(e)
    return render(request , 'home/change-password.html' , context)



import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('forget-password')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('forget-password')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'home/forget-password.html')
  
def Register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('home/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('home/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
    
            profile_obj = Profile.objects.create(user = user_obj )
            profile_obj.save()
            return redirect('home/login')

        except Exception as e:
            print(e)

    except Exception as e:
            print(e)

    return render(request , 'home/register.html')