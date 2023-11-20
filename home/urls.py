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
    path('editar-cuenta', views.editar_cuenta, name='editar-cuenta'),
    path('eliminar-cuenta', views.eliminarCuenta, name='eliminar-cuenta'),
    path('terms', views.terminosCondiciones, name='terms'),
    path('buscar_cliente/',views.buscar_cliente,name="buscar_cliente"),
    path('easywashapp',views.nuestraApp,name="easywashapp"),
    path('descargar-app',views.descargarApp,name="descargar-app")
]
