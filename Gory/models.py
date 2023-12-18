from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms


User = get_user_model()
class Szczyt(models.Model):
    nazwa = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trasy', null=True, default=None)
    godzina_wyjscia = models.DateTimeField(null=True, blank=True)  # Godzina wyjścia
    punkt_na_mapie = models.CharField(max_length=100, null=True, blank=True)  # Punkt na mapie
    godzina_zakonczenia = models.DateTimeField(null=True, blank=True)  # Godzina zakończenia
    ukonczona = models.BooleanField(default=False)  # Pole oznaczające, czy trasa została ukończona
    wybrany_szczyt = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

class Trasa(models.Model):
    identyfikator = models.CharField(max_length=100)
    nazwa = models.CharField(max_length=100)
    czas_trwania = models.IntegerField()
    schroniska = models.TextField()
    notatka_o_szycie = models.TextField()
    wysokosc_szczytu = models.IntegerField()
    kolor_szlaku = models.CharField(max_length=50, default='Domyślny Kolor')
    pasmo_gorskie = models.CharField(max_length=50)
   

    def __str__(self):
        return self.nazwa
    
class Wyprawa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wyprawy', null=True, default=None)
    nazwa_szczytu = models.CharField(max_length=100)
    godzina_wyjscia = models.DateTimeField(null=True, blank=True)
    godzina_zakonczenia = models.DateTimeField(null=True, blank=True)
    ukonczona = models.BooleanField(default=False)
    def __str__(self):
        return f"Wyprawa na {self.nazwa_szczytu}"
    
class WyprawaForm(forms.ModelForm):
    class Meta:
        model = Wyprawa
        fields = ['nazwa_szczytu', 'godzina_wyjscia', 'godzina_zakonczenia', 'ukonczona']

class OddzialRatowniczy(models.Model):
    nazwa = models.CharField(max_length=100)
    kontakt = models.CharField(max_length=100)
    dostepnosc = models.BooleanField(default=True)
    przypisane_zgloszenia = models.ManyToManyField('Zgloszenie', related_name='przypisane_oddzialy', blank=True)

    def __str__(self):
        return self.nazwa

class Zgloszenie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zgloszenia')
    trasa = models.ForeignKey('Trasa', on_delete=models.CASCADE)
    godzina_wyruszenia = models.DateTimeField()
    potrzebuje_pomocy = models.BooleanField(default=False)
    wyruszyl_na_pomoc = models.BooleanField(default=False)
    oddzial_ratowniczy = models.ForeignKey(OddzialRatowniczy, on_delete=models.SET_NULL, null=True, blank=True)
    historia_oddzialow = models.ManyToManyField(OddzialRatowniczy, related_name='historia_zgloszen', blank=True)

    def __str__(self):
        if self.user:
            return f"Zgłoszenie użytkownika {self.user.username} na trasie {self.trasa.nazwa}"
        else:
            return f"Zgłoszenie bez przypisanego użytkownika na trasie {self.trasa.nazwa}"

    class Meta:
        ordering = ['-godzina_wyruszenia']