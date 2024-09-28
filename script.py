import os
from ordine import Ordine
from goitre import GoitreReader
from finnova import FinnovaReader
from campesato import CampesatoReader
from bminfissi import BMinfissiReader

BASE_PATH = '/Users/marco/Downloads/lavoro'

print(
    """
1 - finnova
2 - campesato
3 - goitre
4 - bm infissi
"""
)
choice = input('Quale reader vuoi usare?: ')
filename = input('Nome del file? ')
filepath_ordine = os.path.join(BASE_PATH, filename)

match choice:
    case '1':
        reader = FinnovaReader(filepath_ordine)
    case '2':
        reader = CampesatoReader(filepath_ordine)
    case '3':
        reader = GoitreReader(filepath_ordine)
    case '4':
        reader = BMinfissiReader(filepath_ordine, debug=True)

ordine = Ordine(reader)

ordine.save_to_file(f'Export_{filename}.txt')
