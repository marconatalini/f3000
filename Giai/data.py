from pathlib import Path
from controller import add_to_file

def get_type_by_codice(search: str) -> int:
    path_file = Path(__file__).with_name('type_by_codice.txt')
    file_type = open(path_file)
    for line in file_type.readlines():
        try:
            codice, type = line.split(":")
        except ValueError:
            ...
        if codice == search:
            return int(type.strip())
    return add_to_file(path_file, search.strip(), 'tipologia')

    
