import re
from dataclasses import dataclass
from pypdf import PdfReader
from reader_interface import ReaderInterface
from serramento import Serramento
from .data import get_codice_cliente_by_model, get_codice_colore, get_tabtec_by_model, get_telaio_pattern_by_model

@dataclass
class Offset:
    sx: int = 0
    dx: int = 0
    sup: int = 0
    inf: int = 0

@dataclass
class FinnovaSerramento(Serramento):
    is_minima: bool = False
    is_hs_minima: bool = False
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.offset = Offset()
        self.parse_info()

    def parse_info(self) -> None:
        self.get_offset()
        self.is_minima = bool(re.search(r"Allum +Minima", self.text, re.MULTILINE))
        self.is_hs_minima = bool(re.search(r"HS-Minima", self.text, re.MULTILINE))

    def get_type(self, rif_pos: str, last_type: int) -> int:
        type = input(f'Tipologia pos.{rif_pos}? ')
        if type == '': return last_type
        return int(type)
    
    def get_offset(self) -> Offset:
        sx = re.search(r"(\d{2,3}) SX", self.text, re.MULTILINE)
        if sx: self.offset.sx = int(sx.group(1))
        dx = re.search(r"(\d{2,3}) DX", self.text, re.MULTILINE)
        if dx: self.offset.dx = int(dx.group(1))
        sup = re.search(r"(\d{2,3}) SUP", self.text, re.MULTILINE)
        if sup: self.offset.sup = int(sup.group(1))
        inf = re.search(r"(\d{2,3}) INF", self.text, re.MULTILINE)
        if inf: self.offset.inf = int(inf.group(1))
    
    def get_misure_serramento(self, type: int) -> tuple[int,int]:
        larghezza, altezza = 0,0
        match = re.search(r"(?P<larghezza>\d{3,4})x *(?P<altezza>\d{3,4})", self.text, re.MULTILINE)
        # print(self.offset.sx , int(match.group('larghezza')) , self.offset.dx)
        # print(self.offset.sup , int(match.group('altezza')) , self.offset.inf)
        larghezza = self.offset.sx + int(match.group('larghezza')) + self.offset.dx
        altezza = self.offset.sup + int(match.group('altezza')) + self.offset.inf
    
        if self.is_minima:
            sormonto_ch = 102
            n_ante = type // 100
            is_porta = 40 > (type - (type // 100)*100) > 29
            larghezza = self.offset.sx + int(match.group('larghezza')) * n_ante + self.offset.dx + sormonto_ch * (n_ante -1) + 4
            altezza = self.offset.sup + int(match.group('altezza')) + self.offset.inf + 4 + 66 * (is_porta)
            return (larghezza, altezza)
        
        if type == 90 and not self.is_minima: #FIX
            larghezza += 30
            altezza += 30
        
        return (larghezza, altezza)
            
    def get_tabella_tecnica(self, system: str, model: str) -> int:
        if self.is_minima:
            return 483
        if self.type in [911,912] and self.is_hs_minima:
            return 231
        pattern = get_telaio_pattern_by_model(model)
        match_telai = re.findall(pattern, self.text, re.MULTILINE)
        telaio = max(match_telai, key=match_telai.count)
    
        return get_tabtec_by_model(f'{system} {model} {telaio}')

class FinnovaReader(ReaderInterface):

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
        return re.search(r"Comm:( )*(?P<rif>\d{5})", self.text, re.MULTILINE).group('rif')
            
    @property
    def colore(self) -> str:
        descrizione_colore = re.search(r"Finitura: *ALLUMINIO (?P<colore>.{20,40}) ", self.text).group('colore').strip()            
        return get_codice_colore(descrizione_colore)
    
    def system(self) -> str:
        return re.search(r"(A.FIN LA |A.FIN LA88 |A.FIX LA |A.FIX LA88 |A.BIL LA |A.SCOR LA |A.SCOR LA88 |A.FIN 68ZERO)", self.text).group(0)
    
    def model(self) -> str:
        return re.search("(STONDAT|SQUADR|PARI|BAROCCO|RETT.90|Minima)", self.text).group(0)

    @property
    def cliente(self) -> int:
        system = self.system()
        model = self.model()
        cliente = get_codice_cliente_by_model(f'{system} {model}')
        return cliente
    
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
            serramento = FinnovaSerramento(pos_text)
            serramento.rif_pos = posizioni[i]['pos']
            serramento.pezzi = posizioni[i]['pezzi']
            last_type = serramento.type = serramento.get_type(serramento.rif_pos, last_type)
            serramento.larghezza, serramento.altezza = serramento.get_misure_serramento(last_type)
            serramento.tabella_tecnica = serramento.get_tabella_tecnica(self.system(), self.model())
            serramento.colore = self.colore
            serramenti.append(serramento)
        
        return serramenti
