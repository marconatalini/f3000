import re
from dataclasses import dataclass
from pypdf import PdfReader
from reader_interface import ReaderInterface
from serramento import Serramento
from .data import get_codice_colore, get_tabtec_by_model, get_type_by_codice


@dataclass
class CarrettaSerramento(Serramento):
    is_minima: bool = False
    is_hs_minima: bool = False
    
    def __init__(self, text: str) -> None:
        self.text = text
        self.parse_info()

    def parse_info(self) -> None:
        ...

    def get_type(self, descrizione: str) -> int:
        print(f'Cerco codice Type per {descrizione}...', end='')
        codice = get_type_by_codice(descrizione)
        print(f'trovato {descrizione}')
        return codice
    
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
            
    def get_tabella_tecnica(self, system: str, posa: str) -> int:
        return get_tabtec_by_model(f'{system} {posa}')

class CarrettaReader(ReaderInterface):

    def __init__(self, file_path: str, debug: bool = False) -> None:
        super().__init__(file_path)
        reader = PdfReader(f'{file_path}.pdf')
        number_of_pages = len(reader.pages)
        pages_to_import = self.get_number_pages(number_of_pages)
        self.text = ''
        for page in reader.pages[0:pages_to_import]:
            self.text += page.extract_text(extraction_mode='layout')
        if debug:
            self.get_all_text()

    def get_number_pages(self, total_pages: int) -> int:
        number_pages_to_import = ''
        while number_pages_to_import.isnumeric() == False:
            number_pages_to_import = input('Quante pagine vuoi importare?')
        return min(total_pages, int(number_pages_to_import))


    def get_all_text(self):
        open('debug_text.txt', 'w').write(self.text)

    @property
    def riferimento(self) -> int:
        #ORDINE DI ACQUISTO A 2400656
        return re.search(r"^ORDINE DI ACQUISTO (?P<rif>A \S+)$", self.text, re.MULTILINE).group('rif')
            
    @property
    def colore(self) -> str:
        #TELAIETTI SERRAMENTO MODELLO MODULOR 100 - FINITURA RAL 8016 OPACO LISCIO
        descrizione_colore = re.search(r"FINITURA (?P<colore>.+)$", self.text).group('colore').strip()            
        return get_codice_colore(descrizione_colore)
    
    def system(self) -> str:
        return re.search(r"TELAIETTI SERRAMENTO MODELLO (.+) -", self.text).group(1)
    
    @property
    def cliente(self) -> int:
        return 371
    
    def lista_text_posizioni(self) -> list[dict]:
        #O 2400277 002    MODULOR T75 FINESTRA 2A-DX-A/R                  1      PZ   RAL 8016 OPACO LISCIO      PIATTO 30X2mm           1270       1245       614       1180       474      1040      LU          B
        idx_testo = []
        for match in re.finditer(r"O *\d+ *(?P<rif_pos>\d{3})  +(?P<descrizione>.+\b)  +(?P<pezzi>\d{1,3})  +PZ  +(?P<colore>.+)  +(?P<coprifilo>.*)  +(?P<base>\d{2,4})  +(?P<altezza>\d{2,4})   +(?P<m3>\d{2,4})   +(?P<m4>\d{2,4})   +(?P<la>\d{2,4})   +(?P<ha>\d{2,4})  +(?P<posa>\S{2})  +\S$", self.text, re.MULTILINE):
            idx_testo.append({'start'   : match.start(),
                              'rif_pos'     :match.group('rif_pos'), 
                              'descrizione'     :match.group('descrizione'), 
                              'pezzi'   :match.group('pezzi'),
                              'colore'   :match.group('colore'),
                              'coprifilo'   :match.group('coprifilo'),
                              'base'   :match.group('base'),
                              'altezza'   :match.group('altezza'),
                              'posa'   :match.group('posa'),
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
            serr = CarrettaSerramento(pos_text)
            serr.rif_pos = posizioni[i]['rif_pos'] 
            serr.larghezza = posizioni[i]['base'] 
            serr.altezza = posizioni[i]['altezza'] 
            serr.pezzi = posizioni[i]['pezzi'] 
            serr.type = serr.get_type(posizioni[i]['descrizione'])
            serr.tabella_tecnica = serr.get_tabella_tecnica(self.system(), posizioni[i]['posa'])
            serr.colore = self.colore
            
            serramenti.append(serr)
        
        return serramenti
