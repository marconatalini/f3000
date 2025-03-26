from pathlib import Path
from controller import add_to_file

def get_type_by_codice(search: str) -> int:
    path_file = Path(__file__).with_name('type_by_codice.txt')
    file_type = open(path_file)
    for line in file_type.readlines():
        codice, type = line.split(":")
        if codice == search:
            return int(type.strip())
    return add_to_file(path_file, search, 'tipologia')
    
def get_codice_colore(search: str) -> int:
    path_file = Path(__file__).with_name('codice_colore.txt')
    file_codice_colore = open(path_file)
    for line in file_codice_colore.readlines():
        model, cliente = line.split(":")
        if model == search:
            return int(cliente.strip())
    return add_to_file(path_file, search, 'colore')

