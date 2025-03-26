import re
from dataclasses import dataclass
from pypdf import PdfReader
from reader_interface import ReaderInterface
from serramento import Serramento
from .data import get_tabtec_by_model, get_type_by_codice

@dataclass
class CandioSerramento(Serramento):
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.parse_info()

    def parse_info(self) -> None:
        ...

    def get_type(self, descrizione: str) -> int:
        return get_type_by_codice(descrizione.strip())
        
    def get_misure_serramento(self, type: int) -> tuple[int,int]:
        #Misura esterno telaio:1050x1550
        larghezza, altezza = 0,0
        match = re.search(r"Misura esterno telaio:\s*(?P<larghezza>\d{3,4})x(?P<altezza>\d{3,4})", self.text, re.MULTILINE)
        # print(self.offset.sx , int(match.group('larghezza')) , self.offset.dx)
        # print(self.offset.sup , int(match.group('altezza')) , self.offset.inf)
        larghezza = int(match.group('larghezza'))
        altezza = int(match.group('altezza'))
        
        return (larghezza, altezza)
            
    def get_tabella_tecnica(self, type: int) -> int:
        return get_tabtec_by_model(f'{type}')

class CandioReader(ReaderInterface):

    def __init__(self, file_path: str, debug: bool = False) -> None:
        super().__init__(file_path)
        reader = PdfReader(f'{file_path}.pdf')
        number_of_pages = len(reader.pages)
        # pages_to_import = self.get_number_pages(number_of_pages)
        self.text = ''
        for page in reader.pages[0:number_of_pages]:
            self.text += page.extract_text(extraction_mode='layout')
        if debug:
            self.get_all_text()

    # def get_number_pages(self, total_pages: int) -> int:
    #     number_pages_to_import = ''
    #     while not number_pages_to_import.isnumeric():
    #         number_pages_to_import = input('Quante pagine vuoi importare?')
    #     return min(total_pages, int(number_pages_to_import))


    def get_all_text(self):
        open('debug_text.txt', 'w').write(self.text)

    @property
    def riferimento(self) -> int:
        #RIF. CLIENTE  : Zolin
        return re.search(r"RIF. CLIENTE\s*:\s*(?P<rif>\S*)$", self.text, re.MULTILINE).group('rif')
            
    @property
    def colore(self) -> int:
        return 52
    
    @property
    def cliente(self) -> int:
        return 407
    
    def lista_text_posizioni(self) -> list[dict]:
        #1                 ALTERNATIVA           Finestra 1 ANTA RIBALTA mod. 684                                              8  Pz                                                      00,00
        idx_testo = []
        for match in re.finditer(r"(?P<pos>\d{1,2})\s*ALTERNATIVA\s*(?P<descrizione>.*)\s+(?P<pezzi>\d{1,2})  Pz", self.text, re.MULTILINE):
            idx_testo.append({'start': match.start(),'pos':match.group('pos'), 'pezzi':match.group('pezzi'), 'descrizione': match.group('descrizione')})
        idx_testo.append({'start': len(self.text),'pos':None, 'pezzi':None, 'descrizione':None, })

        print("Trovato {} posizioni".format(len(idx_testo)-1))
        return idx_testo
        
    @property
    def serramenti(self) -> list[Serramento]:
        posizioni = self.lista_text_posizioni()
        serramenti = []
        last_type = 90 #fix

        for i in range(len(posizioni)-1):
            pos_text = self.text[posizioni[i]['start'] : posizioni[i+1]['start']]
            serramento = CandioSerramento(pos_text)
            serramento.rif_pos = posizioni[i]['pos']
            serramento.pezzi = posizioni[i]['pezzi']
            serramento.type = serramento.get_type(posizioni[i]['descrizione'])
            serramento.larghezza, serramento.altezza = serramento.get_misure_serramento(last_type)
            serramento.tabella_tecnica = serramento.get_tabella_tecnica(serramento.type)
            serramento.colore = self.colore
            serramenti.append(serramento)
        
        return serramenti
