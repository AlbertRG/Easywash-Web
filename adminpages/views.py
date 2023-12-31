from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin #for classes
from django.contrib.auth.decorators import login_required
from .models import Inventory, ServicePage, Client, Vehicle, Service, ServiceTicket
from django.contrib import messages
from datetime import date
from dateutil import parser
import re
from django.core.paginator import Paginator
from django.db import models, transaction
import pandas as pd
from django.db.models import Count, Q
from django.db.models.functions import ExtractHour, ExtractWeekDay
from django.db.models import F, Func, IntegerField
from django.template.loader import get_template
from django.http import HttpResponse
import pdfkit
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.generic import View
from xhtml2pdf import pisa
from django.conf import settings 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
#Inventario
#class InventarioView(LoginRequiredMixin, TemplateView):
#  template_name = 'adminpages/inventario.html'
#  login_url = 'adminpages/inventario.html,'



#ServiciosOfrecidos
@login_required
def ServiciosOfrecidos(request):
  servicios = Service.objects.all()
  return render(request, 'adminpages/serviciosOfrecidos.html', {'services':servicios})

@login_required
def ServiciosEditar(request,id):
  servicio = Service.objects.get(id=id)
  return render(request, 'adminpages/servicios.html', {'servicio':servicio})

@login_required
def serviciosEliminar(request,id):
    servicio = Service.objects.get(id=id)
    servicio.delete()
    messages.success(request, 'Servicio eliminado')
    return redirect('servicios')


@login_required
def ServiciosEdicion(request):
  idtxt = request.POST.get('txtCodigo','')
  nametxt = request.POST.get('txtNombre','')
  pricetxt = request.POST.get('txtPrice','')
  if nametxt == "" or pricetxt == "":
    messages.error(request, "Completa todos los campos")
    return redirect('servicios')
  try:
      parse_total = float(pricetxt)
  except Exception as e:
      messages.error(request, "Campo Total no es una entrada válida")
      print(e)
      return redirect('servicios')

  if not parse_total > 0:
      messages.error(request, "Cantidad debe de ser mayor a 0")
      return redirect('servicios')
  servicio = Service.objects.get(id=idtxt)
  servicio.name = nametxt
  servicio.price = pricetxt
  servicio.save()
  messages.success(request,"Servicio actualizado")
  return redirect('servicios')

@login_required
def ServiciosAgregar(request):
  nametxt = request.GET.get('txtServicio','')
  preciotxt = request.GET.get('txtPrecio','')
  if nametxt == "" or preciotxt == "":
    messages.error(request,"Completa todos los campos")
    return redirect('servicios')
  try:
      parse_total = float(preciotxt)
  except Exception as e:
      messages.error(request, "Campo Total no es una entrada válida")
      print(e)
      return redirect('servicios')

  if not parse_total > 0:
      messages.error(request, "Cantidad debe de ser mayor a 0")
      return redirect('servicios')
  servicio = Service.objects.create(name=nametxt.strip(),price=preciotxt.strip())
  messages.success(request,"Servicio agregado")
  return redirect('servicios')
  

