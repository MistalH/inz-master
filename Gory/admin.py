from django.contrib import admin
from .models import OddzialRatowniczy, Trasa, Zgloszenie 

class TrasaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'czas_trwania', 'schroniska', 'notatka_o_szycie', 'wysokosc_szczytu', 'kolor_szlaku', 'pasmo_gorskie')

admin.site.register(Trasa, TrasaAdmin)
# Register your models here.
admin.site.register(OddzialRatowniczy)

admin.site.register(Zgloszenie)