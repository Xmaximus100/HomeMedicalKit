from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Medicine, SideEffect, Substance, MedicineName

class SideEffectInline(admin.TabularInline):
    model = SideEffect
    extra = 1

class SubstanceInline(admin.TabularInline):
    model = Substance
    extra = 1

class MedicineAdmin(admin.ModelAdmin):
    inlines = [SideEffectInline, SubstanceInline]
    list_display = ['name', 'purpose', 'quantity', 'expiration_date']
    search_fields = ['name__name', 'purpose']

admin.site.register(Medicine, MedicineAdmin)
admin.site.register(SideEffect)
admin.site.register(Substance)
admin.site.register(MedicineName)