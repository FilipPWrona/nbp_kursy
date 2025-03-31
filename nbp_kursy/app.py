import os
import requests
import json
from datetime import datetime
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

app = Flask(__name__)

# Globalne zmienne
kursy_walut = {}
ostatnia_aktualizacja = None
scheduler = BackgroundScheduler()

def pobierz_kursy_walut():
    """
    Funkcja pobierająca kursy walut z API NBP
    i aktualizująca globalną zmienną kursy_walut
    """
    global kursy_walut, ostatnia_aktualizacja
    
    try:
        # URL do API NBP - tabela A (średnie kursy walut)
        url = "http://api.nbp.pl/api/exchangerates/tables/A?format=json"
        
        # Wysłanie zapytania GET do API
        response = requests.get(url)
        
        # Sprawdzenie czy zapytanie było udane
        if response.status_code == 200:
            # Parsowanie odpowiedzi jako JSON
            data = response.json()
            
            # Pobranie daty publikacji i kursów walut
            kursy_walut = {
                'data_publikacji': data[0]['effectiveDate'],
                'waluty': data[0]['rates']
            }
            
            ostatnia_aktualizacja = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"Kursy walut zaktualizowane: {ostatnia_aktualizacja}")
            
            # Zapisanie danych do pliku JSON
            with open('static/kursy.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'data_publikacji': kursy_walut['data_publikacji'],
                    'waluty': kursy_walut['waluty'],
                    'ostatnia_aktualizacja': ostatnia_aktualizacja,
                    'instancja': 'główna',  # Identyfikator instancji
                    'pid': os.getpid()  # ID procesu
                }, f, ensure_ascii=False, indent=4)
                
        else:
            print(f"Błąd podczas pobierania danych: {response.status_code}")
            
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def wczytaj_dane_z_pliku():
    """
    Wczytuje dane z pliku JSON, jeśli istnieje
    """
    global kursy_walut, ostatnia_aktualizacja
    try:
        if os.path.exists('static/kursy.json'):
            with open('static/kursy.json', 'r', encoding='utf-8') as f:
                dane = json.load(f)
                kursy_walut = {
                    'data_publikacji': dane['data_publikacji'],
                    'waluty': dane['waluty']
                }
                ostatnia_aktualizacja = dane['ostatnia_aktualizacja']
                print(f"Wczytano dane z pliku. Ostatnia aktualizacja: {ostatnia_aktualizacja}")
    except Exception as e:
        print(f"Błąd podczas wczytywania danych z pliku: {e}")

# Endpoint główny - strona z kursami walut
@app.route('/')
def index():
    # Zawsze wczytaj najnowsze dane z pliku przed wyświetleniem
    wczytaj_dane_z_pliku()
    return render_template('index.html', 
                          kursy=kursy_walut, 
                          ostatnia_aktualizacja=ostatnia_aktualizacja)

@app.route('/odswiez')
def odswiez():
    pobierz_kursy_walut()
    return "Dane zostały odświeżone. <a href='/'>Wróć do strony głównej</a>"

if __name__ == "__main__":
    # Upewnienie się, że katalog static istnieje
    os.makedirs('static', exist_ok=True)
    
    # Wczytanie danych z pliku, jeśli istnieją
    wczytaj_dane_z_pliku()
    
    # Inicjalne pobranie kursów walut
    pobierz_kursy_walut()
    
    # Ustawienie harmonogramu do codziennego pobierania kursów
    # Uruchamianie zadania codziennie o godzinie 16:00
    scheduler.add_job(pobierz_kursy_walut, 'cron', hour=16, minute=0)
    scheduler.start()
    
    # Uruchomienie aplikacji Flask
    app.run(debug=True, use_reloader=False) 