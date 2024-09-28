import os
from pathlib import Path
from typing import TextIO

def _open_file(file_name: str) -> TextIO:
    p = Path(__file__).with_name(f'{file_name}.txt')
    return p.open('r+')

def _add_to_file(file_dati: TextIO, search: str, data_type: str, return_type: str = 'int') -> int:
    codice = input(f'Che {data_type} devo registrare per {search}? ')
    response = input(f'Vuoi aggiungere {search} al file dati? S/N ').upper()
    if response == 'S':
        file_dati.write(f'{os.linesep}{search}:{codice}')
        file_dati.close()
    if return_type != 'int':
        return codice
    return int(codice)

def get_tabtec_by_codice(search: str) -> int:
    file_type = _open_file('tabtec_by_codice')
    for l in file_type.readlines():
        codice, type = l.split(":")
        if codice == search:
            return int(type.strip())
    return _add_to_file(file_type, search, 'tabella tecnica')
    
def get_codice_colore(search: str) -> int:
    p = Path(__file__).with_name('codice_colore.txt')
    file_codice_colore = p.open('r+')
    for l in file_codice_colore.readlines():
        model, cliente = l.split(":")
        if model == search:
            return int(cliente.strip())
    return _add_to_file(file_codice_colore, search, 'colore')

