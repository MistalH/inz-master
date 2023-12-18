import json
from django.core.management.base import BaseCommand
from Gory.models import Trasa  # Zmień na odpowiednią ścieżkę do modelu Trasa w Twojej aplikacji

class Command(BaseCommand):
    help = 'Importuj dane gór z pliku JSON.'

    def add_arguments(self, parser):
        parser.add_argument('plik_json', type=str, help='Ścieżka do pliku JSON z danymi gór.')

    def handle(self, *args, **options):
        plik_json = options['plik_json']

        try:
            with open(plik_json, 'r') as json_file:
                dane_gor = json.load(json_file)

                for data in dane_gor:
                    Trasa.objects.create(
                        identyfikator=data['identyfikator'],
                        nazwa=data['nazwa'],
                        czas_trwania=data['czas_trwania'],
                        schroniska=data['schroniska'],
                        notatka_o_szycie=data['notatka_o_szycie'],
                        wysokosc_szczytu=data['wysokosc_szczytu'],
                        kolor_szlaku=data['kolor_szlaku'],
                        pasmo_gorskie=data['pasmo_gorskie']
                    )

                self.stdout.write(self.style.SUCCESS('Dane zostały zaimportowane pomyślnie.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Błąd podczas importu danych: {str(e)}'))
