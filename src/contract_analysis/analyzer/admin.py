from django.contrib import admin

# Register your models here.
from .models import Contract, ContractText, ContractNatureParty, ContractCategory

admin.site.register(Contract)
admin.site.register(ContractText)
admin.site.register(ContractNatureParty)
admin.site.register(ContractCategory)