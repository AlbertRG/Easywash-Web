from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin #for classes
from django.contrib.auth.decorators import login_required

from .models import Inventory, ServicePage
from django.contrib import messages
from datetime import date
from dateutil import parser
import re
from django.core.paginator import Paginator
from django.db import models
import pandas as pd
from django.db.models import Count
from django.db.models.functions import ExtractHour, ExtractWeekDay
from django.db.models import F, Func, IntegerField
from django.template.loader import get_template
from django.http import HttpResponse

# Create your views here.
#Inventario
#class InventarioView(LoginRequiredMixin, TemplateView):
#  template_name = 'adminpages/inventario.html'
#  login_url = 'adminpages/inventario.html,'
#PDF

#Graficos
@login_required 
def sales_chart(request):
    #Ventas
    sales_data = ServicePage.objects.all().order_by('service_date')
    fechas = [venta.service_date.strftime('%Y-%m-%d') for venta in sales_data]
    montos = [float(venta.price) for venta in sales_data]
    #Servicios
    service_data = ServicePage.objects.values('type_service').annotate(count=models.Count('type_service'))
    service_types = [entry['type_service'] for entry in service_data]
    service_counts = [entry['count'] for entry in service_data]
    #Series
    servicios = ServicePage.objects.all().order_by('service_date')
    servicos_data = ServicePage.objects.values('service_date').annotate(count=models.Count('service_date'))
    fechasSeries = [servicio.service_date.strftime('%Y-%m-%d') for servicio in servicios]
    registros = [entry['count'] for entry in servicos_data]
    
    
    return render(request, 'adminpages/charts.html', {'fechas':fechas, 'montos':montos, 'service_types': service_types, 'service_counts': service_counts, 'fechasSeries': fechasSeries, 'registros': registros})

def sales_search(request):
  date1 = request.POST['desde']
  date2 = request.POST['hasta']
  
  
  if date1 == "" and date2 == "":
    return redirect("estadisticas")
  
  if date2 == "":
    sales_data = ServicePage.objects.filter(service_date__gte=date1).order_by('service_date')
    service_data = ServicePage.objects.filter(service_date__gte=date1).values('type_service').annotate(count=models.Count('type_service'))
    servicios = ServicePage.objects.filter(service_date__gte=date1).order_by('service_date')
    servicos_data = ServicePage.objects.filter(service_date__gte=date1).values('service_date').annotate(count=models.Count('service_date'))
    messages.success(request, 'Estadisticas a partir de '+date1)



    
  if date1 == "":
    sales_data = ServicePage.objects.filter(service_date__lte=date2).order_by('service_date')
    service_data = ServicePage.objects.filter(service_date__lte=date2).values('type_service').annotate(count=models.Count('type_service'))
    servicios = ServicePage.objects.filter(service_date__lte=date2).order_by('service_date')
    servicos_data = ServicePage.objects.filter(service_date__lte=date2).values('service_date').annotate(count=models.Count('service_date'))
    messages.success(request, 'Estadisticas hasta '+date2)

    
  if date1 != "" and date2 != "":
    sales_data = ServicePage.objects.filter(service_date__gte=date1, service_date__lte=date2).order_by('service_date')
    service_data = ServicePage.objects.filter(service_date__gte=date1, service_date__lte=date2).values('type_service').annotate(count=models.Count('type_service'))
    servicios = ServicePage.objects.filter(service_date__gte=date1, service_date__lte=date2).order_by('service_date')
    servicos_data = ServicePage.objects.filter(service_date__gte=date1, service_date__lte=date2).values('service_date').annotate(count=models.Count('service_date'))
    messages.success(request, 'Estadisticas desde '+date1+" hasta "+date2)



  #VEnbtas
  fechas = [venta.service_date.strftime('%Y-%m-%d') for venta in sales_data]
  montos = [float(venta.price) for venta in sales_data]
  #Servicios
  service_types = [entry['type_service'] for entry in service_data]
  service_counts = [entry['count'] for entry in service_data]
  #series
  fechasSeries = [servicio.service_date.strftime('%Y-%m-%d') for servicio in servicios]
  registros = [entry['count'] for entry in servicos_data]
  
  return render(request, 'adminpages/charts.html', {'fechas':fechas, 'montos':montos, 'service_types': service_types, 'service_counts': service_counts, 'fechasSeries': fechasSeries, 'registros': registros})



@login_required 
def service_chart(request):
    service_data = ServicePage.objects.values('type_service').annotate(count=models.Count('type_service'))
    service_types = [entry['type_service'] for entry in service_data]
    service_counts = [entry['count'] for entry in service_data]
    return render(request, 'service_chart.html', {'service_types': service_types, 'service_counts': service_counts})

#Inventario
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
#Ventas
@login_required  
def Ventas(request):
  ventasLista = ServicePage.objects.all()
  return render(request,'adminpages/ventas.html',{'ventas': ventasLista})


@login_required
def VentasEdicion(request, id):
    venta = ServicePage.objects.get(id=id)
    return render(request, "adminpages/ventas-edicion.html", {"venta": venta})

def VentaEliminar(request, id):
    venta = ServicePage.objects.get(id=id)
    venta.delete()
    messages.success(request, 'Venta eliminado!')
    return redirect('ventas')

