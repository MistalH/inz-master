# inz-master

**inz-master** to projekt realizowany w ramach pracy inżynierskiej, oparty na frameworku Django. Aplikacja webowa wspiera zarządzanie danymi związanymi z ratownictwem górskim, oferując moduły zarządzania górami oraz sprzętem ratowniczym.

## Funkcjonalności

- **Moduł Gór**:
  - Przechowywanie informacji o górach (nazwa, wysokość, lokalizacja).
  - Możliwość importowania danych o górach z pliku JSON za pomocą skryptu `import_gory.py`.

- **Moduł Sprzętu**:
  - Zarządzanie sprzętem używanym w ratownictwie górskim (dodawanie, edytowanie, usuwanie danych).

---

## Technologie

Projekt został stworzony przy użyciu następujących technologii:

- **Framework**: Django
- **Język programowania**: Python
- **Baza danych**: SQLite
- **Frontend**: HTML, CSS (zintegrowany z Django)

---

## Instalacja i uruchomienie

Aby uruchomić projekt lokalnie, wykonaj poniższe kroki:

1. **Klonowanie repozytorium**:
   ```bash
   git clone https://github.com/MistalH/inz-master.git
   cd inz-master
