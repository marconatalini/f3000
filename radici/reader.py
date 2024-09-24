import re
from dataclasses import dataclass
from pypdf import PdfReader
from reader_interface import ReaderInterface
from serramento import Serramento


@dataclass
class RadiciSerramento(Serramento):
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.parse_info()

    def parse_info(self) -> None:
        self.get_offset()
        self.is_minima = bool(re.search(r"Allum +Minima", self.text, re.MULTILINE))
        self.is_hs_minima = bool(re.search(r"HS-Minima", self.text, re.MULTILINE))

    def get_type(self, rif_pos: str, last_type: int) -> int:
        type = input(f'Tipologia pos.{rif_pos}? ')
        if type == '': return last_type
        return int(type)
        
    def get_misure_serramento(self, type: int) -> tuple[int,int]:
        larghezza, altezza = 0,0
        match = re.search(r"(?P<larghezza>\d{3,4})x *(?P<altezza>\d{3,4})", self.text, re.MULTILINE)
        larghezza = self.offset.sx + int(match.group('larghezza')) + self.offset.dx
        altezza = self.offset.sup + int(match.group('altezza')) + self.offset.inf
    
        if self.is_minima:
            sormonto_ch = 102
            n_ante = type // 100
            is_porta = 40 > (type - (type // 100)*100) > 29
            larghezza = self.offset.sx + int(match.group('larghezza')) * n_ante + self.offset.dx + sormonto_ch * (n_ante -1) + 4
            altezza = self.offset.sup + int(match.group('altezza')) + self.offset.inf + 4 + 66 * (is_porta)
            return (larghezza, altezza)
        
        return (larghezza, altezza)
            
    def get_tabella_tecnica(self, system: str, model: str) -> int:
        if self.is_minima:
            return 483
        if self.type in [911,912] and self.is_hs_minima:
            return 231

class RadiciReader(ReaderInterface):

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        reader = PdfReader(file_path)
        number_of_pages = len(reader.pages)
        print(f'File di {number_of_pages} pagine.')
        pages_to_import = self.get_number_pages(number_of_pages)
        self.text = ''
        for page in reader.pages[0:pages_to_import]:
            self.text += page.extract_text(extraction_mode='plain')

    def get_number_pages(self, total_pages: int) -> int:
        number_pages_to_import = ''
        while number_pages_to_import.isnumeric() == False:
            number_pages_to_import = input('Quante pagine vuoi importare?')
        return min(total_pages, int(number_pages_to_import))

    def get_all_text(self):
        print(len(self.text))
        open('debug_text.txt', 'w').write(self.text)

    @property
    def riferimento(self) -> int:
        return 'NP'
            
    @property
    def colore(self) -> int:
        colore = input("Colore RAL? S/N").upper()
        if colore == 'S':
            return 52 #RAL
        return 46 #DECOR

    @property
    def cliente(self) -> int:
        return 267 #RADICI ENZO
    
    def lista_text_posizioni(self) -> list[dict]:
        idx_testo = []
        for match in re.finditer(r"^ *(?P<pos>\d{1,2}) (?P<pezzi>\d{1,2}).+\d - ", self.text, re.MULTILINE):
            idx_testo.append({'start': match.start(),'pos':match.group('pos'), 'pezzi':match.group('pezzi')})
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
            serramento = RadiciSerramento(pos_text)
            serramento.rif_pos = posizioni[i]['pos']
            serramento.pezzi = posizioni[i]['pezzi']
            last_type = serramento.type = serramento.get_type(serramento.rif_pos, last_type)
            serramento.larghezza, serramento.altezza = serramento.get_misure_serramento(last_type)
            serramento.tabella_tecnica = serramento.get_tabella_tecnica(self.system(), self.model())
            serramento.colore = self.colore
            serramenti.append(serramento)
        
        return serramenti