@login_required
def VentasEditar(request):
    codigo = request.POST["txtCodigo"]
    nombre = request.POST['txtNombre']
    apellido = request.POST['txtApellido']
    servicio = request.POST['txtServicio']
    tel = request.POST['txtTelefono']
    placas = request.POST['txtPlacas']
    total = request.POST['numTotal']

    #Validaciones
    if nombre == "" or apellido == "" or servicio == "" or tel == "" or placas == "" or total=="":
      messages.error(request, "Completa todos los campos")
      return redirect('edicionVentas/%s' % codigo)

    
    if not validar_placa_mexicana(placas):
      messages.error(request, "Placa de carro no válida")
      return redirect('edicionVentas/%s' % codigo)


    
    if not validar_string(tel):
      messages.error(request, "Campo Total no es una entrada válida")
      return redirect('edicionVentas/%s' % codigo)
     
    try:
      parse_total = float(total)
    except Exception as e:
      messages.error(request, "Campo Total no es una entrada válida")
      print(e)
      return redirect('edicionVentas/%s' % codigo)

    if not parse_total > 0:
      messages.error(request, "Cantidad debe de ser mayor o igual a 0")
      return redirect('edicionVentas/%s' % codigo)

    venta = ServicePage.objects.get(id=codigo)
    venta.first_name = nombre
    venta.last_name = apellido
    venta.phone = tel
    venta.type_service = servicio
    venta.plate_code = placas
    venta.price = total
    venta.save()

    messages.success(request, '¡Venta actualizada!')

    return redirect('ventas')

@login_required
def VentasBuscar(request):
  date1 = request.POST['txtdate1']
  date2 = request.POST['txtdate2']
  phone = request.POST['txtTelefono']
  plate = request.POST['txtPlacas']
  service = request.POST['txtServicio']
  if date1 == "" and date2 == "" and phone == "" and plate == "" and service == "":
    return redirect('ventas')
  
  if service != "":
    serviceQuery = ServicePage.objects.filter(type_service=service)
    messages.success(request, 'Ventas de '+service)
    return render(request,'adminpages/ventas.html',{'ventas': serviceQuery})
  
  if date2 == "" and phone == "" and plate == "" and service == "":
    ventasdate1 = ServicePage.objects.filter(service_date__gte=date1)
    messages.success(request, 'Ventas a partir de '+date1)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate1})
  
  if date1 == "" and date2 == "" and phone == "" and service == "":
    ventasdate6 = ServicePage.objects.filter(plate_code=plate)
    messages.success(request, 'Ventas de placa '+plate)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate6})
  
  if date1 == "" and date2 == "" and plate == "" and service == "":
    ventasdate7 = ServicePage.objects.filter(phone=phone)
    messages.success(request, 'Ventas de numero '+phone)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate7})
  
  if date1 == "" and phone == "" and plate == "" and service == "":
    ventasdate2 = ServicePage.objects.filter(service_date__lte=date2)
    messages.success(request, 'Ventas hasta '+date2)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate2})
  
  if phone == "" and plate == "" and service == "":
    ventasdate3 = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2)
    messages.success(request, 'Ventas desde '+date1 +" hasta "+date2)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate3})
  
  if date1 == "" and phone == "" and service == "":
    ventasdate8 = ServicePage.objects.filter(service_date__lte=date2,plate_code=plate)
    messages.success(request, 'Ventas hasta '+date2)
    messages.success(request, 'Ventas de Placa '+plate)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate8})
  
  
  if date1 == "" and plate == "" and service == "":
    ventasdate9 = ServicePage.objects.filter(service_date__lte=date2,phone=phone)
    messages.success(request, 'Ventas hasta '+date2)
    messages.success(request, 'Ventas de Teléfono '+phone)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate9})
  
  if date1 == "" and date2 == "" and service == "":
    ventasdate9 = ServicePage.objects.filter(plate_code=plate,phone=phone)
    messages.success(request, 'Ventas de Placa '+plate)
    messages.success(request, 'Ventas de Teléfono '+phone)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate9})
  
  if date2 == "" and phone == "" and service == "":
    ventasdate10 = ServicePage.objects.filter(plate_code=plate,service_date__gte=date1)
    messages.success(request, 'Ventas desde '+date1)
    messages.success(request, 'Ventas de Placa '+plate)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate10})
  
  if date2 == "" and plate == "" and service == "":
    ventasdate10 = ServicePage.objects.filter(phone=phone,service_date__gte=date1)
    messages.success(request, 'Ventas desde '+date1)
    messages.success(request, 'Ventas de Teléfono '+phone)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate10})
  
  if plate == "" and service == "":
    ventasdate4 = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2,phone=phone)
    messages.success(request, 'Ventas desde '+date1 +" hasta "+date2)
    messages.success(request, 'Ventas de teléfono '+phone)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate4})
  
  if phone=="" and service == "":
    ventasdate5 = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2,plate_code=plate)
    messages.success(request, 'Ventas desde '+date1 +" hasta "+date2)
    messages.success(request, 'Ventas de placa '+plate)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate5})
  
  if date1 == "" and service == "":
    ventasdate11 = ServicePage.objects.filter(plate_code=plate,service_date__lte=date2,phone=phone)
    messages.success(request, 'Ventas hasta '+date2)
    messages.success(request, 'Ventas de teléfono '+phone)
    messages.success(request, 'Ventas de placa '+plate)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate11})
  
  ventasdate12 = ServicePage.objects.filter(service_date__gte=date1,plate_code=plate,service_date__lte=date2,phone=phone)
  messages.success(request, 'Ventas desde '+date1 +" hasta "+date2)
  messages.success(request, 'Ventas de teléfono '+phone)
  messages.success(request, 'Ventas de placa '+plate)
  return render(request,'adminpages/ventas.html',{'ventas': ventasdate12})
  
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

