from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin #for classes
from django.contrib.auth.decorators import login_required
from .models import Inventory
from django.contrib import messages
from datetime import date
from dateutil import parser
# Create your views here.
#Inventario
#class InventarioView(LoginRequiredMixin, TemplateView):
#  template_name = 'adminpages/inventario.html'
#  login_url = 'adminpages/inventario.html,'
@login_required  
def Inventario(request):
  inventarioLista = Inventory.objects.all()
 # messages.success(request, 'Inventario listado')
  return render(request,'adminpages/inventario.html',{'inventario': inventarioLista})

@login_required  
def InventarioRegistrar(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    categoria = request.POST['txtCategoria']
    expiracion = request.POST['txtExpiracion']
    cantidad = request.POST['numInventario']
    if codigo == "" or nombre == "" or categoria == "" or expiracion == "" or cantidad == "":
      messages.error(request, "Completa todos los campos")
      return redirect('inventario')
    try:
      date_parsed = parser.parse(expiracion)  
    except Exception as e:
      messages.error(request, "Campo expiracion no es una fecha válida")
      print(e)
      return redirect('inventario')
      

    if not isinstance(date_parsed, date):
      messages.error(request, "Campo expiracion no es una fecha válida")
      return redirect('inventario')
    
    try:
      parse_cant = int(cantidad)
    except Exception as e:
      messages.error(request, "Campo cantidad no es una entrada válida")
      print(e)
      return redirect('inventario')

    if not parse_cant > 0:
      messages.error(request, "Cantidad debe de ser mayor o igual a 0")
      return redirect('inventario')
    
    
    if Inventory.objects.filter(sku = codigo).first():
      messages.error(request,"SKU ya registrado")
      return redirect('inventario')

    try:
      inventario = Inventory.objects.create(
      name=nombre, sku=codigo, category=categoria, quantity=cantidad, expiration_date=expiracion)
      messages.success(request, 'Articulo registrado!')
    except Exception as e:
      print(e)  
    return redirect('inventario')

def InventarioEdicion(request, sku):
    article = Inventory.objects.get(sku=sku)
    
    return render(request, "adminpages/inventario-edicion.html", {"inventory": article})


def InventarioEditar(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    categoria = request.POST['txtCategoria']
    expiracion = request.POST['txtExpiracion']
    cantidad = request.POST['numInventario']
    #Validaciones
    if nombre == "" or categoria == "" or expiracion == "" or cantidad == "":
      messages.error(request, "Completa todos los campos")
      return redirect('edicionInventario/%s' % codigo)
    try:
      date_parsed = parser.parse(expiracion)
    except Exception as e:
      messages.error(request, "Campo expiracion no es una fecha válida")
      print(e)
      return redirect('edicionInventario/%s' % codigo)

    if not isinstance(date_parsed, date):
      messages.error(request, "Campo expiracion no es una fecha válida")
      return redirect('edicionInventario/%s' % codigo)
    
    try:
      parse_cant = int(cantidad)
    except Exception as e:
      messages.error(request, "Campo cantidad no es una entrada válida")
      print(e)
      return redirect('edicionInventario/%s' % codigo)

    parse_cant = int(cantidad)
    if not isinstance(parse_cant, int):
      messages.error(request, "Campo cantidad no es una entrada válida")
      print("Cantidad es: ")
      print(cantidad)
      return redirect('edicionInventario/%s' % codigo)
    
    parse_cant = int(cantidad)
    
    if not parse_cant > 0:
      messages.error(request, "Cantidad debe de ser mayor o igual a 0")
      return redirect('edicionInventario/%s' % codigo)
    inventario = Inventory.objects.get(sku=codigo)
    inventario.name = nombre
    inventario.category = categoria
    inventario.expiration_date = expiracion
    inventario.quantity = cantidad
    inventario.save()

    messages.success(request, '¡Producto actualizado!')

    return redirect('inventario')


def InventarioEliminar(request, sku):
    curso = Inventory.objects.get(sku=sku)
    curso.delete()
    messages.success(request, '¡Producto eliminado!')
    return redirect('inventario')

class VentasView(LoginRequiredMixin, TemplateView):
  template_name = 'adminpages/ventas.html'
  login_url = 'login'