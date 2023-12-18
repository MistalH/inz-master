from django.urls import path
from .import views

#Konfifguracjha URL
urlpatterns = [
    path('hello', views.say_hello, name='home'),
    path('register/', views.registerPage, name='register_page'),
    path('login/', views.loginPage, name='login_page'),
    path('logout/', views.logoutUser, name='logout'),
    path('test/', views.test, name='test'),
    #path('trasa/', views.zaplanuj_trase, name='zaplanuj_trase'),
    #path('trasa/', views.zaplanuj_trase, name='trasa')
    path('trasa/', views.zaplanuj_trase, name='zaplanuj_trase'),
    path('dodaj_trase/', views.dodaj_trase, name='dodaj_trase'),  # Dodaj ścieżkę do widoku dodawania trasy
    path('dodaj_szczyt/', views.dodaj_szczyt, name='dodaj_szczyt'),
    path('dodaj_wyprawe/', views.dodaj_wyprawe, name='dodaj_wyprawe'),
    path('lista_wypraw/', views.lista_wypraw, name='lista_wypraw'),
    path('ukoncz_wyprawe/<int:wyprawa_id>/', views.ukoncz_wyprawe, name='ukoncz_wyprawe'),
    path('usun_wyprawe/<int:wyprawa_id>/', views.usun_wyprawe, name='usun_wyprawe'),
    path('zgloszenie/', views.zgloszenie, name='zgloszenie'),
    path('widok_ratownika/', views.widok_ratownika, name='widok_ratownika'),
    path('widok_ratownika/<int:zgloszenie_id>/', views.widok_ratownika, name='widok_ratownika'),
    path('przydziel_oddzial_ratunkowy/', views.przydziel_oddzial_ratunkowy, name='przydziel_oddzial_ratunkowy'),
    path('historia-oddzialow/<int:zgloszenie_id>/', views.historia_oddzialow, name='historia_oddzialow'),
    path('szkolenia/', views.szkolenia, name='szkolenia'),
    




    


]