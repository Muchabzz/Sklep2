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

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

Linux/macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Jeżeli na komputerze komenda Pythona nazywa się inaczej, użyj lokalnie dostępnej komendy wskazującej na Python 3.12+.

### 3. Instalacja zależności

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Przygotowanie bazy danych

```bash
python manage.py migrate
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
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```

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
