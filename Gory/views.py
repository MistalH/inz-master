import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
from .models import *
from .forms import CreateUserForm, SzczytForm, WyruszenieOddzialuForm, ZgloszenieForm
from .forms import TrasaForm
from .forms import DodajTraseForm
from .forms import SzczytForm
from .forms import WyprawaForm
from django.core.mail import send_mail



def say_hello(requset):
   return render(requset, 'index.html')
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Konto Zostało Stworzone")

            return redirect('login_page')
    context = {'form':form}
    return render(request, 'register.html', context)

def loginPage(request):
    context = {}  # Zdefiniowanie zmiennej 'context' przed jej użyciem

    if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username=username, password=password)

      if user is not  None:
          login(request,user)
          return redirect('home')
      else:
          messages.info(request, 'Nazwa lub Hasło są niepoprawne')
    context = {}
    return render(request, 'login.html', context)
def logoutUser(request):
    logout(request)
    return redirect('login_page')

def test(requset):
   return render(requset, 'test.html')
#Nowe
from django.shortcuts import render
from .models import Trasa

from django.shortcuts import render
from .models import Trasa

@login_required
def zaplanuj_trase(request):
    if request.method == 'POST':
        szlak = request.POST.get('szlak')

        try:
            trasa = Trasa.objects.get(nazwa=szlak)
        except Trasa.DoesNotExist:
            trasa = None

        return render(request, 'trasa.html', {'trasa': trasa})

    return render(request, 'trasa.html')

@login_required
def dodaj_trase(request):
    if request.method == 'POST':
        form = DodajTraseForm(request.POST)
        if form.is_valid():
            trasa = form.save(commit=False)
            trasa.user = request.user  # Przypisz trasę do zalogowanego użytkownika
            trasa.save()
            messages.success(request, 'Trasa została dodana pomyślnie.')
            return redirect('trasa')
        else:
            messages.error(request, 'Proszę wypełnić formularz poprawnie.')
    else:
        form = DodajTraseForm()

    trasy = Trasa.objects.filter(user=request.user)  # Pobierz trasy użytkownika
    return render(request, 'trasa.html', {'form': form, 'trasy': trasy})

def dodaj_szczyt(request):
    if request.method == 'POST':
        form = SzczytForm(request.POST)
        if form.is_valid():
            szczyt = form.save()
            # Przetwarzaj dane lub podejmij inne działania, jeśli to konieczne
            return redirect('trasa')  # Przekieruj użytkownika na inną stronę po zapisaniu formularza
    else:
        form = SzczytForm()
    
    return render(request, 'trasa.html', {'form': form})

from .forms import WyprawaForm

@login_required
def dodaj_wyprawe(request):
    if request.method == 'POST':
        form = WyprawaForm(request.POST)
        if form.is_valid():
            wyprawa = form.save(commit=False)
            wyprawa.user = request.user  # Przypisanie użytkownika do wyprawy
            wyprawa.save()
            return redirect('lista_wypraw')
    else:
        form = WyprawaForm()

    return render(request, 'dodaj_wyprawe.html', {'form': form})

@login_required
def lista_wypraw(request):
    wyprawy = Wyprawa.objects.filter(user=request.user)
    return render(request, 'lista_wypraw.html', {'wyprawy': wyprawy})

@login_required
def ukoncz_wyprawe(request, wyprawa_id):
    wyprawa = Wyprawa.objects.get(id=wyprawa_id)
    wyprawa.ukonczona = not wyprawa.ukonczona  # Zmień status na przeciwny
    wyprawa.save()
    return redirect('lista_wypraw')

@login_required
def usun_wyprawe(request, wyprawa_id):
    try:
        wyprawa = Wyprawa.objects.get(id=wyprawa_id)
        wyprawa.delete()
    except Wyprawa.DoesNotExist:
         pass  # Jeśli wyprawa nie istnieje, można dodać odpowiednią obsługę błędu

    return redirect('lista_wypraw')

