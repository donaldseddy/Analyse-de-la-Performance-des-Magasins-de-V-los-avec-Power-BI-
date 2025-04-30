from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.contrib.postgres.search import SearchVectorField
from django.contrib.auth.models import AbstractUser


# Create your models here.


"""create a model for blog category with the following fields: category_id,name, description"""
class category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    

"""create a model for blog brand with the following fields: ref,name"""
class brand(models.Model):
    brand_id =  models.IntegerField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


    "create a model for customer with the following fields: customer_id, first_name,last_name, email, phone, address, city, created_at, updated_at, geolocalization,birth_date, vector_search, and a method to calculate the distance between two points using the haversine formula"
class customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=2)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    geolocalization = PointField(srid=4326, geography=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    birth_date = models.DateField()
    vector_search = SearchVectorField(verbose_name=["first_name", "last_name", "email", "phone"])

    def save(self, *args, **kwargs):
        self.geolocalization = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)

    def distance_to(self, other):
        return self.geolocalization.distance(other.geolocalization)
    
    

   
    
"create a model for blog produit with the following fields: name, description, price, category_id, brand_id, model_year, list_price, product_code, created_at, updated_at"""
class products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey(category, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(brand, on_delete=models.CASCADE)
    model_year = models.IntegerField()
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name



"""create a model for blog store with the following fields: store_id, store_name,store_phone, store_amail,store_zip_code_street, store_city, store_state, store_zip, store_country, store_phone, store_email, created_at, updated_at, geolocalization, vector_search"""
class store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    store_phone = models.CharField(max_length=15, unique=True)
    store_email = models.EmailField(unique=True)
    store_zip_code_street = models.IntegerField()
    store_city = models.CharField(max_length=255)
    store_state = models.CharField(max_length=255)
    store_zip = models.IntegerField()
    store_country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    geolocalization = PointField(srid=4326, geography=True)
    vector_search = SearchVectorField(verbose_name=["store_name", "store_phone", "store_email"])

    def save(self, *args, **kwargs):
        self.geolocalization = Point()
        super().save(*args, **kwargs)


"""create a model for blog staff with the following fields: staff_id, first_name, last_name, email, phone, store_id, active, manager_id"""
class staff(models.Model):  
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    store_id = models.ForeignKey(store, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    manager_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


"""create a model for blog stock with the following fields: (product_id, store_id,)cle compose quantity, created_at, updated_at"""	
class stock(models.Model):
    product_id = models.ForeignKey(products, on_delete=models.CASCADE)
    store_id = models.ForeignKey(store, on_delete=models.CASCADE)
    quantity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product_id', 'store_id'], name='unique_product_store')
        ]

    def __str__(self):
        return f"{self.product_id} - {self.store_id}"
    



"create a model for blog order with the following fields: order_id, customer_id, order_date, required_date, shipped_date, store_id, staff_id, status, created_at, updated_at, and a method to calculate the total amount of the order"
class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField()
    shipped_date = models.DateTimeField()
    store_id = models.ForeignKey(store, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


"""create a model for blog order_items with the following fields: order_id, item_id, product_id, quantity, list_price, discount, total_price, created_at, updated_at, and a method to calculate the total price of the order items"""
class order_items(models.Model):
    order_id = models.ForeignKey(order, on_delete=models.CASCADE)
    item_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * (self.list_price - self.discount)
        super().save(*args, **kwargs)



# models/user.py
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('vendeur', 'Vendeur'),
        ('livreur', 'Livreur'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
