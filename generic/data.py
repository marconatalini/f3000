from pathlib import Path
from controller import add_to_file

def get_type_by_codice(search: str) -> int:
    file_path = Path(__file__).with_name('type_by_codice.txt')
    data_file = open(file_path)

    for line in data_file.readlines():
        try:
            codice, type = line.split(":")
        except ValueError:
            ...
        if codice == search:
            return int(type.strip())
    return add_to_file(file_path, search.strip(), 'tipologia')

    
