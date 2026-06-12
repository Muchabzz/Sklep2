# Dokumentacja techniczna MiniSklep

Ten dokument opisuje projekt z perspektywy osoby, ktora widzi go pierwszy raz i chce go uruchomic, rozwijac albo wdrozyc.

## Cel aplikacji

MiniSklep jest aplikacja sklepu internetowego dla niewielkiego katalogu produktow. Uzytkownik moze ogladac produkty, dodawac je do koszyka, zalozyc konto, zapisac adres dostawy i zlozyc zamowienie. Administrator zarzadza produktami i zamowieniami przez standardowy panel Django.

## Wymagania systemowe

- Python 3.12+
- pip
- dostep do terminala
- przegladarka internetowa

Projekt uzywa Django 6.0.3, dlatego starsze wersje Pythona moga nie wystarczyc.

## Instalacja od zera

1. Sklonuj albo skopiuj projekt.
2. Wejdz do katalogu z `manage.py`.
3. Utworz srodowisko wirtualne:

```bash
python -m venv .venv
```

4. Aktywuj srodowisko:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

5. Zainstaluj zaleznosci:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

6. Wykonaj migracje:

```bash
python manage.py migrate
```

7. Utworz administratora:

```bash
python manage.py createsuperuser
```

8. Uruchom projekt:

```bash
python manage.py runserver
```

## Konfiguracja Django

Plik: `MiniSklep/settings.py`

### Aplikacje

`INSTALLED_APPS` zawiera standardowe aplikacje Django oraz `SklepApp`.

### Middleware

Projekt korzysta z `whitenoise.middleware.WhiteNoiseMiddleware`, dzieki czemu pliki statyczne moga byc serwowane prosciej po `collectstatic`.

### Szablony

Szablony znajduja sie w katalogu `Templates`, ktory jest wskazany w `TEMPLATES[0]["DIRS"]`.

### Baza danych

Domyslna baza to SQLite:

```python
BASE_DIR / "db.sqlite3"
```

Dla lokalnego developmentu to wystarcza. Przy produkcji warto rozwazyc PostgreSQL lub inna zewnetrzna baze.

### Pliki statyczne i media

