import re
from dataclasses import dataclass
from pypdf import PdfReader
from reader_interface import ReaderInterface
from serramento import Serramento
from .data import get_type_by_codice


@dataclass
class CumanSerramento(Serramento):
    is_minima: bool = False
    is_hs_minima: bool = False
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.parse_info()

    def parse_info(self) -> None:
        ...

    def get_type(self, descrizione: str) -> int:
        return get_type_by_codice(descrizione)
            
    def get_tabella_tecnica(self) -> int:
        return 34 #ET113 JTN86

class CumanReader(ReaderInterface):

    def __init__(self, clipboard: str, debug: bool = False) -> None:
        self.text = clipboard
        if debug:
            self.get_all_text()
        
    def get_all_text(self):
        open('debug_text.txt', 'w').write(self.text)

    @property
    def riferimento(self) -> int:
        return ""
            
    @property
    def colore(self) -> str:
        return 52 #RAL STD

    @property
    def cliente(self) -> int:
        return 610
    
    def lista_text_posizioni(self) -> list[dict]:
        # n.5 da 1150x1800 finestra 1 anta
        idx_testo = []
        for match in re.finditer(r"\.(?P<pezzi>\d{1,2}) da (?P<base>\d{3,4})x(?P<altezza>\d{3,4}) (?P<descrizione>.+)$", self.text, re.MULTILINE):
            idx_testo.append({
                'start': match.start(),
                'pezzi':match.group('pezzi'),
                'base':match.group('base'),
                'altezza':match.group('altezza'),
                'descrizione':match.group('descrizione').strip(),
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
            serramento = CumanSerramento(pos_text)
            serramento.rif_pos = i+1
            serramento.pezzi = posizioni[i]['pezzi']
            serramento.type = serramento.get_type(posizioni[i]['descrizione'])
            serramento.larghezza = posizioni[i]['base']
            serramento.altezza = posizioni[i]['altezza']
            serramento.tabella_tecnica = serramento.get_tabella_tecnica()
            serramento.colore = self.colore
            serramenti.append(serramento)
        
        return serramenti
