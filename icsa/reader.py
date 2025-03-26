import re
from dataclasses import dataclass
from reader_interface import ReaderInterface
from serramento import Serramento
from .data import get_type_by_codice


@dataclass
class IcsaSerramento(Serramento):
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.parse_info()

    def parse_info(self) -> None:
        ...

    def get_type(self, descrizione: str) -> int:
        return get_type_by_codice(descrizione.strip())
            
    def get_tabella_tecnica(self, sistema: str) -> int:
        match sistema:
            case "concept":
                return 82
            case "evo28":
                return 153
        return 493

class IcsaReader(ReaderInterface):
    sistema: str = ""

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
        m = input("""Scegli sistema:
                  1 - coibent alu
                  2 - climatop
                  3 - concept   
                  4 - Evo 2.8               
                  """)
        match m:
            case "1":
                self.sistema = "coibent"
            case "2":
                self.sistema = "climatop"
                return 2530
            case "3":
                self.sistema = "concept"
            case "4":
                self.sistema = "evo28"
        return 285
    
    def lista_text_posizioni(self) -> list[dict]:
        # N° 02		  880 X 2290	Porta finestra I anta, soglia, zoccolo A070.071 X 2
        # 1	1600	X	2550	PF2 + 1 zoccolo
        idx_testo = []
        for match in re.finditer(r"(?P<pezzi>\d{1,2})\s+(?P<base>\d{3,4})\s*[X|x]*\s*(?P<altezza>\d{3,4})\s+(?P<descrizione>.+)$", self.text, re.MULTILINE):
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
            serramento = IcsaSerramento(pos_text)
            serramento.rif_pos = i+1
            serramento.pezzi = posizioni[i]['pezzi']
            serramento.type = serramento.get_type(posizioni[i]['descrizione'])
            serramento.larghezza = posizioni[i]['base']
            serramento.altezza = posizioni[i]['altezza']
            serramento.tabella_tecnica = serramento.get_tabella_tecnica(self.sistema)
            serramento.colore = self.colore
            serramenti.append(serramento)
        
        return serramenti


