from django.contrib import admin
from .models import User, Contributor

admin.site.register(Contributor)
admin.site.register(User)
