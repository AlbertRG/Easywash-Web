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
