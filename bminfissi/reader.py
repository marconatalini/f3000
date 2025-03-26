import re
from dataclasses import dataclass
from pypdf import PdfReader
from reader_interface import ReaderInterface
from serramento import Serramento
from .data import get_codice_colore, get_tabtec_by_codice

@dataclass
class BMinfissiSerramento(Serramento):
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.parse_info()

    def parse_info(self) -> None:
        ...

    def get_type(self, ante: str, altezza: str, note: str) -> int:
        codice = 0
        match ante:
            case 'CF':
                return 90
            case '1':
                codice = 100
            case '2':
                codice = 200
        if eval(altezza) > 2000 and codice < 900:
            codice += 30
        if codice == 0:
            return input(f"Non so che tipologia usare per {note}, ante:{ante} altezza:{altezza}. Inserisci il numero: ")
        return codice
                
    def get_tabella_tecnica(self, system: str, type: int) -> int:
        return get_tabtec_by_codice(f'{system} type {type}')
    
class BMinfissiReader(ReaderInterface):

    def __init__(self, file_path: str, debug: bool = False) -> None:
        super().__init__(file_path)
        reader = PdfReader(f'{file_path}.pdf')
        # number_of_pages = len(reader.pages)
        self.text = ''
        for page in reader.pages:
            self.text += page.extract_text(extraction_mode='layout')
        if debug:
            self.get_all_text()

    def get_all_text(self):
        open('debug_text.txt', 'w').write(self.text)

    @property
    def riferimento(self) -> int:
        # Oggetto: richiesta di preventivo rif. PERESANI
        return re.search(r"richiesta di preventivo rif. (?P<rif>.+)$", self.text, re.MULTILINE).group('rif')
            
    @property
    def colore(self) -> str:
        # rivestimento in alluminio tinta
        descrizione_colore = re.search(r"rivestimento in alluminio tinta\s+(?P<colore>\S+)", self.text, re.MULTILINE).group('colore').strip()            
        return get_codice_colore(descrizione_colore)

    @property
    def commento(self) -> str:
        return ''
        
    @property
    def system(self) -> str:
        # (con vostro profilo EVO 2.8 da 93)
        return re.search(r"\(con vostro profilo (?P<system>.+)\)", self.text, re.MULTILINE).group('system')
    
    @property
    def cliente(self) -> int:
        return 2642
    
    def lista_text_posizioni(self) -> list[dict]:
        #   n. 1            1460        x    1600         ante 1  wasistas
        # n. 6            5300        x     2250        ante 2 alzante scorrevole
        #             2                          3                       1.320                        300                             CF
        idx_testo = []
        for match in re.finditer(r"^\s*.* (?P<pos>\d{1,2})\s+(?P<pezzi>\d{1,2})\s+(?P<base>\S{2,5})\s+(?P<altezza>\S{2,5})\s+(?P<ante>\S+)\s*(?P<note>\S*)$", self.text, re.MULTILINE):
            idx_testo.append({'start': match.start(),
                              'pos':match.group('pos'), 
                              'pezzi':match.group('pezzi'), 
                              'base':match.group('base'), 
                              'altezza':match.group('altezza'), 
                              'ante':match.group('ante'),
                              'note':match.group('note')
                              })
        idx_testo.append({'start': len(self.text),'pos':None, 'pezzi':None})

        print("Trovato {} posizioni".format(len(idx_testo)-1))
        return idx_testo
        
    @property
    def serramenti(self) -> list[Serramento]:
        posizioni = self.lista_text_posizioni()
        serramenti = []

        for i in range(len(posizioni)-1):
            pos_text = self.text[posizioni[i]['start'] : posizioni[i+1]['start']]
            serramento = BMinfissiSerramento(pos_text)
            serramento.pezzi = posizioni[i]['pezzi']
            serramento.rif_pos = posizioni[i]['pos']
            serramento.type = serramento.get_type(posizioni[i]['ante'], posizioni[i]['altezza'], posizioni[i]['note'])
            serramento.larghezza = posizioni[i]['base']
            serramento.altezza = posizioni[i]['altezza']
            serramento.tabella_tecnica = serramento.get_tabella_tecnica(self.system, serramento.type)
            serramento.colore = self.colore
            serramenti.append(serramento)
        
        return serramenti
