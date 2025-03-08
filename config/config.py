import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz klucz API z .env
REJESTR_API_KEY = os.getenv("REJESTR_API_KEY")

# Opcjonalnie: Rzucaj wyjątkiem, jeśli klucz nie jest ustawiony
if not all([REJESTR_API_KEY]):
    raise ValueError("Brakuje danych uwierzytelniających do RejestrIO. Sprawdź plik .env.")