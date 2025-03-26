from pathlib import Path
from controller import add_to_file

def get_codice_cliente_by_model(search: str) -> int:
    file_path = Path(__file__).with_name('codice_cliente_by_model.txt')
    file_codice_cliente = open(file_path)
    for line in file_codice_cliente.readlines():
        model, cliente = line.split(":")
        if model == search:
            return int(cliente.strip())
    return add_to_file(file_path, search, 'cliente')
    
def get_codice_colore(search: str) -> int:
    file_path = Path(__file__).with_name('codice_colore.txt')
    file_codice_colore = open(file_path)
    for line in file_codice_colore.readlines():
        model, cliente = line.split(":")
        if model == search:
            return int(cliente.strip())
    return add_to_file(file_path, search, 'colore')

def get_tabtec_by_model(search: str) -> int:
    file_path = Path(__file__).with_name('tabtec_by_model.txt')
    file_codice_colore = open(file_path)
    for line in file_codice_colore.readlines():
        model, cliente = line.split(":")
        if model == search:
            return int(cliente.strip())
    return add_to_file(file_path, search, 'tabella tecnica')

def get_telaio_pattern_by_model(search: str) -> str:
    file_path = Path(__file__).with_name('pattern_telaio_by_model.txt')
    file_pattern_telaio = open(file_path)
    for l in file_pattern_telaio.readlines():
        model, pattern = l.split(":")
        if model == search:
            return pattern.strip()
    return add_to_file(file_path, search, 'pattern', return_type='str')

    
