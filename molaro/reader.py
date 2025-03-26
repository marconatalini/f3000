import re
from dataclasses import dataclass
from pypdf import PdfReader
from reader_interface import ReaderInterface
from serramento import Serramento

@dataclass
class MolaroSerramento(Serramento):
    
    def __init__(self, text: str) -> None:
        self.text = text
            
    def get_tabella_tecnica(self, system: str, model: str) -> int:
        return 11

class MolaroReader(ReaderInterface):

    def __init__(self, file_path: str, debug: bool = False) -> None:
        super().__init__(file_path)
        reader = PdfReader(f'{file_path}.pdf')
        number_of_pages = len(reader.pages)
        pages_to_import = 1
        self.text = ''
        for page in reader.pages[0:pages_to_import]:
            self.text += page.extract_text(extraction_mode='layout')
        if debug:
            self.get_all_text()

    def get_all_text(self):
        open('debug_text.txt', 'w').write(self.text)

    @property
    def riferimento(self) -> str:
        numero = re.search(r"ORDINE FORNITORE N.\s*(?P<numero>\d{5})", self.text, re.MULTILINE).group('numero')
        riferimento = re.search(r"RIF. (?P<rif>.+)$", self.text, re.MULTILINE).group('rif')
        return f'{numero} {riferimento}'
    
    @property
    def commento(self) -> str:
        return ""
            
    @property
    def cliente(self) -> int:
        return 273 # molaro
    
        
    @property
    def serramenti(self) -> list[Serramento]:
        s = Serramento("ELIMINAMI",999,999,1,21,90,52)
        return [s,]
