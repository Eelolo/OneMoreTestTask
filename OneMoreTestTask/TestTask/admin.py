from django.contrib import admin
from .models import Company, Contact, Deal, DealStage, DealStatus


admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Deal)
admin.site.register(DealStage)
admin.site.register(DealStatus)
