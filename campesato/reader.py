import re
from dataclasses import dataclass
from pypdf import PdfReader
from reader_interface import ReaderInterface
from serramento import Serramento
from .data import get_codice_colore, get_type_by_codice

@dataclass
class Offset:
    sx: int = 0
    dx: int = 0
    sup: int = 0
    inf: int = 0

@dataclass
class CampesatoSerramento(Serramento):
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.offset = Offset()
        self.parse_info()

    def parse_info(self) -> None:
        ...

    def get_type(self, codice: str, descrizione: str, last_type: int) -> int:
        print(f'Cerco codice Type per {descrizione}...', end='')
        codice = get_type_by_codice(codice)
        print(f'trovato {codice}')
        if '2V' in descrizione:
            self.rif_pos = 'MODIFICARE!'
        return codice
                
    def get_tabella_tecnica(self, system: str) -> int:
        match (system):
            case 'UNIPLANAR 81 R':
                return 500
            case 'REFLEX T':
                return 499

class CampesatoReader(ReaderInterface):

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        reader = PdfReader(f'{file_path}.pdf')
        number_of_pages = len(reader.pages)
        pages_to_import = self.get_number_pages(number_of_pages)
        self.text = ''
        for page in reader.pages[0:pages_to_import]:
            self.text += page.extract_text(extraction_mode='layout')

    def get_number_pages(self, total_pages: int) -> int:
        number_pages_to_import = ''
        while number_pages_to_import.isnumeric() == False:
            number_pages_to_import = input('Quante pagine vuoi importare?')
        return min(total_pages, int(number_pages_to_import))


    def get_all_text(self):
        open('debug_text.txt', 'w').write(self.text)

    @property
    def riferimento(self) -> int:
        #Riferimento               VILONE MAURO
        return re.search(r"^Riferimento +(?P<rif>.+)$", self.text, re.MULTILINE).group('rif')
            
    @property
    def colore(self) -> str:
        # Finitura Alluminio                                  RAL 9010 GOFF. OPACO RIV.ALL.
        descrizione_colore = re.search(r"^Finitura Alluminio +(?P<colore>.+)$", self.text, re.MULTILINE).group('colore').strip()            
        return get_codice_colore(descrizione_colore)

    @property
    def commento(self) -> str:
        return ''
        
    @property
    def system(self) -> str:
        # Tipo Alluminio:                                     UNIPLANAR 81 R
        return re.search(r"^Tipo Alluminio: +(?P<system>.+)$", self.text, re.MULTILINE).group('system')
    
    @property
    def cliente(self) -> int:
        return 542
    
    def lista_text_posizioni(self) -> list[dict]:
        # 7               LGFFNSTD0.1N                                                   FISSO FIN. L/A UNIPLANAR 81R                                                                                                                                              000245                                   2310 x 1705                               NR                             1          1
        idx_testo = []
        for match in re.finditer(r"^\d{1,2} +(?P<codice>\S+)  +(?P<descrizione>.+)  +(?P<variante>\d{6})  +(?P<base>\d{2,4}) x (?P<altezza>\d{2,4})  +NR  +(?P<pezzi>\d{1,2})  +(?P<rif_pos>\d{1,2})$", self.text, re.MULTILINE):
            idx_testo.append({'start': match.start(),
                              'codice':match.group('codice'), 
                              'descrizione':match.group('descrizione'), 
                              'variante':match.group('variante'), 
                              'base':match.group('base'), 
                              'altezza':match.group('altezza'), 
                              'pezzi':match.group('pezzi'),
                              'rif_pos':match.group('rif_pos')
                              })
        idx_testo.append({'start': len(self.text),'pos':None, 'pezzi':None})

        print("Trovato {} posizioni".format(len(idx_testo)-1))
        return idx_testo
        
    @property
    def serramenti(self) -> list[Serramento]:
        posizioni = self.lista_text_posizioni()
        serramenti = []
        last_type = 90 #fix

        for i in range(len(posizioni)-1):
            pos_text = self.text[posizioni[i]['start'] : posizioni[i+1]['start']]
            serramento = CampesatoSerramento(pos_text)
            serramento.rif_pos = posizioni[i]['rif_pos']
            serramento.pezzi = posizioni[i]['pezzi']
            last_type = serramento.type = serramento.get_type(posizioni[i]['codice'], posizioni[i]['descrizione'], last_type)
            serramento.larghezza = posizioni[i]['base']
            serramento.altezza = posizioni[i]['altezza']
            serramento.tabella_tecnica = serramento.get_tabella_tecnica(self.system)
            serramento.colore = self.colore
            serramenti.append(serramento)
        
        return serramenti
