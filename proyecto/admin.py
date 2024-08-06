from django.contrib import admin
from .models import Proyecto, BudgetItem, ItemSolicitud

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(BudgetItem)
admin.site.register(ItemSolicitud)