- `STATIC_URL = "/static/"`
- `STATICFILES_DIRS = [BASE_DIR / "static"]`
- `STATIC_ROOT = BASE_DIR / "staticfiles"`
- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = BASE_DIR / "media"`

W development Django obsluguje media przez konfiguracje w `MiniSklep/urls.py`.

### E-mail

Aktywny jest backend konsolowy:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

Reset hasla nie wysyla prawdziwego e-maila. Tresc wiadomosci i link resetujacy pojawiaja sie w terminalu, w ktorym dziala `runserver`.

## Aplikacja `SklepApp`

### Modele

Plik: `SklepApp/models.py`

#### `Product`

Reprezentuje produkt w sklepie.

Pola:

- `name` - nazwa produktu,
- `description` - opis,
- `price` - cena,
- `availability` - czy produkt jest dostepny,
- `image` - tekstowa sciezka/nazwa obrazu.

#### `Order`

Reprezentuje zamowienie.

Pola:

- `user` - powiazany uzytkownik, opcjonalny,
- `created_at` - data utworzenia,
- `total` - suma zamowienia,
- `status` - status zamowienia,
- `payment_method` - metoda platnosci,
- `full_name`, `phone`, `street`, `postal_code`, `city` - dane dostawy.

Statusy:

- `Nowe`
- `W realizacji`
- `Wyslane`
- `Dostarczone`
- `Anulowane`

Metody platnosci:

- `Przelew`
- `Za pobraniem`
- `BLIK`

Metoda `can_cancel()` pozwala anulowac zamowienie, o ile nie jest juz dostarczone lub anulowane.

#### `OrderItem`

Pozycja zamowienia.

Pola:

- `order` - zamowienie,
- `product` - produkt,
- `quantity` - liczba sztuk,
- `price` - cena produktu w momencie skladania zamowienia.

Metoda `subtotal()` zwraca wartosc pozycji.

#### `Address`

Adres dostawy przypisany do uzytkownika.

Pola:

- `user`
- `full_name`
- `phone`
- `street`
- `postal_code`
- `city`

### Panel admina

Plik: `SklepApp/admin.py`

W adminie zarejestrowane sa:

- `Product`
- `Address`
- `Order`

Model `Order` ma inline dla `OrderItem`, filtry po statusie, metodzie platnosci i dacie oraz mozliwosc szybkiej edycji statusu z listy.

## Widoki i przeplywy

Plik: `SklepApp/views.py`

### Katalog produktow

- `home_view` pobiera wszystkie produkty i wyswietla strone glowna.
- `item_details` wyswietla szczegoly produktu, ale tylko jesli produkt ma `availability=True`.

### Koszyk

Koszyk jest trzymany w sesji pod kluczem `cart`.

Format:

```python
{
    "1": 2,
    "4": 1
}
```

Klucz to tekstowe ID produktu, wartosc to liczba sztuk.

Widoki koszyka:

- `add_to_cart` - dodaje produkt przez POST i zwraca JSON,
- `remove_from_cart` - usuwa produkt,
- `cart` - pokazuje koszyk i sume,
- `increase_quantity` - zwieksza liczbe sztuk,
- `decrease_quantity` - zmniejsza liczbe sztuk lub usuwa pozycje,
- `clear_cart` - czysci caly koszyk.

### Konta uzytkownikow

- `register_view` tworzy konto przez `UserCreationForm`, dopisuje imie, nazwisko i e-mail.
- `login_view` loguje uzytkownika i pokazuje komunikaty dla blednej nazwy lub hasla.
- `logout_view` wylogowuje.
- `delete_account_view` usuwa konto po POST.

### Panel klienta

Widoki wymagajace logowania:

- `panel_view` - podsumowanie konta, zamowien i adresow,
- `user_data_view` - edycja danych uzytkownika,
- `user_orders_view` - lista zamowien,
- `order_detail_view` - szczegoly zamowienia,
- `user_addresses_view` - lista, dodawanie i edycja adresow,
- `user_settings_view` - ustawienia konta,
- `cancel_order_view` - anulowanie zamowienia.

### Zamowienia

`checkout_view`:

1. Pobiera koszyk z sesji.
2. Jesli koszyk jest pusty, przekierowuje do koszyka.
3. Dla zalogowanego uzytkownika pobiera zapisane adresy.
4. Po POST wybiera zapisany adres albo bierze dane z formularza.
5. Liczy sume zamowienia.
6. Tworzy `Order`.
7. Tworzy powiazane `OrderItem`.
8. Czysci koszyk.
9. Przekierowuje na strone sukcesu.

`order_success_view` pokazuje potwierdzenie zamowienia.

## Routing

Plik: `SklepApp/urls.py`

Najwazniejsze trasy:

| URL | Widok | Dostep |
| --- | --- | --- |
| `/` | `home_view` | publiczny |
| `/product/<product_id>/` | `item_details` | publiczny |
| `/add-to-cart/<product_id>/` | `add_to_cart` | POST |
| `/cart/` | `cart` | publiczny |
| `/checkout/` | `checkout_view` | brak dekoratora logowania, ale przeplyw sukcesu wymaga konta |
| `/login/` | `login_view` | publiczny |
| `/register/` | `register_view` | publiczny |
| `/panel/` | `panel_view` | zalogowany |
| `/panel/dane/` | `user_data_view` | zalogowany |
| `/panel/adresy/` | `user_addresses_view` | zalogowany |
| `/panel/zamowienia/` | `user_orders_view` | zalogowany |
| `/panel/zamowienia/<order_id>/` | `order_detail_view` | zalogowany |
| `/panel/zamowienia/<order_id>/anuluj/` | `cancel_order_view` | zalogowany, POST |
| `/reset-hasla/` | `PasswordResetView` | publiczny |

`MiniSklep/urls.py` podlacza `SklepApp.urls` pod pusty prefix oraz dodaje `/admin/`.

## Szablony

Katalog: `Templates`

Wazniejsze pliki:

- `home.html` - strona glowna,
- `item_details.html` - szczegoly produktu,
- `cart.html` - koszyk,
- `checkout.html` - finalizacja zamowienia,
- `order_success.html` - potwierdzenie,
- `order_detail.html` - szczegoly zamowienia,
- `login.html` i `register.html` - konta,
- `panel.html` - panel klienta,
- `user_data.html`, `user_addresses.html`, `user_orders.html`, `user_settings.html` - podstrony panelu,
- `password_reset*.html` - reset hasla,
- `kontakt.html` - kontakt.

## Dane startowe

Projekt zawiera lokalny plik `db.sqlite3`, ale przy pracy zespolowej nie nalezy traktowac go jako jedynego zrodla prawdy. Najbezpieczniejsza procedura dla nowej osoby:

1. Uruchomic `python manage.py migrate`.
2. Utworzyc konto admina.
3. Dodac produkty przez panel `/admin/`.
4. Upewnic sie, ze obrazy produktow sa dostepne w `static`, `media`, `grafika` albo zgodnie ze sciezka wpisana w polu `image`.

## Testowanie i walidacja

Podstawowa walidacja:

```bash
python manage.py check
python manage.py migrate --check
```

W projekcie istnieje plik `SklepApp/tests.py`, ale aktualnie nie zawiera rozbudowanych testow. Przy dalszym rozwoju warto dodac testy dla:

- dodawania do koszyka,
- skladania zamowienia,
- anulowania zamowienia,
- uprawnien do szczegolow zamowien,
- edycji adresow,
- rejestracji z unikalnym e-mailem.

## Wdrozenie

Projekt zawiera `gunicorn` i `whitenoise`, co sugeruje wdrozenie w stylu Render/Heroku.

Przy wdrozeniu:

1. Ustaw zmienna `SECRET_KEY`.
2. Ustaw `DEBUG = False`.
3. Dopisz docelowa domene do `ALLOWED_HOSTS`.
4. Uruchom migracje:

```bash
python manage.py migrate
```

5. Zbierz statyki:

```bash
python manage.py collectstatic --noinput
```

6. Uruchom aplikacje przez Gunicorn:

```bash
gunicorn MiniSklep.wsgi
```

## Typowe problemy

### `ModuleNotFoundError: No module named 'django'`

Srodowisko wirtualne nie jest aktywne albo zaleznosci nie zostaly zainstalowane.

Rozwiazanie:

```bash
python -m pip install -r requirements.txt
```

### `This version of Django requires Python...`

Uzywana wersja Pythona jest za stara. Zainstaluj Python 3.12 lub nowszy i utworz srodowisko od nowa.

### Brak obrazkow produktow

Sprawdz wartosc pola `image` w produkcie oraz lokalizacje pliku. Aktualny model przechowuje sciezke jako tekst, wiec aplikacja nie wymusza automatycznego uploadu przez `ImageField`.

### Link resetu hasla nie przychodzi na e-mail

To normalne w konfiguracji deweloperskiej. Link jest wypisywany w terminalu, poniewaz aktywny jest backend konsolowy.

### Statyki nie dzialaja po wdrozeniu

Uruchom:

```bash
python manage.py collectstatic --noinput
```

Upewnij sie tez, ze `WhiteNoiseMiddleware` znajduje sie w `MIDDLEWARE`.

## Uwagi utrzymaniowe

- W `SklepApp/views.py` wystepuje podwojna definicja `checkout_view`; w Pythonie aktywna jest druga definicja, bo nadpisuje pierwsza.
- W `SklepApp/urls.py` trasa `panel/` jest zdefiniowana dwa razy.
- `checkout_view` pozwala wejsc bez logowania, ale `order_success_view` wymaga logowania i pobiera zamowienie po `user=request.user`; anonimowy checkout moze wiec wymagac poprawki, jesli ma byc oficjalnie wspierany.
- W plikach modeli/migracji widac miejscami uszkodzone kodowanie polskich znakow, np. w statusie `Wyslane`. Przed wiekszymi zmianami warto ujednolic kodowanie plikow do UTF-8.
- Katalogi `venv`, `.venv`, `staticfiles` i plik `db.sqlite3` zwykle nie powinny byc wersjonowane w repozytorium produkcyjnym.
- Przy produkcji nie nalezy trzymac sekretow w kodzie. `SECRET_KEY` powinien pochodzic ze zmiennych srodowiskowych.
