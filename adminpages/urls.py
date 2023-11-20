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
  path('estadisticas',views.sales_chart,name="estadisticas"),
  path('sales-search',views.sales_search,name="sales-search"),
  path('eliminarVenta/<id>',views.VentaEliminar, name='eliminar-venta'),
  path('sales_PDF',views.sales_PDF, name='sales_PDF'),
  path('pdf_report',views.pdf_report_create, name='pdf_report'),
  path('clients',views.Clientes, name='clients'),
  path('descuento/<id>',views.ClientesDescuento, name='descuento'),
  path('registrarDescuento',views.registrarDescuento, name='registrarDescuento'),
  path('buscarClientDescuento',views.buscarClient,name='buscarClientDescuento'),




]
