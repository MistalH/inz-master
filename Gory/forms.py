from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import OddzialRatowniczy, Szczyt, Trasa
from .models import Wyprawa
from .models import Zgloszenie
from django.contrib.auth import get_user_model
User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class TrasaForm(forms.ModelForm):
    class Meta:
        model = Trasa
        fields = ['nazwa', 'czas_trwania', 'schroniska', 'notatka_o_szycie', 'wysokosc_szczytu', 'kolor_szlaku', 'pasmo_gorskie']

class DodajTraseForm(forms.Form):
    identyfikator_trasy = forms.IntegerField(label="Identyfikator trasy")
    godzina_rozpoczecia = forms.DateTimeField(label="Godzina Rozpoczęcia")
    punkt_poczatkowy = forms.CharField(max_length=100, label="Punkt Początkowy")

    # Pobierz dostępne szczyty z bazy danych
    dostepne_szczyty = Szczyt.objects.all().values_list('nazwa', 'nazwa')
    wybierz_szczyt = forms.ChoiceField(choices=dostepne_szczyty, label="Wybierz Szczyt")


class SzczytForm(forms.ModelForm):
    class Meta:
        model = Szczyt
        fields = ['nazwa', 'godzina_wyjscia', 'punkt_na_mapie', 'godzina_zakonczenia', 'ukonczona', 'wybrany_szczyt']

class DodajSzczytForm(forms.Form):
    wybierz_szczyt = forms.ModelChoiceField(queryset=Szczyt.objects.all(), label="Wybierz Szczyt")
    
from django.forms.widgets import DateTimeInput
class WyprawaForm(forms.ModelForm):
    class Meta:
        model = Wyprawa
        fields = ['nazwa_szczytu', 'godzina_wyjscia', 'godzina_zakonczenia', 'ukonczona']
        widgets = {
            'godzina_wyjscia': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'godzina_zakonczenia': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
class ZgloszenieForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ['trasa', 'godzina_wyruszenia', 'potrzebuje_pomocy', 'oddzial_ratowniczy']
        labels = {
            'trasa': 'Trasa',
            'godzina_wyruszenia': 'Godzina wyruszenia',
            'potrzebuje_pomocy': 'Potrzebuję pomocy',
            'oddzial_ratowniczy': 'Wybierz oddział ratowniczy'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pobierz użytkownika z argumentów
        super(ZgloszenieForm, self).__init__(*args, **kwargs)

        # Pobierz oddziały, które nie są jeszcze przypisane do żadnego zgłoszenia
        oddzialy_choices = OddzialRatowniczy.objects.filter(zgloszenie__isnull=True)

        # Dodaj pole wyboru oddziału do formularza
        self.fields['oddzial_ratowniczy'] = forms.ModelChoiceField(
            queryset=oddzialy_choices,
            required=False,
            label='Wybierz oddział ratowniczy'
        )

        # Jeśli użytkownik jest zalogowany, ustaw go jako właściciela zgłoszenia
        if user and user.is_authenticated:
            self.initial['oddzial_ratowniczy'] = user


from .models import OddzialRatowniczy

class PrzydzielOddzialRatunkowyForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ['oddzial_ratowniczy']
        labels = {'oddzial_ratowniczy': 'Wybierz oddział ratunkowy'}

class WyruszenieOddzialuForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ['oddzial_ratowniczy']

    def __init__(self, *args, **kwargs):
        super(WyruszenieOddzialuForm, self).__init__(*args, **kwargs)

        # Dodaj dodatkowe pola lub zmiany w polach formularza, jeśli są potrzebne
        self.fields['oddzial_ratowniczy'].queryset = OddzialRatowniczy.objects.filter(dostepnosc=True)