#PDF
#VENTAS
@login_required 
def pdf_report_create(request):
  date1 = request.GET['txtdate1']
  date2 = request.GET['txtdate2']
  phone = request.GET['txtTelefono']
  plate = request.GET['txtPlacas']
  service = request.GET['txtServicio']

  if date1 == "" and date2 == "" and phone == "" and plate == "" and service == "":
    products = ServicePage.objects.all()
    mensajes = ["Total de Ventas"]

  if service != "":
    products = ServicePage.objects.filter(type_service=service)
    mensajes = ["Ventas de "+service]
  
  if date2 == "" and phone == "" and plate == "" and service == "":
    products = ServicePage.objects.filter(service_date__gte=date1)
    mensajes = ['Ventas a partir de '+date1]
  
  if date1 == "" and date2 == "" and phone == "" and service == "":
    products = ServicePage.objects.filter(plate_code=plate)
    mensajes = ['Ventas de placa '+plate]
  
  if date1 == "" and date2 == "" and plate == "" and service == "":
    products = ServicePage.objects.filter(phone=phone)
    mensajes = ['Ventas de numero '+phone]
  
  if date1 == "" and phone == "" and plate == "" and service == "":
    products = ServicePage.objects.filter(service_date__lte=date2)
    mensajes = ['Ventas hasta '+date2]
  
  if phone == "" and plate == "" and service == "":
    products = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2)
    mensajes = ['Ventas desde '+date1 +" hasta "+date2]
  
  if date1 == "" and phone == "" and service == "":
    products = ServicePage.objects.filter(service_date__lte=date2,plate_code=plate)
    mensajes = ['Ventas hasta '+date2, 'Ventas de Placa '+plate]
  
  
  if date1 == "" and plate == "" and service == "":
    products = ServicePage.objects.filter(service_date__lte=date2,phone=phone)
    mensajes = ['Ventas hasta '+date2, 'Ventas de Teléfono '+phone]
  
  if date1 == "" and date2 == "" and service == "":
    products = ServicePage.objects.filter(plate_code=plate,phone=phone)
    mensajes = ['Ventas de Placa '+plate, 'Ventas de Teléfono '+phone]
  
  if date2 == "" and phone == "" and service == "":
    products = ServicePage.objects.filter(plate_code=plate,service_date__gte=date1)
    mensajes = ['Ventas desde '+date1, 'Ventas de Placa '+plate]
  
  if date2 == "" and plate == "" and service == "":
    products = ServicePage.objects.filter(phone=phone,service_date__gte=date1)
    mensajes = ['Ventas desde '+date1, 'Ventas de Teléfono '+phone]
  
  if plate == "" and service == "":
    products = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2,phone=phone)
    mensajes = ['Ventas desde '+date1 +" hasta "+date2, 'Ventas de teléfono '+phone]
  
  if phone=="" and service == "":
    products = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2,plate_code=plate)
    mensajes = ['Ventas desde '+date1 +" hasta "+date2,  'Ventas de placa '+plate]
  
  if date1 == "" and service == "":
    products = ServicePage.objects.filter(plate_code=plate,service_date__lte=date2,phone=phone)
    mensajes = ['Ventas hasta '+date2, 'Ventas de teléfono '+phone, 'Ventas de placa '+plate]
  
  if date1 != "" and date2 != "" and phone != "" and plate != "" and service != "":
    products = ServicePage.objects.filter(service_date__gte=date1,plate_code=plate,service_date__lte=date2,phone=phone)
    mensajes = ['Ventas desde '+date1 +" hasta "+date2, 'Ventas de teléfono '+phone,  'Ventas de placa '+plate]
    
  template_path = 'pdf_convert/pdfReport.html'

  context = {'ventas': products, 'messages': mensajes}

  response = HttpResponse(content_type='application/pdf')

  response['Content-Disposition'] = 'filename="reporte_ventas.pdf"'

  pdf_page = pisa.pisaDocument(
        get_template(template_path).render(context),
        response,
        encoding='UTF-8',
        link_callback=lambda uri, rel: uri.startswith(settings.MEDIA_URL)
    )

  if not pdf_page.err:
    return response

  return HttpResponse('We had some errors while generating the PDF.')


#GRAPH
 
class PDFView(View):
    def get(self, request):
        # Renderiza un template HTML con una gráfica generada con JavaScript
        print('rafa')
        context = {'example_data': 'Hola desde Django'}
        html_template = render_to_string('adminpages/chartReports.html', context, request=request)
        
        # Convierte el HTML en PDF utilizando pdfkit
        pdf = pdfkit.from_string(html_template, False, configuration="./wkhtmltopdf_config.json")

        # Crea una respuesta HTTP con el PDF generado
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="output.pdf"'
    
        return response
