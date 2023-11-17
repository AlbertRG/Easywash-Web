from django.shortcuts import render
from django.utils import timezone
import pytz
from cryptography.fernet import Fernet
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required # for functions
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin #for classes
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
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

def eliminarCuenta(request):
  return render(request, 'home/eliminar-cuenta.html')

def terminosCondiciones(request):
  return render(request, 'home/terminos-condiciones.html')

   




#Editar cuenta
@login_required
def editar_cuenta(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        password = request.POST.get('password')

        # Verificar la contraseña del usuario actual
        user = authenticate(username=request.user.username, password=password)

        if user is not None:
            # La contraseña es válida, actualiza los datos de la cuenta
            request.user.username = new_username
            request.user.email = new_email
            request.user.save()

            messages.success(request, 'Los cambios se han guardado correctamente.')
            return redirect('editar-cuenta')  # Redirecciona a la misma página después de guardar los cambios.
        else:
            messages.error(request, 'Contraseña incorrecta. Los cambios no se han guardado.')

    return render(request, 'home/change_data_account.html')


def LogOut(request):
   logout(request)
   return redirect('home')


def LoginInterface(request):
  print("HOLAAAAAAAAAAAAAAAAAA")
  request.session.flush()
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
      request.session.flush()
      # Lógica personalizada para manejar credenciales incorrectas
      messages.error(request,"Nombre de usuario o contraseña incorrectos.")
  if request.user.is_authenticated:
    print("if User.is_authenticated:")
    return redirect('home')
  return render(request, 'registration/login.html')
  

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
                messages.success(request, 'Usuario no encontrado')
                return redirect(f'home/change-password/{token}/')
                
            #Tiempo de 5 min
            now = datetime.now(timezone.utc)
            # Calcula la fecha y hora 5 minutos adelante desde la crecion del token
            tokenDate = profile_obj.created_at + timedelta(minutes=5)
            print(now)
            print(profile_obj.created_at)
            print(tokenDate)

            
            if now > tokenDate:
              messages.success(request, 'Tiempo expirado, vuelva a solicitar cambio de contraseña')
              url_referer = request.META.get('HTTP_REFERER')
              return redirect('home')  

            
            if  new_password != confirm_password:
                messages.success(request, 'Ambas contraseñas deben ser iguales')
                url_referer = request.META.get('HTTP_REFERER')
                return redirect(url_referer)
            
            user_obj = User.objects.get(id = user_id)
            if validar_contrasena(new_password,user_obj.username) is False:
              messages.success(request, 'Contraseña no cumple requisitos')
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
                messages.success(request, 'No se encontró ningún usuario con este nombre')
                return redirect('forget-password')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            #Creation date of token
            timezone = pytz.timezone('America/Mexico_City')
            dateToken = datetime.now(timezone)
            profile_obj.created_at = dateToken
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'Un correo de recuperación fue enviado')
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
                return redirect('register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
    
            profile_obj = Profile.objects.create(user = user_obj )
            profile_obj.save()
            return redirect('home')

        except Exception as e:
            print(e)

    except Exception as e:
            print(e)

    return render(request , 'home/register.html')
  
  #2af
  
def signin_verification(request):
  if User.is_authenticated:
      print("if User.is_authenticated:")
      return redirect('home/index.html')
  if request.method=="POST":
    username=request.POST["username"]
    user_obj = User.objects.get(username = username)
    password=request.POST["password"]
    request.session["username"]=username
    request.session["password"]=password
    request.session["email"]=user_obj.email
    user = authenticate(request, username=username, password=password)
    request.session.flush()
    print("if request.method=='POST':")
    if user is not None:
      print("if user is not None:")
      send_otp(request)
      return render(request,'otp.html',{"email":user_obj.email})
    else:
      print("else")
      messages.info(request,"Credenciales incorrectas")
      return redirect("signin_verification")
          
          
def send_otp(request):
    s=""
    for x in range(0,6):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    request.session["date"] = str(datetime.now(timezone.utc))
    print("@@@@@@@@@@@@@@@@@@@@")
    print("saved in send_otp")
    print(request.session["date"])
    print("@@@@@@@@@@@@@@@@@@@@")
    send_mail("Tu código de inicio de sesión de dos factores","Tu código de inicio de sesión de dos factores es "+s +"\n Este código expirará en 5 minutos.",'easywashgdl@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"home/otp.html")


def  otp_verification(request):
  if  request.method=='POST':
    otp_=request.POST.get("otp")
    sessionDate=request.session["date"]
    print("@@@@@@@@@@@@@@@@@@@@")
    print("saved")
    print(sessionDate)
    print("otp")
    print(otp_)
    print("@@@@@@@@@@@@@@@@@@@@")

    otpDate =  datetime.strptime(sessionDate, "%Y-%m-%d %H:%M:%S.%f%z")
    dateNow = datetime.now(timezone.utc)
    tokenDate = otpDate + timedelta(minutes=5)
    print("@@@@@@@@@@@@@@@@@@@@")
    print("saved")
    print(sessionDate)
    print("converted")
    print(otpDate)
    print("now")
    print(dateNow)
    print()
    if dateNow > tokenDate:
      email = request.session["email"]
      messages.error(request,"Código expirado")
      return render(request,'home/otp.html',{'email':email})
    
    if otp_ == request.session["otp"]:
      username = request.session['username']
      password = request.session['password']
      user = authenticate(request, username=username, password=password)
      login(request, user)
      #User.is_active=True
      return redirect('home')
    else:
      email = request.session["email"]
      messages.error(request,"El código no coincide")
      return render(request,'home/otp.html',{'email':email})
  else:
    return redirect("home")
    

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
      messages.error(request, "Campo Teléfono no es una entrada válida")
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
    

    try:
      key = Fernet.generate_key()
      fernet = Fernet(key)
      encrypted_name = fernet.encrypt(name.encode())
      encrypted_last_name = fernet.encrypt(last_name.encode())
      encrypted_phone= fernet.encrypt(phone.encode())
      encrypted_service = fernet.encrypt(service.encode())
      encrypted_plate = fernet.encrypt(plate.encode())
      encrypted_total = fernet.encrypt(total.encode())

      servicio = ServicePage.objects.create(
      first_name=encrypted_name, last_name=encrypted_last_name, phone=encrypted_phone, type_service=encrypted_service, plate_code=encrypted_plate, price=total)
      messages.success(request, 'Servicio registrado!')
      print("DOOOOOOOOOOOOOOOOOOONEEEEEEEEE")
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
