from django.db import models

# Create your models here.

class Client(models.Model):
  first_name = models.CharField(max_length=150)
  last_name = models.CharField(max_length=150)
  phone = models.CharField(max_length=15, unique=True)
  email = models.EmailField(max_length=100,unique=True)
  password = models.CharField(max_length=32)
  created = models.DateField(auto_now_add=True)
  
  def __str__(self):
        return self.last_name + " " + self.first_name


class Vehicle(models.Model):
  owner = models.ForeignKey(Client, on_delete=models.CASCADE)
  plate = models.CharField(unique=True, max_length=7)
  brand = models.CharField(max_length=50)
  model = models.CharField(max_length=50)
  year = models.IntegerField()
  color = models.CharField(max_length=50)
  def __str__(self):
    return self.owner.first_name + " " + self.model
  

class Inventory(models.Model):
  name = models.CharField(max_length=200)
  sku = models.CharField(unique=True, max_length=50, default="1")
  category = models.CharField(max_length=150)
  quantity = models.IntegerField()
  expirated = models.BooleanField(default=False)
  expiration_date = models.DateField()
  
  
class Service(models.Model):
  name = models.CharField(max_length=50)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  
class ServiceTicket(models.Model):
  client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
  car = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, default=0)
  service = models.CharField(max_length=100)
  date = models.DateTimeField(auto_now_add=True)
  total = models.CharField(max_length=50,default="0")
  status = models.CharField(max_length=50)
  paymethod = models.CharField(max_length=50,default="Efectivo")

class ServicePage(models.Model):
  first_name = models.CharField(max_length=150)
  last_name = models.CharField(max_length=150)
  phone = models.CharField(max_length=15)
  type_service = models.CharField(max_length=100)
  plate_code = models.CharField(max_length=7)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  service_date = models.DateField(auto_now_add=True)
  hour_date = models.TimeField(auto_now_add=True)