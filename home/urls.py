from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    #path('loginaccount', views.LoginInterfaceView.as_view(), name='loginaccount'),
    path('loginaccount', views.LoginInterface, name='loginaccount'),
    path('logout', views.LogoutInterfaceView.as_view(), name='logout'),
    path('register' , views.Register , name="register"),
   # path('signup', views.SignupView.as_view(), name='signup'),
    path('forget-password' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
    path('otp_verification',views.otp_verification,name="otp_verification"),
    #path('loginredirect', views.LoginRedirectView.as_view(), name='loginredirect'),
    #path('signin_verification',views.signin_verification,name="signin_verification"),

]
