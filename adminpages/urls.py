from django.urls import path

from . import views

urlpatterns = [
  path('inventario', views.InventarioView.as_view(), name='inventario'),
  path('ventas', views.VentasView.as_view(), name='ventas'),
]
