import re
from dataclasses import dataclass
from reader_interface import ReaderInterface
from serramento import Serramento
from .data import get_type_by_codice


@dataclass
class SquizzatoSerramento(Serramento):
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.parse_info()

    def parse_info(self) -> None:
        ...

    def get_type(self) -> int:
        type: int = 100
        if self.larghezza > 1000:
            type = 200
        if self.larghezza > 1800:
            type = 300
        if self.altezza > 2000:
            type += 30
        return type            

class SquizzatoReader(ReaderInterface):
    sistema: str = ""
    tabella_tecnica: int = 122

    def __init__(self, clipboard: str, debug: bool = False) -> None:
        self.text = clipboard
        self.sistema = input("Sistema? Legno, Alu, Alu parziale?").strip()
        if debug:
            self.get_all_text()
        
    def get_all_text(self):
        open('debug_text.txt', 'w').write(self.text)

    @property
    def riferimento(self) -> int:
        return ""
            
    @property
    def colore(self) -> str:
        return 72 #KIT + RAL STD

    @property
    def cliente(self) -> int:
        return 532
    
    def lista_text_posizioni(self) -> list[dict]:
        # N° 02		  880 X 2290	Porta finestra I anta, soglia, zoccolo A070.071 X 2
        # pz 2     110x145    2 a
        idx_testo = []
        for match in re.finditer(r"pz\s*(?P<pezzi>\d{1,2})\s+(?P<base>\d{2,4})\s*[X|x]*\s*(?P<altezza>\d{2,4}).*$", self.text, re.MULTILINE):
            idx_testo.append({
                'start': match.start(),
                'pezzi':match.group('pezzi'),
                'base':match.group('base'),
                'altezza':match.group('altezza'),
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
            serramento = SquizzatoSerramento(pos_text)
            serramento.rif_pos = i+1
            serramento.pezzi = posizioni[i]['pezzi']
            serramento.larghezza = int(posizioni[i]['base'])*10
            serramento.altezza = int(posizioni[i]['altezza'])*10
            serramento.type = serramento.get_type()
            serramento.tabella_tecnica = self.tabella_tecnica
            serramento.colore = self.colore
            serramenti.append(serramento)
        
        return serramenti


