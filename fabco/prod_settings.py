from myproject.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Fabco', 'info@fabco.la'), )
MANAGERS = ADMINS

DATABASES = {}  # Appropriately for your production environment
SECRET_KEY = "..."  # Your secret key
ALLOWED_HOSTS = ["work.fabco.la", "work.fabco.la"]