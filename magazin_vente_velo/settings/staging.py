from .base import *
import dj_database_url
from .base import config

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {

    'default': dj_database_url.parse(
        
        config("DATABASE_URL"),
        conn_max_age=600,  # optionnel, pour les connexions persistantes
        engine='django.contrib.gis.db.backends.postgis'
    
    )
}

