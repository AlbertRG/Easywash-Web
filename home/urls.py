from django.urls import path

from . import views

urlpatterns = [
    path('', views.Servicio, name='home'),
    path('registrarServicio',views.ServicioRegistrar, name="registerService"),
    path('loginaccount', views.LoginInterface, name='loginaccount'),
    path('logout', views.LogOut, name='logout'),
    path('register' , views.Register , name="register"),
    path('forget-password' , views.ForgetPassword , name="forget-password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
    path('otp_verification',views.otp_verification,name="otp_verification"),

]