import smtplib
from email.mime.text import MIMEText
from django.shortcuts import render
from .forms import ZgloszenieForm 
from django.conf import settings
from django.contrib.auth.decorators import login_required
@login_required
def zgloszenie(request):
    if request.method == 'POST':
        form = ZgloszenieForm(request.POST)

        if form.is_valid():
            zgloszenie = form.save(commit=False)
            zgloszenie.user = request.user
            
            oddzial_id = request.POST.get('oddzial_ratowniczy')  # Pobranie przypisanego oddziału z formularza
            if oddzial_id:
                oddzial = OddzialRatowniczy.objects.get(pk=oddzial_id)
                zgloszenie.oddzial_ratowniczy = oddzial  # Przypisanie oddziału do zgłoszenia
            zgloszenie.save()

            # Logika wysyłania e-maila
            subject = 'Nowe zgłoszenie potrzeby pomocy'
            message = f'Zgłoszenie użytkownika {request.user.username} na trasie {zgloszenie.trasa.nazwa} wymaga natychmiastowej uwagi zespołu ratownictwa górskiego. Prosimy o niezwłoczne podjęcie działań ratunkowych i śledzenie postępu operacji.'
            from_email = 'm-hamela@wp.pl'
            recipient_list = ['michaal11123@gmail.com']

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Przypisanie oddziału ratowniczego do zgłoszenia
            oddzial_id = request.POST.get('oddzial_ratowniczy')
            if oddzial_id:
                oddzial = OddzialRatowniczy.objects.get(pk=oddzial_id)
                zgloszenie.oddzial_ratowniczy = oddzial
                zgloszenie.save()

                messages.success(request, 'Zgłoszenie zostało pomyślnie zapisane z przypisanym oddziałem.')
            else:
                messages.warning(request, 'Zgłoszenie zostało zapisane, ale brakuje przypisanego oddziału.')

            print("E-mail został wysłany pomyślnie.")
        else:
            print(form.errors)
    else:
        form = ZgloszenieForm()

    return render(request, 'zgloszenie.html', {'form': form})

from .forms import PrzydzielOddzialRatunkowyForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Zgloszenie, OddzialRatowniczy
from .forms import PrzydzielOddzialRatunkowyForm

from django.core.mail import send_mail
from django.contrib import messages

def widok_ratownika(request):
    if request.user.groups.filter(name='Ratownicy').exists():
        if request.method == 'POST':
            zgloszenie_id = request.POST.get('zgloszenie_id')
            oddzial_id = request.POST.get('oddzial_ratunkowy')

            try:
                zgloszenie = Zgloszenie.objects.get(id=zgloszenie_id)
                oddzial = OddzialRatowniczy.objects.get(id=oddzial_id)

                # Sprawdź, czy oddział jest już przypisany do innego zgłoszenia
                oddzial_is_assigned = Zgloszenie.objects.filter(oddzial_ratowniczy=oddzial).exclude(id=zgloszenie_id).exists()
                if not oddzial_is_assigned:
                    zgloszenie.oddzial_ratowniczy = oddzial
                    zgloszenie.save()
                    messages.success(request, 'Oddział został przypisany do zgłoszenia.')

                    # Wysyłanie e-maila z informacją o przypisaniu oddziału
                    subject = 'Przypisanie oddziału ratowniczego'
                    if zgloszenie.user and hasattr(zgloszenie.user, 'username'):
                        user_username = zgloszenie.user.username
                    else:
                        user_username = "Nieznany użytkownik"
                    message = f'Oddział ratowniczy {oddzial.nazwa} został przypisany do zgłoszenia użytkownika {user_username} na trasie {zgloszenie.trasa.nazwa}. Prosimy o natychmiastowe wyruszenie na miejsce zdarzenia i udzielenie pomocy w sytuacji awaryjnej. Upewnijcie się, że macie odpowiedni sprzęt ratowniczy i jesteście gotowi podjąć wszelkie niezbędne działania w celu zapewnienia bezpieczeństwa użytkownika i skutecznego przeprowadzenia akcji ratunkowej.'
                    from_email = 'michaal11123@gmail.com'  # Zmień na swój e-mail
                    recipient_list = ['michaal11123@gmail.com']  # Zmień na adres e-mail oddziału

                    send_mail(
                        subject,
                        message,
                        from_email,
                        recipient_list,
                        fail_silently=False,  # Ustaw na True, aby ukryć błędy
                    )

                else:
                    messages.error(request, 'Ten oddział jest już przypisany do innego zgłoszenia.')

            except (Zgloszenie.DoesNotExist, OddzialRatowniczy.DoesNotExist):
                messages.error(request, 'Nieprawidłowe zgłoszenie lub oddział.')

        zgloszenia = Zgloszenie.objects.all()
        oddzialy = OddzialRatowniczy.objects.filter(zgloszenie=None)
        przydziel_form = PrzydzielOddzialRatunkowyForm()

        return render(request, 'widok_ratownika.html', {'zgloszenia': zgloszenia, 'oddzialy': oddzialy, 'uzytkownik': request.user, 'przydziel_form': przydziel_form})

    else:
        return render(request, 'brak_dostepu.html')


