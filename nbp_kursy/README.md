# Automatyzacja Pobierania Kursów Walut NBP

Projekt służy do automatycznego pobierania i wyświetlania aktualnych kursów walut z Narodowego Banku Polskiego.

## Funkcje

- Pobieranie aktualnych kursów walut z API NBP
- Zapisywanie danych do pliku JSON
- Wyświetlanie kursów w formie tabeli na stronie internetowej
- Automatyczne odświeżanie kursów codziennie o godzinie 16:00

## Wymagania

- Python 3.7+
- Biblioteki z pliku requirements.txt

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki projektu
2. Przejdź do katalogu projektu:
   ```
   cd nbp_kursy
   ```
3. Zainstaluj wymagane zależności:
   ```
   pip install -r requirements.txt
   ```

## Uruchomienie

1. Uruchom aplikację:
   ```
   python app.py
   ```
   lub
   ```
   python run.py
   ```

2. Otwórz przeglądarkę i przejdź pod adres:
   ```
   http://localhost:5000
   ```

## Ustawienie jako serwis

### Windows (Zadanie zaplanowane)

1. Otwórz Harmonogram zadań
2. Utwórz nowe zadanie
3. Ustaw wyzwalacz na uruchomienie podczas startu systemu
4. Jako akcję dodaj uruchomienie programu: `python` z argumentem ścieżka_do_projektu/run.py

### Linux (systemd)

1. Utwórz plik `/etc/systemd/system/nbp-kursy.service`:
   ```
   [Unit]
   Description=NBP Kursy Walut
   After=network.target

   [Service]
   User=twoj_uzytkownik
   WorkingDirectory=/sciezka/do/nbp_kursy
   ExecStart=/usr/bin/python3 run.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. Włącz i uruchom serwis:
   ```
   sudo systemctl enable nbp-kursy
   sudo systemctl start nbp-kursy
   ```

## Dokumentacja API NBP

Więcej informacji o API NBP można znaleźć pod adresem:
http://api.nbp.pl/

## Struktura projektu

- `app.py` - główny plik aplikacji
- `run.py` - skrypt do uruchomienia aplikacji jako serwis
- `requirements.txt` - wymagane biblioteki
- `templates/index.html` - szablon HTML dla strony z kursami
- `static/kursy.json` - zapisane dane o kursach walut 