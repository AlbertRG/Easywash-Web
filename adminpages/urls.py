from django.urls import path

from . import views

urlpatterns = [
  path('inventario', views.Inventario, name='inventario'),
  path('registrarArticulo',views.InventarioRegistrar, name="registerArticle"),
  path('edicionInventario/<sku>',views.InventarioEdicion,name="edicion-inventario"),
  path('editarInventario',views.InventarioEditar,name="editar-inventario"),
  path('eliminarInventario/<sku>',views.InventarioEliminar, name='eliminar-inventario'),
  path('ventas', views.VentasView.as_view(), name='ventas'),
]