from django.shortcuts import render, redirect
from .forms import WyruszenieOddzialuForm
from .models import OddzialRatowniczy, Zgloszenie
from django.http import JsonResponse
from django.core.mail import send_mail

def zgloszenie_wyruszenia_oddzialu(request):
    if request.method == 'POST':
        form = WyruszenieOddzialuForm(request.POST)
        if form.is_valid():
            oddzial_id = form.cleaned_data['oddzial_ratunkowy']
            oddzial = OddzialRatowniczy.objects.get(id=oddzial_id)

            zgloszenie = oddzial.zgloszenie
            zgloszenie.wyruszyl_na_pomoc = True
            zgloszenie.save()

            
            # Wysyłanie e-maila po wyruszeniu oddziału
            if zgloszenie.oddzial_ratowniczy:
                subject = 'Wyruszenie Oddziału Ratunkowego'
                message = f'Oddział {oddzial.nazwa} właśnie wyruszył na pomoc w zgłoszeniu nr {zgloszenie.id}.'
                from_email = 'michaal11123@gmail.com'  # Wpisz swój adres e-mail
                recipient_list = [zgloszenie.user.email]  # Adres e-mail użytkownika zgłaszającego

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('lista_zgloszen')  # Przekierowanie do odpowiedniego widoku
    else:
        form = WyruszenieOddzialuForm()

    return render(request, 'zgloszenie_wyruszenia_oddzialu.html', {'form': form})


from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Zgloszenie, OddzialRatowniczy
def przydziel_oddzial_ratunkowy(request):
    if request.method == 'POST':
        zgloszenie_id = request.POST.get('zgloszenie_id')
        oddzial_ids = request.POST.getlist('oddzial_ratunkowy')  # Pobierz listę przypisanych identyfikatorów oddziałów

        if zgloszenie_id and oddzial_ids:
            try:
                zgloszenie = get_object_or_404(Zgloszenie, pk=zgloszenie_id)
                oddzialy = OddzialRatowniczy.objects.filter(id__in=oddzial_ids)  # Pobierz obiekty oddziałów na podstawie identyfikatorów

                # Przypisanie wybranych oddziałów do zgłoszenia
                for oddzial in oddzialy:
                    zgloszenie.historia_oddzialow.add(oddzial)

                return JsonResponse({'status': 'success', 'oddzialy': [oddzial.nazwa for oddzial in oddzialy]})

            except Zgloszenie.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe zgłoszenie.'})
            except OddzialRatowniczy.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Nieprawidłowy oddział.'})

    return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe żądanie.'})

from django.shortcuts import render, get_object_or_404
from Gory.models import Zgloszenie


def historia_oddzialow(request, zgloszenie_id):
    zgloszenie = get_object_or_404(Zgloszenie, pk=zgloszenie_id)
    historia_oddzialow = zgloszenie.historia_oddzialow.all()

    return render(request, 'historia_oddzialow.html', {'zgloszenie': zgloszenie, 'historia_oddzialow': historia_oddzialow})


def szkolenia(request):
    return render(request, 'Szkolenia.html')