import os
from pathlib import Path
from typing import TextIO
from controller import add_to_file

def _open_file(file_name: str) -> TextIO:
    p = Path(__file__).with_name(f'{file_name}.txt')
    return p.open('r+')

def get_tabtec_by_codice(search: str) -> int:
    file_type = _open_file('tabtec_by_codice')
    for l in file_type.readlines():
        codice, type = l.split(":")
        if codice == search:
            return int(type.strip())
    return add_to_file(file_type, search, 'tabella tecnica')
    
def get_codice_colore(search: str) -> int:
    p = Path(__file__).with_name('codice_colore.txt')
    file_codice_colore = p.open('r+')
    for l in file_codice_colore.readlines():
        model, cliente = l.split(":")
        if model == search:
            return int(cliente.strip())
    return add_to_file(file_codice_colore, search, 'colore')

