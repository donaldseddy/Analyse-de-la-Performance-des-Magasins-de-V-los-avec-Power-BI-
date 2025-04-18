from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.contrib.postgres.search import SearchVectorField


# Create your models here.


"create a model for blog produit with the following fields: name, ref, description, price, latitude, longitude, longitude, geolocalization, created_at, updated_at, vector_search and a method to calculate the distance between two points using the haversine formula"
class products(models.Model):
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=15, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    geolocalization = PointField(srid=4326, geography=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vector_search = SearchVectorField(verbose_name=["name", "description"])


    def save(self, *args, **kwargs):
        self.geolocalization = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)

    def distance_to(self, other):
        return self.geolocalization.distance(other.geolocalization)
    
    def __str__(self):
        return self.name


    "create a model for blog category with the following fields: ref,name, description"
class category(models.Model):
    ref = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    

    "create a model for blog brand with the following fields: ref,name"
class brand(models.Model):
    ref =  models.IntegerField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

