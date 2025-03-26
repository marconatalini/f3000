

import os


def add_to_file(file_dati_path: str, search: str, data_type: str, return_type: str = 'int') -> int:
    file_dati = open(file_dati_path, 'a')
    codice = input(f'Che {data_type} devo registrare per {search}? ')
    response = input(f'Vuoi aggiungere {search} al file dati? S/N ').upper()
    if response == 'S':
        file_dati.write(f'{search.strip()}:{codice}\n')
        file_dati.close()
    if return_type != 'int':
        return codice
    return int(codice)