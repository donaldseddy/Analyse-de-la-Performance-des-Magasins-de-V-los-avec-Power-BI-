from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.contrib.postgres.search import SearchVectorField
from django.contrib.auth.models import AbstractUser
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut






# Create your models here.
class Localisation(models.Model):
    id = models.AutoField(primary_key=True)
    point = PointField(srid=4326, geography=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def full_address(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}"

    def save(self, *args, **kwargs):
        # Géocodage de l'adresse
        geolocator = Nominatim(user_agent="my_django_app")
        try:
            location = geolocator.geocode(self.full_address())
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
        except GeocoderTimedOut:
            pass  # ou gérer autrement

        super().save(*args, **kwargs)
    

    def save_point(self, *args, **kwargs):
        self.point = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}"
    
    # definir la longitude et latitude avec les street, city, state, zip_code
    def get_latitude_longitude(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude
        }



class Identify(models.Model):
    HOMME = 'H'
    FEMME = 'F'
    AUTRE = 'A'
    # Define the choices
    GENRE_CHOICES = [
        (HOMME, 'Homme'),
        (FEMME, 'Femme'),
        (AUTRE, 'Autre'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=255, null=True)
    genre = models.CharField(
        max_length=1,
        choices=GENRE_CHOICES,
        default=HOMME
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField()
    location = models.ForeignKey(
        Localisation, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.name} ({self.email})"
        return f"{self.name} ({self.email})"
    
    def get_full_name(self):
        if self.first_name:
            return f"{self.first_name} {self.name}"
        return self.name    

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    id =  models.IntegerField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    identify = models.ForeignKey(
        Identify, 
        on_delete=models.CASCADE
    )
    zip_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vector_search = SearchVectorField(verbose_name=["first_name", "last_name", "email", "phone"])


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    identify = models.ForeignKey(
        Identify,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model_year = models.IntegerField()
    reference = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    garanty_date = models.DateField()
    vector_search = SearchVectorField(verbose_name=["name", "category", "brand"])

    def __str__(self):
        return self.name



class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    location = models.ForeignKey(
        Localisation, 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vector_search = SearchVectorField(verbose_name=["name", "phone", "email"])

    def save(self, *args, **kwargs):
        self.geolocalization = Point()
        super().save(*args, **kwargs)


class Role(models.TextChoices):
    DIRECTEUR = 'directeur', 'Directeur'
    SOUS_DIRECTEUR = 'sous_directeur', 'Sous-Directeur'
    CHEF_EQUIPE = 'chef_equipe', "Chef d'équipe"
    EMPLOYE = 'employe', 'Employé'


class Staff(models.Model):  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True)
    manager = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_dirige',
        limit_choices_to={'role__in': [Role.DIRECTEUR, Role.SOUS_DIRECTEUR, Role.CHEF_EQUIPE]}
    ) 

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    identify = models.ForeignKey(
        Identify, 
        on_delete=models.CASCADE
    )
    Role = models.CharField(
        max_length=255,
        choices=Role.choices
    )

    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Stock(models.Model):
    product = models.ForeignKey(
        Products, 
        on_delete=models.CASCADE
    )
    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE
    )
    quantity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'store'], name='unique_product_store')
        ]

    def __str__(self):
        return f"{self.product} - {self.store}"
    




class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer= models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField()
    shipped_date = models.DateTimeField()
    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE
    )
    staff = models.ForeignKey(
        Staff, 
        on_delete=models.CASCADE
    )
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * (self.list_price - self.discount)
        super().save(*args, **kwargs)



# models/user.py
"""class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('vendeur', 'Vendeur'),
        ('livreur', 'Livreur'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
"""

