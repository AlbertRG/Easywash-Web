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
from adminpages.models import ServicePage
from .helpers import send_forget_password_mail
import re
#2af
from django.contrib.auth.hashers import make_password
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.views.generic.base import RedirectView
from django.contrib import messages
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
  
  def get(self, request, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('home/index.html')
    return super().get(request, *args, **kwargs)


# Create your views here.
class LoginInterfaceView(LoginView):
  template_name = 'home/login.html'
  
def LoginInterface(request):
 if request.user.is_authenticated:
   return redirect('home')
 if request.method == 'POST':
   username=request.POST["username"]
   user_obj = User.objects.get(username = username)
   password=request.POST["password"]
   request.session["username"]=username
   request.session["password"]=password
   request.session["email"]=user_obj.email
   user = authenticate(request, username=username, password=password)
   if user is not None:
     send_otp(request)
     return render(request,'home/otp.html',{"email":user_obj.email})
   else:
     # Lógica personalizada para manejar credenciales incorrectas
     messages.error(request,"Nombre de usuario o contraseña incorrectos.")

 return render(request, 'home/login.html')
  
  
class HomeView(LoginRequiredMixin, TemplateView):
  template_name = 'home/index.html'
  login_url = 'loginaccount'
  #extra_context = {'today': datime.today()}

#class AuthorizedView(LoginRequiredMixin,TemplateView):
#  template_name = 'home/authorized.html'
#  login_url = '/admin'
def ChangePassword(request , token):
    print('Request:    ')
  
    if request.user.is_authenticated:
      return redirect('home')
    context = {}
    
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        if not profile_obj:
           return redirect('loginaccount')
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
                url_referer = request.META.get('HTTP_REFERER')
                return redirect(url_referer)
            
            user_obj = User.objects.get(id = user_id)
            if validar_contrasena(new_password,user_obj.username) is False:
              messages.success(request, 'Contrasena no cumple requerimientos')
              url_referer = request.META.get('HTTP_REFERER')
              return redirect(url_referer)

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
  
  #2af
  
def signin_verification(request):
  if User.is_authenticated:
      return redirect('home/index.html')
  if request.method=="POST":
    username=request.POST["username"]
    user_obj = User.objects.get(username = username)
    password=request.POST["password"]
    request.session["username"]=username
    request.session["password"]=password
    request.session["email"]=user_obj.email
    user = authenticate(request, username=username, password=password)
    if user is not None:
      send_otp(request)
      return render(request,'otp.html',{"email":user_obj.email})
    else:
      messages.info(request,"Credenciales incorrectas")
      return redirect("signin_verification")
          
          
def send_otp(request):
    s=""
    for x in range(0,6):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("Tu código de inicio de sesión de dos factores","Tu código de inicio de sesión de dos factores es "+s,'easywashgdl@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"home/otp.html")


def  otp_verification(request):
    if  request.method=='POST':
        otp_=request.POST.get("otp")
    if otp_ == request.session["otp"]:
        username = request.session['username']
        password = request.session['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)
        #User.is_active=True
        return redirect('home')
    else:
        messages.error(request,"El código no coincide")
        return render(request,'home/otp.html')
    

def validar_contrasena(contrasena, usuario):
    # Expresión regular para validar la contraseña
    patron = (
        r'^(?!.*' + re.escape(usuario) + r')'  # No se parece al usuario
        r'(?=.*\d)'  # Al menos un número
        r'(?=.*[A-Z])'  # Al menos una letra mayúscula
        r'(?=.*[@#%&*_+\[\]?\\|\-])'  # Al menos un carácter especial
        r'.{8,}$'  # Mínimo 8 caracteres
    )
    
    if re.match(patron, contrasena):
        return True
    else:
        return False
      
  #Inventario
@login_required  
def Servicio(request):
 # messages.success(request, 'Inventario listado')
  return render(request,'home/index.html')
  
@login_required  
def ServicioRegistrar(request):
    name = request.POST['txtNombre']
    last_name = request.POST['txtApellido']
    phone = request.POST['txtTelefono']
    service = request.POST['txtServicio']
    plate = request.POST['txtPlacas']
    total = request.POST['numTotal']

    if name == "" or last_name == "" or phone == "" or service == "" or plate == "" or total == "":
      messages.error(request, "Completa todos los campos")
      return redirect('home')
    
    if not validar_placa_mexicana(plate):
      messages.error(request, "Placa de carro no válida")
      return redirect('home') 


    
    if not validar_string(phone):
      messages.error(request, "Campo Total no es una entrada válida")
      return redirect('home') 
     
    try:
      parse_total = float(total)
    except Exception as e:
      messages.error(request, "Campo Total no es una entrada válida")
      print(e)
      return redirect('home')

    if not parse_total > 0:
      messages.error(request, "Cantidad debe de ser mayor o igual a 0")
      return redirect('home')
    
    
    if ServicePage.objects.filter(plate_code = plate).first():
      messages.error(request,"Placa ya registrada")
      return redirect('home')

    try:
      servicio = ServicePage.objects.create(
      first_name=name, last_name=last_name, phone=phone, type_service=service, plate_code=plate, price=total)
      messages.success(request, 'Servicio registrado!')
    except Exception as e:
      print(e)  
    return redirect('home')

def validar_string(string):
    # Elimina espacios en blanco y luego verifica si la longitud es 10 y si todos los caracteres son dígitos
    return len(string.strip()) == 10 and string.isdigit()

def validar_placa_mexicana(placa):
    # Define una expresión regular que coincida con el formato de placas de México
    patron = r'^[A-Z]{3}\d{3,4}$'
    
    # Usa re.match para verificar si la placa cumple con el patrón
    if re.match(patron, placa):
        return True
    else:
        return False
