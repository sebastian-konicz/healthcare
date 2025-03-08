import os
import requests
import json
import pandas as pd
from config.config import REJESTR_API_KEY

# Twój klucz API z FoodData Central
BASE_URL = f'https://rejestr.io/api/v2/org/{id}'

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)  # Brak limitu na liczbę kolumn
pd.set_option('display.width', None)  # Brak limitu szerokości wyświetlania
pd.set_option('display.max_rows', None)  # Opcjonalnie, wyświetlanie wszystkich wierszy

def registry(nip):

    id = f'nip{nip}'
    rozdzial = 'oddzialy'
    BASE_URL = f'https://rejestr.io/api/v2/org/{id}'
    # BASE_URL = f'https://rejestr.io/api/v2/org/{id}/krs-powiazania'
    # BASE_URL = f'https://rejestr.io/api/v2/org/{id}/krs-dokumenty'

    # BASE_URL = f'https://rejestr.io/api/v2/org/{id}/krs-rozdzialy/{rozdzial}'

    print(BASE_URL)

    headers = {
        "Authorization": f"{REJESTR_API_KEY}",  # Jeśli API używa Bearer Token
        "Content-Type": "application/json",
    }

    response = requests.get(BASE_URL, headers=headers)

    print(response)

    if response.status_code == 200:
        data = response.json()
        print(data)
        # Zapisz surową odpowiedź do pliku JSON, jeśli save_response jest True
        if data:
            with open('raw_response.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("Surowa odpowiedź zapisana do pliku 'raw_response.json'")
    else:
        print(f"Błąd: {response.status_code}")
        data = {"nip": nip, "note": "brak danych"}

    return data

def create_dataframe(data):
    """
    Funkcja tworzy DataFrame z informacji o produkcie spożywczym.

    :param food: Produkt spożywczy o najwyższym score.
    :return: DataFrame z informacjami o produkcie.
    """
    # Pobierz podstawowe informacje
    numery = data.get('numery', {})
    nazwy = data.get('nazwy', {})
    adres = data.get('adres', {})
    glowna_osoba = data.get('glowna_osoba', {})
    kontakt = data.get('kontakt', {})

    # numery
    krs = numery.get('krs', None)
    regon = numery.get('regon', None)

    # nazwy
    nazwa_pelna = nazwy.get('pelna', None)
    nazwa_skrocona = nazwy.get('skrocona', None)

    # adres
    ulica = adres.get('ulica', None)
    nr_domu = adres.get('nr_domu', None)
    nr_mieszkania = adres.get('nr_mieszkania', None)
    kod = adres.get('kod', None)
    miejscowosc = adres.get('miejscowosc', None)
    panstwo = adres.get('panstwo', None)
    teryt = adres.get('teryt', {})

    # teryt
    wojewodztwo = teryt.get('wojewodztwo', None)
    powiat = teryt.get('powiat', None)
    gmina = teryt.get('gmina', None)

    # glowna_osoba
    glowna_osoba = glowna_osoba.get('imiona_i_nazwisko', None)

    # kontakt
    emaile = kontakt.get('emaile', None)
    www = kontakt.get('www', None)

    print(krs)

    # Połącz wszystkie dane w jeden słownik
    data = {
        'krs': krs,
        'nip': nip,
        'regon': regon,
        'nazwa_pelna': nazwa_pelna,
        'nazwa_skrocona': nazwa_skrocona,
        'ulica': ulica,
        'nr_domu': nr_domu,
        'nr_mieszkania': nr_mieszkania,
        'kod_pocztowy': kod,
        'miejscowosc': miejscowosc,
        'panstwo': panstwo,
        'wojewodztwo': wojewodztwo,
        'powiat': powiat,
        'gmina': gmina,
        'glowna_osoba': glowna_osoba,
        'emaile': emaile,
        'www': www,
        'note': data.get('note', None)
    }

    # Utwórz DataFrame z jednego wiersza
    df = pd.DataFrame([data])

    print(df)
    return df


if __name__ == "__main__":
    cwd = str(os.getcwd())

    nip_data = pd.read_excel(cwd + '/data/combined/nip_sample.xlsx', dtype=str)
    nip_list = nip_data['nip'].tolist()
    print(nip_list)

    df_list = []
    # nip = '8942814132'
    # nip = '8942686384'
    for nip in nip_list:
        data = registry(nip)
        df_nip = create_dataframe(data)
        df_list.append(df_nip)

    df = pd.concat(df_list)

    df.to_excel(cwd + f'/data/final/registry_data.xlsx', index=False)

    # if top_food:
    #     df = create_food_dataframe(top_food)
    #     print(df)
    # else:
    #     print("Nie znaleziono produktów.")