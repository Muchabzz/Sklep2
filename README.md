# MiniSklep

Aplikacja sklepu internetowego napisana w Django. Projekt zawiera katalog produktów, koszyk oparty o sesję, konta użytkowników, panel klienta, adresy dostawy, obsługę zamówień oraz panel administracyjny Django.

## Spis Treści

- [Status Projektu](#status-projektu)
- [Wymagania](#wymagania)
- [Uruchomienie Lokalne](#uruchomienie-lokalne)
- [Konfiguracja](#konfiguracja)
- [Najważniejsze Komendy](#najważniejsze-komendy)
- [Struktura Projektu](#struktura-projektu)
- [Główne Funkcje](#główne-funkcje)
- [Adresy URL](#adresy-url)
- [Dokumentacja Techniczna](#dokumentacja-techniczna)
- [Znane Ograniczenia](#znane-ograniczenia)

## Status Projektu

Projekt jest skonfigurowany jako aplikacja deweloperska Django:

- `DEBUG = True`,
- lokalna baza danych SQLite,
- e-maile wysyłane do konsoli,
- statyki obsługiwane przez Django/WhiteNoise,
- brak rozbudowanego zestawu testów automatycznych.

Przed wdrożeniem produkcyjnym wymagane jest co najmniej ustawienie `SECRET_KEY`, wyłączenie `DEBUG`, skonfigurowanie `ALLOWED_HOSTS` i wykonanie `collectstatic`.

## Wymagania

- Python 3.12 lub nowszy
- pip
- virtualenv/venv
- przeglądarka internetowa
- terminal PowerShell, CMD, Bash albo podobny

Zależności aplikacji znajdują się w [requirements.txt](requirements.txt).

Ważne zależności:

- `Django` - framework aplikacji.
- `Pillow` - biblioteka do obsługi obrazów; przydaje się przy pracy z grafikami produktów i mediami.
- `WhiteNoise` - obsługa plików statycznych przez middleware Django.
- `certifi` - wymagane, ponieważ [MiniSklep/settings.py](MiniSklep/settings.py) importuje `certifi` przy konfiguracji certyfikatów SSL.

Przed instalacją sprawdź wersję Pythona:

Windows:

```powershell
py -0p
py -3.12 --version
```

Linux/macOS:

```bash
python3.12 --version
```

Jeżeli te komendy nie działają, najpierw zainstaluj Python 3.12+ i dodaj go do `PATH`.

## Uruchomienie Lokalne

Poniższe kroki zakładają świeżą kopię projektu.

### 1. Przejście do katalogu projektu

Windows:

```powershell
cd C:\sciezka\do\Sklep2
```

Linux/macOS:

```bash
cd /sciezka/do/Sklep2
```

### 2. Utworzenie środowiska wirtualnego

W repozytorium mogą znajdować się stare katalogi `venv` albo `.venv`. Nie używaj ich jako pewnego środowiska startowego. Najbezpieczniej utworzyć nowe, lokalne środowisko o nazwie `.venv-local`.

Windows PowerShell:

```powershell
py -3.12 -m venv .venv-local
.\.venv-local\Scripts\Activate.ps1
```

Jeżeli PowerShell blokuje aktywację skryptu, uruchom w tym samym oknie:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv-local\Scripts\Activate.ps1
```

Windows CMD:

```bat
py -3.12 -m venv .venv-local
.venv-local\Scripts\activate.bat
```

Linux/macOS:

```bash
python3.12 -m venv .venv-local
source .venv-local/bin/activate
```

Jeżeli na komputerze komenda Pythona nazywa się inaczej, użyj lokalnie dostępnej komendy wskazującej na Python 3.12+.

Po aktywacji sprawdź, czy terminal używa Pythona ze środowiska wirtualnego:

```bash
python --version
python -m pip --version
```

### 3. Instalacja zależności

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Szybka kontrola po instalacji:

```bash
python -c "import django; print(django.get_version())"
```

Oczekiwany wynik to wersja `6.0.3`.

### 4. Przygotowanie bazy danych

```bash
python manage.py migrate
```

Sprawdź konfigurację Django:

```bash
python manage.py check
```

Opcjonalnie utwórz konto administratora:

```bash
python manage.py createsuperuser
```

### 5. Uruchomienie serwera

```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresami:

- sklep: http://127.0.0.1:8000/
- panel admina: http://127.0.0.1:8000/admin/

Jeżeli port `8000` jest zajęty:

```bash
python manage.py runserver 8001
```

Wtedy aplikacja będzie dostępna pod adresem http://127.0.0.1:8001/.

### 6. Kontrola poprawnego uruchomienia

Po starcie sprawdź kolejno:

1. Wejdź na http://127.0.0.1:8000/.
2. Wejdź na http://127.0.0.1:8000/admin/.
3. Zaloguj się kontem administratora.
4. Dodaj produkt w panelu admina, jeżeli lista produktów jest pusta.
5. Wróć na stronę główną i sprawdź, czy produkt jest widoczny.
6. Dodaj produkt do koszyka.
7. Zarejestruj zwykłego użytkownika i przejdź testowy checkout jako zalogowany użytkownik.

## Konfiguracja

Główna konfiguracja znajduje się w [MiniSklep/settings.py](MiniSklep/settings.py).

Najważniejsze ustawienia:

| Ustawienie | Znaczenie |
| --- | --- |
| `SECRET_KEY` | Klucz Django. Może pochodzić ze zmiennej środowiskowej `SECRET_KEY`. |
| `DEBUG` | Obecnie `True`, czyli tryb deweloperski. |
| `ALLOWED_HOSTS` | Dozwolone hosty: Render, localhost i 127.0.0.1. |
| `DATABASES` | SQLite w pliku `db.sqlite3`. |
| `STATIC_ROOT` | Katalog wynikowy dla `collectstatic`. |
| `MEDIA_ROOT` | Katalog plików multimedialnych. |
| `EMAIL_BACKEND` | Backend konsolowy, linki resetu hasła pojawiają się w terminalu. |

Przykład ustawienia sekretu w PowerShell:

```powershell
$env:SECRET_KEY="wlasny-dlugi-losowy-klucz"
```

Przykład ustawienia sekretu w Bash:

```bash
export SECRET_KEY="wlasny-dlugi-losowy-klucz"
```

## Najważniejsze Komendy

```bash
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```

`makemigrations` uruchamiaj dopiero wtedy, gdy zmieniasz modele w `SklepApp/models.py`.

`collectstatic` nie jest wymagane do zwykłego lokalnego `runserver`; przydaje się głównie przy wdrożeniu albo testowaniu obsługi statyków przez WhiteNoise.

## Struktura Projektu

```text
.
|-- manage.py                 # Narzędzie CLI Django
|-- requirements.txt          # Zależności Pythona
|-- db.sqlite3                # Lokalna baza SQLite, jeżeli istnieje w kopii projektu
|-- MiniSklep/                # Konfiguracja projektu Django
|-- SklepApp/                 # Główna aplikacja sklepu
|-- Templates/                # Szablony HTML
|-- static/                   # Źródłowe pliki statyczne
|-- staticfiles/              # Wynik collectstatic
|-- media/                    # Pliki multimedialne
|-- grafika/, products/       # Dodatkowe obrazy produktów
|-- tekstowe/                 # Materiały pomocnicze i starsza dokumentacja
`-- docs/                     # Dokumentacja techniczna
```

## Główne Funkcje

- lista produktów,
- szczegóły produktu,
- koszyk przechowywany w sesji,
- zwiększanie, zmniejszanie i usuwanie pozycji koszyka,
- rejestracja, logowanie i wylogowanie,
- reset hasła przez wbudowane widoki Django,
- panel klienta,
- edycja danych użytkownika,
- zarządzanie adresami dostawy,
- lista zamówień i szczegóły zamówienia,
- anulowanie zamówienia, jeżeli status na to pozwala,
- finalizacja zamówienia z wyborem metody płatności,
- panel admina dla produktów, adresów i zamówień.

## Adresy URL

| URL | Nazwa | Opis |
| --- | --- | --- |
| `/` | `home` | Lista produktów |
| `/product/<id>/` | `item_details` | Szczegóły produktu |
| `/cart/` | `cart` | Koszyk |
| `/checkout/` | `checkout` | Finalizacja zamówienia |
| `/login/` | `login` | Logowanie |
| `/register/` | `register` | Rejestracja |
| `/panel/` | `panel` | Panel klienta |
| `/panel/dane/` | `user_data` | Dane konta |
| `/panel/adresy/` | `user_addresses` | Adresy dostawy |
| `/panel/zamowienia/` | `user_orders` | Zamówienia użytkownika |
| `/admin/` | Django admin | Panel administracyjny |

## Dokumentacja Techniczna

Pełniejszy opis architektury, modeli, przepływów, wdrożenia, testowania i ryzyk znajduje się tutaj:

- [docs/DOKUMENTACJA.md](docs/DOKUMENTACJA.md)

## Znane Ograniczenia

- Projekt jest w trybie deweloperskim.
- W repozytorium znajdują się katalogi `venv` i `.venv`; nowa osoba powinna utworzyć własne środowisko.
- `Product.image` jest polem tekstowym, nie `ImageField`.
- Koszyk jest przechowywany w sesji jako słownik `{product_id: quantity}`.
- Reset hasła działa przez konsolę, nie przez realny serwer SMTP.
- `checkout` nie ma dekoratora logowania, ale strona sukcesu zamówienia wymaga zalogowanego użytkownika.
- W kodzie są drobne elementy wymagające uporządkowania przed produkcją, opisane w dokumentacji technicznej.

## Najczęstsze Problemy Przy Instalacji

### `python` albo `py` nie jest rozpoznawany

Python nie jest zainstalowany albo nie został dodany do `PATH`. Zainstaluj Python 3.12+ i zaznacz opcję dodania do `PATH` w instalatorze.

### `Activate.ps1 cannot be loaded`

PowerShell blokuje uruchamianie skryptów. W tym samym oknie terminala uruchom:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Następnie ponownie aktywuj środowisko.

### `ModuleNotFoundError: No module named 'django'`

Środowisko wirtualne nie jest aktywne albo zależności nie zostały zainstalowane.

```bash
python -m pip install -r requirements.txt
```

### Strona działa, ale nie ma produktów

Utwórz superusera, wejdź do `/admin/` i dodaj produkty ręcznie.

### Reset hasła nie wysyła e-maila

To oczekiwane lokalnie. Wiadomość z linkiem resetującym pojawia się w terminalu, bo projekt używa konsolowego backendu e-mail.
