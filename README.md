# MiniSklep

MiniSklep to prosta aplikacja sklepu internetowego napisana w Django. Projekt obsluguje katalog produktow, szczegoly produktu, koszyk zapisany w sesji, rejestracje i logowanie uzytkownikow, panel klienta, adresy dostawy, skladanie zamowien oraz panel administratora Django.

## Technologie

- Python 3.12 lub nowszy
- Django 6.0.3
- SQLite jako lokalna baza danych
- WhiteNoise do serwowania plikow statycznych
- Pillow do obslugi obrazow

Pelna lista zaleznosci znajduje sie w pliku `requirements.txt`.

## Struktura projektu

```text
.
|-- manage.py                 # Narzedzie CLI Django
|-- requirements.txt          # Zaleznosci Pythona
|-- db.sqlite3                # Lokalna baza danych SQLite, jesli istnieje w kopii projektu
|-- MiniSklep/                # Konfiguracja projektu Django
|-- SklepApp/                 # Glowna aplikacja sklepu
|-- Templates/                # Szablony HTML
|-- static/                   # Pliki statyczne uzywane w development
|-- staticfiles/              # Wynik collectstatic
|-- media/                    # Pliki wyslane / media produktow
|-- grafika/, products/       # Dodatkowe obrazy produktow
|-- tekstowe/                 # Materialy tekstowe i starsza dokumentacja
`-- docs/                     # Dokumentacja techniczna projektu
```

## Szybkie uruchomienie

Ponizsze kroki zakladaja swieza kopie projektu.

### 1. Wejdz do katalogu projektu

```powershell
cd C:\Users\kamil\Desktop\Sklep2
```

Na Linux/macOS:

```bash
cd /sciezka/do/Sklep2
```

### 2. Utworz i aktywuj srodowisko wirtualne

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

Jezeli system ma tylko komende `python` zamiast `py` albo `python3.12`, uzyj lokalnie dostepnej komendy Pythona 3.12+.

### 3. Zainstaluj zaleznosci

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Przygotuj baze danych

Projekt korzysta z SQLite. Jezeli w repozytorium jest plik `db.sqlite3`, aplikacja moze wystartowac od razu z istniejacymi danymi. Dla czystej bazy wykonaj migracje:

```bash
python manage.py migrate
```

Opcjonalnie utworz konto administratora:

```bash
python manage.py createsuperuser
```

### 5. Uruchom serwer deweloperski

```bash
python manage.py runserver
```

Domyslnie aplikacja bedzie dostepna pod adresem:

- sklep: http://127.0.0.1:8000/
- admin Django: http://127.0.0.1:8000/admin/

## Konfiguracja

Glowny plik ustawien to `MiniSklep/settings.py`.

Najwazniejsze ustawienia:

- `SECRET_KEY` - moze byc podany przez zmienna srodowiskowa `SECRET_KEY`; jesli jej nie ma, uzywana jest wartosc deweloperska z pliku ustawien.
- `DEBUG = True` - konfiguracja deweloperska, nieprodukcyjna.
- `ALLOWED_HOSTS` - zawiera `sklep2-owtt.onrender.com`, `localhost` i `127.0.0.1`.
- `DATABASES` - SQLite w pliku `db.sqlite3`.
- `STATICFILES_DIRS` - katalog `static`.
- `STATIC_ROOT` - katalog `staticfiles`, tworzony przez `collectstatic`.
- `MEDIA_ROOT` - katalog `media`.
- `EMAIL_BACKEND` - backend konsolowy; linki resetu hasla wypisywane sa w terminalu.

Dla wdrozenia produkcyjnego ustaw przynajmniej:

```powershell
$env:SECRET_KEY="wlasny-dlugi-losowy-klucz"
```

oraz zmien `DEBUG` na `False` i dostosuj `ALLOWED_HOSTS`.

## Podstawowe komendy

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```

## Glowna funkcjonalnosc

- lista produktow na stronie glownej,
- karta szczegolow produktu,
- dodawanie do koszyka przez AJAX,
- zmiana liczby sztuk w koszyku,
- czyszczenie koszyka,
- rejestracja, logowanie i wylogowanie,
- reset hasla przez mechanizmy Django,
- panel klienta,
- edycja danych uzytkownika,
- lista zamowien i szczegoly zamowienia,
- anulowanie zamowienia, jezeli nie jest dostarczone lub anulowane,
- zarzadzanie adresami dostawy,
- skladanie zamowien z wybrana metoda platnosci; praktycznie najlepiej testowac jako zalogowany uzytkownik,
- panel admina z produktami, adresami i zamowieniami.

## Najwazniejsze adresy URL

| URL | Nazwa widoku | Opis |
| --- | --- | --- |
| `/` | `home` | Lista produktow |
| `/product/<id>/` | `item_details` | Szczegoly produktu |
| `/cart/` | `cart` | Koszyk |
| `/checkout/` | `checkout` | Finalizacja zamowienia |
| `/login/` | `login` | Logowanie |
| `/register/` | `register` | Rejestracja |
| `/panel/` | `panel` | Panel klienta |
| `/panel/dane/` | `user_data` | Dane konta |
| `/panel/adresy/` | `user_addresses` | Adresy dostawy |
| `/panel/zamowienia/` | `user_orders` | Zamowienia uzytkownika |
| `/admin/` | admin Django | Panel administracyjny |

## Dodawanie produktow

1. Uruchom migracje i utworz superusera.
2. Wejdz na http://127.0.0.1:8000/admin/.
3. Zaloguj sie kontem administratora.
4. W sekcji `Products` dodaj produkt.
5. Pole `image` przechowuje tekstowa sciezke/nazwe obrazu zgodnie z aktualna implementacja modelu.

## Dokumentacja

Szczegolowy opis architektury, modeli, przeplywow i uwag utrzymaniowych znajduje sie w pliku:

- `docs/DOKUMENTACJA.md`

## Znane uwagi

- Projekt jest obecnie skonfigurowany pod development (`DEBUG = True`).
- W repozytorium sa katalogi srodowisk wirtualnych `venv` i `.venv`; nowa osoba powinna utworzyc wlasne srodowisko zamiast polegac na istniejacych plikach.
- Model `Product.image` jest polem tekstowym, nie `ImageField`.
- Koszyk jest przechowywany w sesji jako slownik `{product_id: quantity}`.
- Reset hasla wysyla wiadomosc do konsoli, poniewaz aktywny jest `django.core.mail.backends.console.EmailBackend`.
- `checkout` nie wymaga obecnie logowania na poziomie URL, ale strona sukcesu zamowienia wymaga zalogowanego uzytkownika.