@login_required 
def sales_PDF(request):
  date1 = request.POST['desde']
  date2 = request.POST['hasta']
  print("@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
  print(date1)
  print(date2)
  
  print("@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
  
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
  context = {'fechas':fechas, 'montos':montos, 'service_types': service_types, 'service_counts': service_counts, 'fechasSeries': fechasSeries, 'registros': registros}
  html_template = render_to_string('adminpages/chartReports.html', context, request=request)
        
        # Convierte el HTML en PDF utilizando pdfkit
  config = {
    "wkhtmltopdf": "/usr/local/bin/wkhtmltopdf",  # Reemplaza con la ubicación correcta en tu sistema
}
  pdf = pdfkit.from_string(html_template, False, configuration=config)

        # Crea una respuesta HTTP con el PDF generado
  response = HttpResponse(pdf, content_type='application/pdf')
  response['Content-Disposition'] = 'inline; filename="output.pdf"'
    
  return response
  

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
@login_required 
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
@login_required 
def InventarioEdicion(request, sku):
    article = Inventory.objects.get(sku=sku)
    return render(request, "adminpages/inventario-edicion.html", {"inventory": article})

@login_required 
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

@login_required 
def InventarioEliminar(request, sku):
    curso = Inventory.objects.get(sku=sku)
    curso.delete()
    messages.success(request, '¡Producto eliminado!')
    return redirect('inventario')


#Descuento Clientes
@login_required   
def Clientes(request):
  clients = Client.objects.annotate(num_tickets=Count('serviceticket', filter=Q(serviceticket__status="Terminado"))).filter(num_tickets__gte=5)
  for client in clients:
    print(f"{client.first_name} {client.last_name} tiene {client.num_tickets} tickets terminados.")
  print(clients)
  return render(request,'adminpages/clientes.html',{'clientes': clients})

@login_required
def buscarClient(request):
  correo = request.GET.get('txtCorreo','')
  telefono = request.GET.get('txtTelefono','')
  placas = request.GET.get('txtPlacas','')
  #Todos VACIOS
  if correo == "" and telefono == "" and placas == "":
      clients = Client.objects.annotate(num_tickets=Count('serviceticket', filter=Q(serviceticket__status="Terminado"))).filter(num_tickets__gte=5)
      return render(request,'adminpages/clientes.html',{'clientes': clients})
  #TODOS LLENO
  if correo != "" and telefono != "" and placas != "":
    try:
      cliente = Client.objects.get(phone=telefono.strip(),email=correo.strip())
      carros = Vehicle.objects.get(plate=placas.strip(),owner=cliente)
    except (Vehicle.DoesNotExist, Client.DoesNotExist):
      messages.success(request,'Cliente no encontrado')
      return redirect('buscarClientDescuento')
    if carros is None:
      messages.error(request,'Cliente no encontrado')
    elif ServiceTicket.objects.filter(client=cliente, status="Terminado").count() >= 5:
      messages.success(request,'Cliente encontrado')
      clientes = Client.objects.filter(phone=telefono.strip())
      return render(request,'adminpages/clientes.html',{'clientes': clientes})
  #TELEFONO Y PLACAS
  if correo == "" and telefono != "" and placas != "":
    try:
      cliente = Client.objects.get(phone=telefono.strip())
      carros = Vehicle.objects.get(plate=placas.strip(),owner=cliente)
    except (Vehicle.DoesNotExist, Client.DoesNotExist):
      messages.success(request,'Cliente no encontrado')
      return redirect('buscarClientDescuento')
    if carros is None:
      messages.error(request,'Cliente no encontrado')
    elif ServiceTicket.objects.filter(client=cliente, status="Terminado").count() >= 5:
      messages.success(request,'Cliente encontrado')
      clientes = Client.objects.filter(phone=telefono.strip())
      return render(request,'adminpages/clientes.html',{'clientes': clientes})
  
  #Correo y telefono
  if correo != "" and telefono != "" and placas == "":
    try:
      clientes = Client.objects.filter(email=correo.strip(),phone=telefono.strip())
      cliente = Client.objects.get(email=correo.strip(),phone=telefono.strip())
    except Client.DoesNotExist:
      messages.success(request,'Cliente no encontrado')
      return redirect('buscarClientDescuento')
    if clientes is None:
      messages.error(request,'Cliente no encontrado')
    elif ServiceTicket.objects.filter(client=cliente, status="Terminado").count() >= 5:
      messages.success(request,'Cliente encontrado')
      return render(request,'adminpages/clientes.html',{'clientes': clientes})
  #Correo y placas
  if correo != "" and telefono == "" and placas != "":
    try:
      cliente = Client.objects.get(email=correo.strip())
      carros = Vehicle.objects.get(plate=placas.strip(),owner=cliente)
    except (Vehicle.DoesNotExist, Client.DoesNotExist):
      messages.success(request,'Cliente no encontrado')
      return redirect('buscarClientDescuento')
    if carros is None:
      messages.error(request,'Cliente no encontrado')
    elif ServiceTicket.objects.filter(client=cliente, status="Terminado").count() >= 5:
      messages.success(request,'Cliente encontrado')
      clientes = Client.objects.filter(email=correo.strip())
      return render(request,'adminpages/clientes.html',{'clientes': clientes})
  #Correo
  if correo != "" and telefono == "" and placas == "":
    try:
      clientes = Client.objects.filter(email=correo.strip())
      cliente = Client.objects.get(email=correo.strip())
    except Client.DoesNotExist:
      messages.success(request,'Cliente no encontrado')
      return redirect('buscarClientDescuento')
    if clientes is None:
      messages.error(request,'Cliente no encontrado')
    elif ServiceTicket.objects.filter(client=cliente, status="Terminado").count() >= 5:
      messages.success(request,'Cliente encontrado')
      return render(request,'adminpages/clientes.html',{'clientes': clientes})
  #Telefono 
  if correo == "" and telefono != "" and placas == "":
    try:
      clientes = Client.objects.filter(phone=telefono.strip())
      cliente = Client.objects.get(phone=telefono.strip())
    except Client.DoesNotExist:
      messages.success(request,'Cliente no encontrado')
      return redirect('buscarClientDescuento')
    if clientes is None:
      messages.error(request,'Cliente no encontrado')
    elif ServiceTicket.objects.filter(client=cliente, status="Terminado").count() >= 5:
      messages.success(request,'Cliente encontrado')
      return render(request,'adminpages/clientes.html',{'clientes': clientes})
  #Placas 
  if correo == "" and telefono == "" and placas != "":
    try:
      carros = Vehicle.objects.filter(plate=placas.strip())
      cliente = Vehicle.objects.get(plate=placas.strip())
    except Vehicle.DoesNotExist:
      messages.success(request,'Cliente no encontrado')
      return redirect('buscarClientDescuento')
    if carros is None:
      messages.error(request,'Cliente no encontrado')
    elif ServiceTicket.objects.filter(client=cliente.owner, status="Terminado").count() >= 5:
      messages.success(request,'Cliente encontrado')
      clientes = Client.objects.filter(id=cliente.owner.id)
      return render(request,'adminpages/clientes.html',{'clientes': clientes})
  
  clients = Client.objects.annotate(num_tickets=Count('serviceticket', filter=Q(serviceticket__status="Terminado"))).filter(num_tickets__gte=5)
  return render(request,'adminpages/clientes.html',{'clientes': clientes})
    
@login_required   
def ClientesDescuento(request, id):
  cliente = Client.objects.get(id=id)
  vehicles = Vehicle.objects.filter(owner=cliente)
  services = Service.objects.all()
  return render(request,'adminpages/descuento.html',{'services':services,'cliente': cliente, 'cars':vehicles})

@login_required
def registrarDescuento(request):
  try:
    phoneText = request.POST['txtTelefono']
    client = Client.objects.get(phone=phoneText)
    nameText = request.POST['txtNombre']
    last_nameText = request.POST['txtApellido']
    serviceText = request.POST['txtServicio']
    plateText = request.POST['txtPlacas']
    totalText = request.POST['numTotal']
    
    if nameText == "" or last_nameText == "" or serviceText == "" or phoneText == "" or plateText == "" or totalText=="":
        messages.error(request, "Completa todos los campos")
        return ('registrarDescuento')
    serviceObject = Service.objects.get(id=serviceText)
    carObject = Vehicle.objects.get(id=plateText)
    print("name")
    print(nameText)
    print("last_name")
    print(last_nameText)
    print("phone")  
    print(phoneText)
    print("service")
    print(serviceObject.name)
    print("plate")
    print(carObject.plate)
    print("total")
    print(totalText)
  except MultiValueDictKeyError:
      messages.error(request, "Completa todos los campos")
      return redirect('descuento/%s' % client.id)
  if ServiceTicket.objects.filter(client=client, status="Terminado").count() >= 5:
      tickets_terminados = ServiceTicket.objects.filter(client=client, status="Terminado")[:5]
      with transaction.atomic():
          for ticket in tickets_terminados:
            ticket.status = "Canjeado"
            ticket.save()
        # Agregar un mensaje de éxito a tu sistema de mensajes

  ticketQuery = ServiceTicket.objects.create(client=client,car=carObject,service="Paquete {}".format(serviceObject.id),total=totalText,status="Canjeado",paymethod="Efectivo")
  servicePage = ServicePage.objects.create(
      first_name=nameText, last_name=last_nameText, phone=phoneText, type_service=serviceObject.name+" Descuento", plate_code=carObject.plate, price=totalText)
  messages.success(request, 'Se ha canjeado el descuento para el cliente {}'.format(client.first_name))  
  return redirect('clients')


  
#Ventas
@login_required   
def Ventas(request):
  ventasLista = ServicePage.objects.all()
  services = Service.objects.all()
  return render(request,'adminpages/ventas.html',{'ventas': ventasLista, 'services':services})


@login_required 
def VentasEdicion(request, id):
    venta = ServicePage.objects.get(id=id)
    servicios = Service.objects.all()
    return render(request, "adminpages/ventas-edicion.html", {"venta": venta,'services':servicios})
@login_required 
def VentaEliminar(request, id):
    venta = ServicePage.objects.get(id=id)
    venta.delete()
    messages.success(request, 'Venta eliminada')
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
    service = Service.objects.get(id=servicio)
    venta = ServicePage.objects.get(id=codigo)
    venta.first_name = nombre
    venta.last_name = apellido
    venta.phone = tel
    venta.type_service = service.name
    venta.plate_code = placas
    venta.price = total
    venta.save()

    messages.success(request, '¡Venta actualizada!')

    return redirect('ventas')

@login_required 
def VentasBuscar(request):
  date1 = request.GET['txtdate1']
  date2 = request.GET['txtdate2']
  phone = request.GET['txtTelefono']
  plate = request.GET['txtPlacas']
  service = request.GET.get('txtServicio','')
  accion = request.GET['accion']
  services = Service.objects.all()
  if accion == "buscar":
    if date1 == "" and date2 == "" and phone == "" and plate == "" and service == "":
      return redirect('ventas')
    
    if service != "":
      serviceQuery = ServicePage.objects.filter(type_service=service)
      messages.success(request, 'Ventas de '+service)
      return render(request,'adminpages/ventas.html',{'ventas': serviceQuery,'services':services})
    
    if date2 == "" and phone == "" and plate == "" and service == "" and date1 != "":
      ventasdate1 = ServicePage.objects.filter(service_date__gte=date1)
      messages.success(request, 'Ventas a partir de '+date1)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate1,'services':services})
    
    if date1 == "" and date2 == "" and phone == "" and service == "" and plate!="":
      ventasdate6 = ServicePage.objects.filter(plate_code=plate)
      messages.success(request, 'Ventas de placa '+plate)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate6,'services':services})
    
    if date1 == "" and date2 == "" and plate == "" and service == "":
      ventasdate7 = ServicePage.objects.filter(phone=phone)
      messages.success(request, 'Ventas de numero '+phone)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate7,'services':services})
    
    if date1 == "" and phone == "" and plate == "" and service == "" and date2!="":
      ventasdate2 = ServicePage.objects.filter(service_date__lte=date2)
      messages.success(request, 'Ventas hasta '+date2)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate2,'services':services})
    
    if phone == "" and plate == "" and service == "":
      ventasdate3 = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2)
      messages.success(request, 'Ventas desde '+date1 +" hasta "+date2)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate3,'services':services})
    
    if date1 == "" and phone == "" and service == "":
      ventasdate8 = ServicePage.objects.filter(service_date__lte=date2,plate_code=plate)
      messages.success(request, 'Ventas hasta '+date2)
      messages.success(request, 'Ventas de Placa '+plate)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate8,'services':services})
    
    
    if date1 == "" and plate == "" and service == "":
      ventasdate9 = ServicePage.objects.filter(service_date__lte=date2,phone=phone)
      messages.success(request, 'Ventas hasta '+date2)
      messages.success(request, 'Ventas de Teléfono '+phone)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate9,'services':services})
    
    if date1 == "" and date2 == "" and service == "":
      ventasdate9 = ServicePage.objects.filter(plate_code=plate,phone=phone)
      messages.success(request, 'Ventas de Placa '+plate)
      messages.success(request, 'Ventas de Teléfono '+phone)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate9,'services':services})
    
    if date2 == "" and phone == "" and service == "":
      ventasdate10 = ServicePage.objects.filter(plate_code=plate,service_date__gte=date1)
      messages.success(request, 'Ventas desde '+date1)
      messages.success(request, 'Ventas de Placa '+plate)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate10,'services':services})
    
    if date2 == "" and plate == "" and service == "":
      ventasdate10 = ServicePage.objects.filter(phone=phone,service_date__gte=date1)
      messages.success(request, 'Ventas desde '+date1)
      messages.success(request, 'Ventas de Teléfono '+phone)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate10,'services':services})
    
    if plate == "" and service == "":
      ventasdate4 = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2,phone=phone)
      messages.success(request, 'Ventas desde '+date1 +" hasta "+date2)
      messages.success(request, 'Ventas de teléfono '+phone)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate4,'services':services})
    
    if phone=="" and service == "":
      ventasdate5 = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2,plate_code=plate)
      messages.success(request, 'Ventas desde '+date1 +" hasta "+date2)
      messages.success(request, 'Ventas de placa '+plate)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate5,'services':services})
    
    if date1 == "" and service == "":
      ventasdate11 = ServicePage.objects.filter(plate_code=plate,service_date__lte=date2,phone=phone)
      messages.success(request, 'Ventas hasta '+date2)
      messages.success(request, 'Ventas de teléfono '+phone)
      messages.success(request, 'Ventas de placa '+plate)
      return render(request,'adminpages/ventas.html',{'ventas': ventasdate11,'services':services})
    
    ventasdate12 = ServicePage.objects.filter(service_date__gte=date1,plate_code=plate,service_date__lte=date2,phone=phone)
    messages.success(request, 'Ventas desde '+date1 +" hasta "+date2)
    messages.success(request, 'Ventas de teléfono '+phone)
    messages.success(request, 'Ventas de placa '+plate)
    return render(request,'adminpages/ventas.html',{'ventas': ventasdate12,'services':services})
  elif accion == "descargar" or accion == "enviar":
    date1 = request.GET.get('txtdate1')
    date2 = request.GET.get('txtdate2')
    phone = request.GET.get('txtTelefono')
    plate = request.GET.get('txtPlacas')
    service = request.GET.get('txtServicio')
    if date1 == "" and date2 == "" and phone == "" and plate == "" and service == "":
      products = ServicePage.objects.all()
      mensajes = ["Total de Ventas"]

    elif service != "":
      products = ServicePage.objects.filter(type_service=service)
      mensajes = ["Ventas de "+service]
    
    elif date2 == "" and phone == "" and plate == "" and service == "":
      products = ServicePage.objects.filter(service_date__gte=date1)
      mensajes = ['Ventas a partir de '+date1]
    
    elif date1 == "" and date2 == "" and phone == "" and service == "":
      products = ServicePage.objects.filter(plate_code=plate)
      mensajes = ['Ventas de placa '+plate]
    
    elif date1 == "" and date2 == "" and plate == "" and service == "":
      products = ServicePage.objects.filter(phone=phone)
      mensajes = ['Ventas de numero '+phone]
    
    elif date1 == "" and phone == "" and plate == "" and service == "":
      products = ServicePage.objects.filter(service_date__lte=date2)
      mensajes = ['Ventas hasta '+date2]
    
    elif phone == "" and plate == "" and service == "":
      products = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2)
      mensajes = ['Ventas desde '+date1 +" hasta "+date2]
    
    elif date1 == "" and phone == "" and service == "":
      products = ServicePage.objects.filter(service_date__lte=date2,plate_code=plate)
      mensajes = ['Ventas hasta '+date2, 'Ventas de Placa '+plate]
    
    
    elif date1 == "" and plate == "" and service == "":
      products = ServicePage.objects.filter(service_date__lte=date2,phone=phone)
      mensajes = ['Ventas hasta '+date2, 'Ventas de Teléfono '+phone]
    
    elif date1 == "" and date2 == "" and service == "":
      products = ServicePage.objects.filter(plate_code=plate,phone=phone)
      mensajes = ['Ventas de Placa '+plate, 'Ventas de Teléfono '+phone]
    
    elif date2 == "" and phone == "" and service == "":
      products = ServicePage.objects.filter(plate_code=plate,service_date__gte=date1)
      mensajes = ['Ventas desde '+date1, 'Ventas de Placa '+plate]
    
    elif date2 == "" and plate == "" and service == "":
      products = ServicePage.objects.filter(phone=phone,service_date__gte=date1)
      mensajes = ['Ventas desde '+date1, 'Ventas de Teléfono '+phone]
    
    elif plate == "" and service == "":
      products = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2,phone=phone)
      mensajes = ['Ventas desde '+date1 +" hasta "+date2, 'Ventas de teléfono '+phone]
    
    elif phone=="" and service == "":
      products = ServicePage.objects.filter(service_date__gte=date1,service_date__lte=date2,plate_code=plate)
      mensajes = ['Ventas desde '+date1 +" hasta "+date2,  'Ventas de placa '+plate]
    
    elif date1 == "" and service == "":
      products = ServicePage.objects.filter(plate_code=plate,service_date__lte=date2,phone=phone)
      mensajes = ['Ventas hasta '+date2, 'Ventas de teléfono '+phone, 'Ventas de placa '+plate]
    
    elif date1 != "" and date2 != "" and phone != "" and plate != "" and service != "":
      products = ServicePage.objects.filter(service_date__gte=date1,plate_code=plate,service_date__lte=date2,phone=phone)
      mensajes = ['Ventas desde '+date1 +" hasta "+date2, 'Ventas de teléfono '+phone,  'Ventas de placa '+plate]
      
    template_path = 'adminpages/ventasReports.html'
    print("@@@@@@@@@@@@@@@@@@@@@@")
    print(products)
    print("@@@@@@@@@@@@@@@@@@@@@@")
    context = {'ventas': products, 'messages': mensajes}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="reporte_ventas.pdf"'

    template = get_template(template_path)

    html = template.render(context)

      # create a pdf
    pisa_status = pisa.CreatePDF(
      html, dest=response)
      # if error then show some funy view
    if pisa_status.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
    if accion == "enviar":
      # Dirección de correo electrónico del remitente y destinatario
      from_email = settings.EMAIL_HOST_USER
      to_email  = request.user.email

      # Configuración del servidor SMTP
      smtp_server = 'smtp.gmail.com'
      smtp_port = 587
      smtp_username = settings.EMAIL_HOST_USER
      smtp_password = settings.EMAIL_HOST_PASSWORD

      # Crear el objeto MIMEMultipart
      msg = MIMEMultipart()
      msg['From'] = from_email
      msg['To'] = to_email
      msg['Subject'] = 'Reporte de Ventas'

      # Adjuntar el archivo PDF al correo electrónico
      attachment = MIMEBase('application', 'octet-stream')
      attachment.set_payload(response.getvalue())
      encoders.encode_base64(attachment)
      attachment.add_header('Content-Disposition', 'attachment; filename="reporte_ventas.pdf"')
      msg.attach(attachment)

      # Iniciar sesión en el servidor SMTP
      server = smtplib.SMTP(smtp_server, smtp_port)
      server.starttls()
      server.login(smtp_username, smtp_password)

      # Enviar el correo electrónico
      server.sendmail(from_email, to_email, msg.as_string())

      # Cerrar la conexión con el servidor SMTP
      server.quit()
      messages.success(request,"Correo enviado")
      return render(request,'adminpages/ventas.html',{'ventas':products})
    return response
  
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