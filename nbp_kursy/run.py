"""
Skrypt do uruchomienia aplikacji kursów walut jako serwis.
Można go uruchomić bezpośrednio lub przez narzędzie do zarządzania procesami (np. systemd, supervisor).
"""
import os
import sys
from app import app, pobierz_kursy_walut, scheduler

if __name__ == "__main__":
    # Ustawienie bieżącego katalogu
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Upewnienie się, że katalog static istnieje
    os.makedirs('static', exist_ok=True)
    
    # Inicjalne pobranie kursów walut
    pobierz_kursy_walut()
    
    # Uruchomienie harmonogramu
    scheduler.start()
    
    # Uruchomienie aplikacji Flask
    app.run(host='0.0.0.0', port=5000, use_reloader=False) 