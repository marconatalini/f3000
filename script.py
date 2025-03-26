import os
import pyperclip
from Giai.reader import GiaiReader
from bricca.reader import BriccaReader
from candio.reader import CandioReader
from generic.reader import GenericReader
from icsa.reader import IcsaReader
from ordine import Ordine
from goitre import GoitreReader
from finnova import FinnovaReader
from campesato import CampesatoReader
from bminfissi import BMinfissiReader
from carretta import CarrettaReader
from cuman import CumanReader
from molaro import MolaroReader
from squizzato import SquizzatoReader

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
7 - molaro
8 - bricca (appunti)
9 - icsa (appunti)
10 - generico (pz - base x altezza - descrizione)
11 - CanDio (pdf)
12 - Squizzato (appunti)
13 - Giai (appunti)
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
    case '7':
        reader = MolaroReader(filepath_ordine, debug= True)
    case '8':
        input("Copia il testo e premi INVIO")
        reader = BriccaReader(pyperclip.paste(), debug= True)
    case '9':
        input("Copia il testo e premi INVIO")
        reader = IcsaReader(pyperclip.paste(), debug= True)
    case '10':
        input("Copia il testo e premi INVIO")
        reader = GenericReader(pyperclip.paste(), debug= True)
    case '11':
        reader = CandioReader(filepath_ordine, debug= True)
    case '12':
        reader = SquizzatoReader(pyperclip.paste(), debug= True)
    case '13':
        reader = GiaiReader(pyperclip.paste(), debug= True)
    

ordine = Ordine(reader)

ordine.save_to_file(f'{os.path.expanduser("~")}\Documents\Stampe\Export_{filename}.txt')
