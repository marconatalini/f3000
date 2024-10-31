import os
import pyperclip
from ordine import Ordine
from goitre import GoitreReader
from finnova import FinnovaReader
from campesato import CampesatoReader
from bminfissi import BMinfissiReader
from carretta import CarrettaReader
from cuman import CumanReader

# BASE_PATH = '/Users/marco/Downloads/lavoro'
BASE_PATH = r'c:\Users\marco\Documents\Stampe\lavoro'

print(
    """
1 - finnova
2 - campesato
3 - goitre
4 - bm infissi
5 - carretta
6 - cuman (appunti)
"""
)

choice = input('Quale reader vuoi usare?: ')
if choice != '6': 
    filename = input('Nome del file? ')
    filepath_ordine = os.path.join(BASE_PATH, filename)
else:
    filename = 'cuman'

match choice:
    case '1':
        reader = FinnovaReader(filepath_ordine, debug= True)
    case '2':
        reader = CampesatoReader(filepath_ordine, debug= True)
    case '3':
        reader = GoitreReader(filepath_ordine)
    case '4':
        reader = BMinfissiReader(filepath_ordine, debug= True)
    case '5':
        reader = CarrettaReader(filepath_ordine, debug= True)
    case '6':
        input("Copia il testo e premi INVIO")
        reader = CumanReader(pyperclip.paste(), debug= True)


ordine = Ordine(reader)

ordine.save_to_file(f'Export_{filename}.txt')
