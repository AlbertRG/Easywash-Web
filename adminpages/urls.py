from django.urls import path

from . import views

urlpatterns = [
  path('inventario', views.Inventario, name='inventario'),
  path('registrarArticulo',views.InventarioRegistrar, name="registerArticle"),
  path('edicionInventario/<sku>',views.InventarioEdicion,name="edicion-inventario"),
  path('editarInventario',views.InventarioEditar,name="editar-inventario"),
  path('eliminarInventario/<sku>',views.InventarioEliminar, name='eliminar-inventario'),
  path('ventas', views.Ventas, name='ventas'),
  path('buscarVenta', views.VentasBuscar, name='buscar-venta'),
  path('edicionVenta/<id>',views.VentasEdicion,name="edicion-venta"),
  path('editarVenta',views.VentasEditar,name="editar-venta"),
  path('eliminarVenta/<id>',views.VentaEliminar, name='eliminar-venta'),
]
