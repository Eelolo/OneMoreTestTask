from django.contrib import admin
from .models import Company, Contact, Deal, DealStage, DealStatus


admin.site.register(Contact)
admin.site.register(DealStage)
admin.site.register(DealStatus)


"""
The ContactInline and DealStatusInline classes
provide editing of records of related tables 
from records of the Company and Deal models
"""


class ContactInline(admin.TabularInline):
    model = Contact


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('ownership', 'name')
    inlines = [ContactInline]


class DealStatusInline(admin.TabularInline):
    model = DealStatus


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')
    inlines = [DealStatusInline]
