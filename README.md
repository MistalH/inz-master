# Praca inżynierska

**inz-master** to projekt realizowany w ramach pracy inżynierskiej, oparty na frameworku Django. Aplikacja webowa wspiera zarządzanie danymi związanymi z ratownictwem górskim, oferując moduły zarządzania górami oraz sprzętem ratowniczym.

---

## 📂 Struktura katalogu `Gory/`

Katalog `Gory/` zawiera moduł Django odpowiedzialny za zarządzanie danymi górskimi. Znajdują się tutaj pliki obsługujące modele, widoki, formularze oraz skrypty pomocnicze.

### 📁 Zawartość katalogu:
- **`migrations/`** – Pliki migracji bazy danych dla aplikacji Gory.
- **`templates/`** – Szablony HTML dla interfejsu użytkownika.
- **`__init__.py`** – Plik inicjalizacyjny modułu Django.
- **`admin.py`** – Konfiguracja panelu administracyjnego Django dla modułu Gory.
- **`apps.py`** – Definicja aplikacji Gory w Django.
- **`forms.py`** – Formularze Django używane w aplikacji Gory.
- **`import_gory.py`** – Skrypt do importowania danych o górach z pliku JSON.
- **`models.py`** – Definicja modeli bazy danych dla gór.
- **`tests.py`** – Testy jednostkowe dla modułu Gory.
- **`urls.py`** – Konfiguracja tras URL dla aplikacji Gory.
- **`views.py`** – Logika widoków obsługujących żądania HTTP dla aplikacji Gory.

---

## 🚀 Instalacja i uruchomienie

Aby uruchomić projekt lokalnie, wykonaj poniższe kroki:

1. **Klonowanie repozytorium**:
   ```bash
   git clone https://github.com/MistalH/inz-master.git
   cd inz-master
2.**Utworzenie wirtulanego środowiska**
  ```python
  python3 -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows
```
3.**Wykonanie Migracji bazy danych**
python manage.py migrate
4. **Uruchomienie środowiska Deweloperskiego**
```
python manage.py runserver
```
Aplikacja będzie dostępna pod adresem: http://127.0.0.1:8000/.


## 📌 Technologie

Projekt został stworzony przy użyciu następujących technologii:

- **Framework**: Django  
- **Język programowania**: Python  
- **Baza danych**: SQLite  
- **Frontend**: HTML, CSS (zintegrowany z Django)  

---

## 👨‍💻 Autor

- **MistalH**  
  GitHub: [MistalH](https://github.com/MistalH)  
