import os
# import requests
import pandas as pd

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)  # Brak limitu na liczbę kolumn
pd.set_option('display.width', None)  # Brak limitu szerokości wyświetlania
pd.set_option('display.max_rows', None)  # Opcjonalnie, wyświetlanie wszystkich wierszy

def main():

    cwd = os.getcwd()

    file_name_list = ['podmioty', 'zaklady', 'jednostki']

    for file_name in file_name_list:
        print(file_name)
        # wczytywanie pliku csv
        df = pd.read_csv(cwd + f'/data/raw/{file_name}.csv', sep=';', encoding='utf-8', dtype=str)
        # zapisywanie pliku xlsx
        df.to_excel(cwd + f'/data/interim/{file_name}.xlsx', index=False)

    print('Done!')
if __name__ == "__main__":
    main()