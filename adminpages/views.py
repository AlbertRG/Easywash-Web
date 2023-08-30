from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class InventarioView(TemplateView):
  template_name = 'adminpages/inventario.html'


class VentasView(TemplateView):
  template_name = 'adminpages/ventas.html'