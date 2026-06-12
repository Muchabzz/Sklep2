# Dokumentacja Techniczna MiniSklep

## 1. Cel Dokumentu

Ten dokument jest technicznym przewodnikiem po projekcie MiniSklep. Ma umożliwić nowej osobie szybkie uruchomienie aplikacji, zrozumienie jej architektury, wykonanie podstawowej diagnostyki i bezpieczne rozpoczęcie dalszych prac.

Dokument uzupełnia główny plik [README.md](../README.md). README jest szybkim punktem wejścia, a ten plik opisuje szczegóły implementacyjne i operacyjne.

## 2. Zakres Aplikacji

MiniSklep to aplikacja sklepu internetowego oparta o Django.

Zakres funkcjonalny:

- przeglądanie produktów,
- podgląd szczegółów produktu,
- obsługa koszyka w sesji,
- rejestracja i logowanie użytkowników,
- panel klienta,
- adresy dostawy,
- składanie zamówień,
- historia i szczegóły zamówień,
- anulowanie zamówień,
- administracja produktami i zamówieniami przez panel Django.

## 3. Stos Technologiczny

| Obszar | Technologia |
| --- | --- |
| Backend | Django 6.0.3 |
| Język | Python 3.12+ |
| Baza danych | SQLite |
| Statyki | Django staticfiles + WhiteNoise |
| Media | Lokalny katalog `media` |
| Autoryzacja | Wbudowany system użytkowników Django |
| E-mail | Backend konsolowy Django |
| Serwer produkcyjny | Gunicorn, jeżeli aplikacja jest wdrażana poza `runserver` |

## 4. Struktura Katalogów

