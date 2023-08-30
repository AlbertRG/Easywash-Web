from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin #for classes

# Create your views here.
class InventarioView(LoginRequiredMixin, TemplateView):
  template_name = 'adminpages/inventario.html'
  login_url = 'login'


class VentasView(LoginRequiredMixin, TemplateView):
  template_name = 'adminpages/ventas.html'
  login_url = 'login'