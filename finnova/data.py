import os
from pathlib import Path
from typing import TextIO

def _open_file(file_name: str) -> TextIO:
    p = Path(__file__).with_name(f'{file_name}.txt')
    return p.open('r+')

def _add_to_file(file_dati: TextIO, search: str, data_type: str, return_type: str = 'int') -> int:
    response = input(f'Vuoi aggiungere {search} al file dati? S/N ').upper()
    if response == 'S':
        codice = input(f'Che {data_type} devo registrare? ')
        file_dati.write(f'{os.linesep}{search}:{codice}')
    file_dati.close()
    if return_type != 'int':
        return codice
    return int(codice)

def get_codice_cliente_by_model(search: str) -> int:
    file_codice_cliente = _open_file('codice_cliente_by_model')
    for l in file_codice_cliente.readlines():
        model, cliente = l.split(":")
        if model == search:
            return int(cliente.strip())
    _add_to_file(file_codice_cliente, search, 'cliente')
    
def get_codice_colore(search: str) -> int:
    p = Path(__file__).with_name('codice_colore.txt')
    file_codice_colore = p.open('r+')
    for l in file_codice_colore.readlines():
        model, cliente = l.split(":")
        if model == search:
            return int(cliente.strip())
    _add_to_file(file_codice_colore, search, 'colore')

def get_tabtec_by_model(search: str) -> int:
    p = Path(__file__).with_name('tabtec_by_model.txt')
    file_codice_colore = p.open('r+')
    for l in file_codice_colore.readlines():
        model, cliente = l.split(":")
        if model == search:
            return int(cliente.strip())
    _add_to_file(file_codice_colore, search, 'tabella tecnica')

def get_telaio_pattern_by_model(search: str) -> str:
    p = Path(__file__).with_name('pattern_telaio_by_model.txt')
    file_pattern_telaio = p.open('r+')
    for l in file_pattern_telaio.readlines():
        model, pattern = l.split(":")
        if model == search:
            return pattern.strip()
    _add_to_file(file_pattern_telaio, search, 'pattern', return_type='str')

    