```text
.
|-- MiniSklep/
|   |-- settings.py          # Główna konfiguracja Django
|   |-- urls.py              # Główny routing projektu
|   |-- wsgi.py              # Punkt wejścia WSGI
|   `-- asgi.py              # Punkt wejścia ASGI
|-- SklepApp/
|   |-- admin.py             # Konfiguracja panelu admina
|   |-- apps.py              # Konfiguracja aplikacji
|   |-- models.py            # Modele domenowe
|   |-- urls.py              # Routing aplikacji
|   |-- views.py             # Widoki i logika przepływów
|   `-- migrations/          # Migracje bazy danych
|-- Templates/               # Szablony HTML
|-- static/                  # Źródłowe statyki
|-- staticfiles/             # Wynik `collectstatic`
|-- media/                   # Pliki użytkownika/media
|-- manage.py
|-- requirements.txt
`-- db.sqlite3
```

## 5. Uruchomienie Od Zera

### 5.1. Wymagania

- Python 3.12 lub nowszy,
- pip,
- możliwość uruchomienia komend w terminalu,
- przeglądarka internetowa.

### 5.2. Instalacja

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instalacja zależności:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Migracje:

```bash
python manage.py migrate
```

Administrator:

```bash
python manage.py createsuperuser
```

Start aplikacji:

```bash
python manage.py runserver
```

Adresy po starcie:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

## 6. Konfiguracja

Plik konfiguracyjny: [MiniSklep/settings.py](../MiniSklep/settings.py)

### 6.1. Ustawienia Bezpieczeństwa

| Ustawienie | Obecny stan | Rekomendacja |
| --- | --- | --- |
| `SECRET_KEY` | Wartość z env albo fallback w kodzie | W produkcji zawsze z env |
| `DEBUG` | `True` | W produkcji `False` |
| `ALLOWED_HOSTS` | Render, localhost, 127.0.0.1 | Dopisać realną domenę |
| SMTP | Wyłączony, backend konsolowy | Skonfigurować realny serwer poczty |

Przykład zmiennej środowiskowej:

```powershell
$env:SECRET_KEY="wlasny-dlugi-losowy-klucz"
```

### 6.2. Baza Danych

Domyślnie projekt używa SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

SQLite jest wystarczające dla lokalnego uruchomienia i prezentacji. Dla produkcji albo pracy zespołowej zalecane jest rozważenie PostgreSQL.

### 6.3. Statyki i Media

Statyki:

- źródło: `static/`,
- wynik zbierania: `staticfiles/`,
- URL: `/static/`.

Media:

- katalog: `media/`,
- URL: `/media/`.

Komenda produkcyjna:

```bash
python manage.py collectstatic --noinput
```

### 6.4. E-mail

Aktywny backend:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

Oznacza to, że reset hasła wypisuje wiadomość w terminalu zamiast wysyłać ją do realnej skrzynki.

## 7. Model Danych

Plik: [SklepApp/models.py](../SklepApp/models.py)

### 7.1. `Product`

Produkt dostępny w sklepie.

| Pole | Typ | Opis |
| --- | --- | --- |
| `name` | `CharField` | Nazwa produktu |
| `description` | `TextField` | Opis produktu |
| `price` | `DecimalField` | Cena |
| `availability` | `BooleanField` | Dostępność |
| `image` | `CharField` | Tekstowa nazwa/ścieżka obrazu |

Ważne: `image` nie jest obecnie `ImageField`, więc Django nie waliduje automatycznie uploadu obrazu.

### 7.2. `Order`

Zamówienie klienta.

| Pole | Typ | Opis |
| --- | --- | --- |
| `user` | `ForeignKey(User)` | Użytkownik, opcjonalny |
| `created_at` | `DateTimeField` | Data utworzenia |
| `total` | `DecimalField` | Suma zamówienia |
| `status` | `CharField` | Status |
| `payment_method` | `CharField` | Metoda płatności |
| `full_name` | `CharField` | Imię i nazwisko odbiorcy |
| `phone` | `CharField` | Telefon |
| `street` | `CharField` | Ulica |
| `postal_code` | `CharField` | Kod pocztowy |
| `city` | `CharField` | Miasto |

Statusy:

- `Nowe`,
- `W realizacji`,
- `Wysłane`,
- `Dostarczone`,
- `Anulowane`.

Metody płatności:

- `Przelew`,
- `Za pobraniem`,
- `BLIK`.

Metoda `can_cancel()` zwraca `False` dla zamówień dostarczonych i anulowanych.

### 7.3. `OrderItem`

Pozycja zamówienia.

| Pole | Typ | Opis |
| --- | --- | --- |
| `order` | `ForeignKey(Order)` | Zamówienie |
| `product` | `ForeignKey(Product)` | Produkt |
| `quantity` | `PositiveIntegerField` | Liczba sztuk |
| `price` | `DecimalField` | Cena w momencie zamówienia |

Metoda `subtotal()` zwraca `quantity * price`.

### 7.4. `Address`

Adres dostawy użytkownika.

| Pole | Typ | Opis |
| --- | --- | --- |
| `user` | `ForeignKey(User)` | Właściciel adresu |
| `full_name` | `CharField` | Imię i nazwisko |
| `phone` | `CharField` | Telefon |
| `street` | `CharField` | Ulica |
| `postal_code` | `CharField` | Kod pocztowy |
| `city` | `CharField` | Miasto |

## 8. Główne Przepływy

### 8.1. Przeglądanie Produktów

1. Użytkownik wchodzi na `/`.
2. `home_view` pobiera `Product.objects.all()`.
3. Szablon `home.html` renderuje listę produktów.
4. Licznik koszyka pochodzi z sesji.

### 8.2. Dodanie Produktu Do Koszyka

1. Frontend wysyła `POST` na `/add-to-cart/<product_id>/`.
2. `add_to_cart` pobiera koszyk z `request.session["cart"]`.
3. ID produktu jest zapisywane jako string.
4. Ilość jest zwiększana albo ustawiana na `1`.
5. Widok zwraca JSON z `success` i `cart_count`.

Format koszyka:

```python
{
    "1": 2,
    "4": 1
}
```

### 8.3. Finalizacja Zamówienia

1. `checkout_view` pobiera koszyk z sesji.
2. Jeżeli koszyk jest pusty, przekierowuje do `/cart/`.
3. Dla zalogowanego użytkownika pobiera zapisane adresy.
4. Po `POST` wybiera zapisany adres albo dane z formularza.
5. Liczy sumę zamówienia.
6. Tworzy `Order`.
7. Tworzy powiązane `OrderItem`.
8. Czyści koszyk.
9. Przekierowuje na stronę sukcesu zamówienia.

Uwaga techniczna: `checkout_view` nie ma dekoratora `login_required`, ale `order_success_view` wymaga zalogowanego użytkownika i filtruje zamówienie po `user=request.user`. Jeżeli anonimowy checkout ma być wspierany, ten przepływ wymaga poprawki.

### 8.4. Anulowanie Zamówienia

1. Użytkownik wchodzi w szczegóły zamówienia.
2. Formularz wysyła `POST` na `/panel/zamowienia/<order_id>/anuluj/`.
3. `cancel_order_view` sprawdza `order.can_cancel()`.
4. Jeżeli można anulować, status zmienia się na `Anulowane`.

## 9. Routing

Plik: [SklepApp/urls.py](../SklepApp/urls.py)

| URL | Widok | Dostęp |
| --- | --- | --- |
| `/` | `home_view` | publiczny |
| `/product/<product_id>/` | `item_details` | publiczny |
| `/add-to-cart/<product_id>/` | `add_to_cart` | POST |
| `/remove-from-cart/<product_id>/` | `remove_from_cart` | publiczny |
| `/cart/` | `cart` | publiczny |
| `/increase/<product_id>/` | `increase_quantity` | publiczny |
| `/decrease/<product_id>/` | `decrease_quantity` | publiczny |
| `/clear-cart/` | `clear_cart` | publiczny |
| `/checkout/` | `checkout_view` | formalnie publiczny |
| `/login/` | `login_view` | publiczny |
| `/logout/` | `logout_view` | publiczny |
| `/register/` | `register_view` | publiczny |
| `/panel/` | `panel_view` | zalogowany |
| `/panel/dane/` | `user_data_view` | zalogowany |
| `/panel/adresy/` | `user_addresses_view` | zalogowany |
| `/panel/zamowienia/` | `user_orders_view` | zalogowany |
| `/panel/zamowienia/<order_id>/` | `order_detail_view` | zalogowany |
| `/panel/zamowienia/<order_id>/anuluj/` | `cancel_order_view` | zalogowany, POST |
| `/panel/usun-konto/` | `delete_account_view` | zalogowany, POST |
| `/reset-hasla/` | `PasswordResetView` | publiczny |

## 10. Panel Administracyjny

Plik: [SklepApp/admin.py](../SklepApp/admin.py)

Zarejestrowane modele:

- `Product`,
- `Address`,
- `Order`.

`OrderAdmin` zawiera:

- listę najważniejszych pól,
- filtry po statusie, metodzie płatności i dacie,
- edycję statusu z listy,
- inline `OrderItemInline`.

## 11. Szablony

Katalog: [Templates](../Templates)

| Szablon | Rola |
| --- | --- |
| `home.html` | Strona główna |
| `item_details.html` | Szczegóły produktu |
| `cart.html` | Koszyk |
| `checkout.html` | Finalizacja zamówienia |
| `order_success.html` | Potwierdzenie zamówienia |
| `order_detail.html` | Szczegóły zamówienia |
| `login.html` | Logowanie |
| `register.html` | Rejestracja |
| `panel.html` | Panel klienta |
| `user_data.html` | Dane użytkownika |
| `user_addresses.html` | Adresy |
| `user_orders.html` | Zamówienia |
| `user_settings.html` | Ustawienia |
| `password_reset*.html` | Reset hasła |
| `kontakt.html` | Kontakt |

## 12. Dane Startowe

Projekt zawiera plik `db.sqlite3`, ale w profesjonalnym obiegu nie powinien on zastępować migracji ani danych testowych.

Zalecana procedura dla nowej osoby:

1. Uruchomić `python manage.py migrate`.
2. Utworzyć konto administratora.
3. Dodać produkty przez `/admin/`.
4. Zweryfikować ścieżki obrazów produktów.
5. Przejść testowy zakup jako zalogowany użytkownik.

## 13. Weryfikacja Po Instalacji

Po instalacji wykonaj:

```bash
python manage.py check
python manage.py migrate --check
```

Następnie ręcznie sprawdź:

- wejście na stronę główną,
- wejście do panelu admina,
- dodanie produktu,
- dodanie produktu do koszyka,
- rejestrację użytkownika,
- dodanie adresu,
- złożenie zamówienia,
- anulowanie zamówienia z panelu klienta.

## 14. Testy

W projekcie istnieje [SklepApp/tests.py](../SklepApp/tests.py), ale obecnie nie zawiera pełnego pokrycia testowego.

Rekomendowane testy automatyczne:

- model `Product`,
- dodawanie do koszyka,
- przeliczanie wartości koszyka,
- finalizacja zamówienia,
- tworzenie `OrderItem`,
- uprawnienia do zamówień,
- anulowanie zamówienia,
- walidacja rejestracji,
- widoki wymagające logowania.

## 15. Wdrożenie

Projekt zawiera `gunicorn` i `whitenoise`, więc może być uruchamiany na platformach typu Render, Heroku albo podobnych.

Minimalna procedura wdrożenia:

1. Ustawić `SECRET_KEY`.
2. Ustawić `DEBUG = False`.
3. Dodać domenę do `ALLOWED_HOSTS`.
4. Wykonać migracje:

```bash
python manage.py migrate
```

5. Zebrać statyki:

```bash
python manage.py collectstatic --noinput
```

6. Uruchomić aplikację przez Gunicorn:

```bash
gunicorn MiniSklep.wsgi
```

## 16. Checklista Produkcyjna

Przed traktowaniem projektu jako produkcyjnego należy:

- usunąć sekret z kodu i używać tylko zmiennych środowiskowych,
- ustawić `DEBUG = False`,
- zweryfikować `ALLOWED_HOSTS`,
- skonfigurować prawdziwy backend e-mail,
- zdecydować, czy checkout anonimowy ma być wspierany,
- poprawić duplikację `checkout_view`,
- usunąć duplikację trasy `panel/`,
- ujednolicić kodowanie polskich znaków w kodzie i migracjach,
- rozważyć zmianę `Product.image` na `ImageField`,
- dodać testy automatyczne,
- nie wersjonować `venv`, `.venv`, `staticfiles` i lokalnej bazy,
- przygotować dane startowe albo fixtures,
- skonfigurować backup bazy danych.

## 17. Typowe Problemy

### `ModuleNotFoundError: No module named 'django'`

Zależności nie są zainstalowane albo aktywne jest złe środowisko.

```bash
python -m pip install -r requirements.txt
```

### Django wymaga nowszego Pythona

Projekt używa Django 6.0.3. Utwórz środowisko na Pythonie 3.12+.

### Brak obrazów produktów

Sprawdź wartość pola `image` w produkcie i lokalizację pliku. Obecna implementacja przechowuje ścieżkę jako tekst.

### Reset hasła nie przychodzi na e-mail

W development to oczekiwane. Link resetujący pojawia się w terminalu, ponieważ aktywny jest backend konsolowy.

### Statyki nie działają po wdrożeniu

Uruchom:

```bash
python manage.py collectstatic --noinput
```

Sprawdź również, czy `WhiteNoiseMiddleware` znajduje się w `MIDDLEWARE`.

## 18. Uwagi Utrzymaniowe

W kodzie wykryto kilka elementów, które warto uporządkować przed dalszym rozwojem:

- [SklepApp/views.py](../SklepApp/views.py) zawiera podwójną definicję `checkout_view`; aktywna jest druga, bo nadpisuje pierwszą.
- [SklepApp/urls.py](../SklepApp/urls.py) zawiera podwójną trasę `panel/`.
- Status `Wysłane` wygląda w części plików na zapisany z uszkodzonym kodowaniem.
- `checkout_view` pozwala wejść bez logowania, ale dalszy przepływ sukcesu wymaga użytkownika.
- Obecna konfiguracja jest deweloperska, nie produkcyjna.

## 19. Sugerowana Kolejność Dalszych Prac

1. Uporządkować `checkout_view` i decyzję o anonimowym checkout.
2. Usunąć duplikację route `panel/`.
3. Naprawić kodowanie polskich znaków.
4. Dodać podstawowe testy dla koszyka i zamówień.
5. Przenieść konfigurację produkcyjną do zmiennych środowiskowych.
6. Dodać fixtures albo management command do danych startowych.
7. Rozważyć migrację obrazów produktów na `ImageField`.
