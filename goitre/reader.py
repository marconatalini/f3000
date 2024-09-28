import re
from dataclasses import dataclass
import xlrd
from goitre.data import get_codice_colore, get_type_by_codice
from reader_interface import ReaderInterface
from serramento import Serramento


@dataclass
class GoitreSerramento(Serramento):
    pezzi: int
    larghezza: int
    altezza: int
    tabella_tecnica: int = 11

    def get_type(self, descrizione: str) -> int:
        print(f'Cerco codice Type per {descrizione}...', end='')
        codice = get_type_by_codice(descrizione)
        print(f'trovato {descrizione}')
        return codice
    
    def get_tabtec(self, codice_telaio: str) -> int:
        if codice_telaio == 'K087.145':
            return 12
        return 11
                
    
class GoitreReader(ReaderInterface):

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        book = xlrd.open_workbook(f'{file_path}.xls')
        # print("The number of worksheets is {0}".format(book.nsheets))
        # print("Worksheet name(s): {0}".format(book.sheet_names()))
        self.sheet = book.sheet_by_index(0)
        # print("{0} {1} {2}".format(self.sheet.name, self.sheet.nrows, self.sheet.ncols))
        # print("Cell D30 is {0}".format(self.sheet.cell_value(rowx=29, colx=3)))
        # for rx in range(self.sheet.nrows):
        #     print(self.sheet.row(rx))

    @property
    def riferimento(self) -> int:
        return self.sheet.cell_value(rowx=2, colx=1)
    
    @property
    def telaio(self) -> int:
        return self.sheet.cell_value(rowx=7, colx=1)
    
    @property
    def colore(self) -> str:
        descrizione_colore = self.sheet.cell_value(rowx=4, colx=1)
        return get_codice_colore(descrizione_colore)

    @property
    def commento(self) -> str:
        return ''
        
    @property
    def system(self) -> str:
        return 'Sprint 1'
    
    @property
    def cliente(self) -> int:
        return 1206
        
    @property
    def serramenti(self) -> list[Serramento]:
        serramenti = []
        for rx in range(10, self.sheet.nrows):
            if self.sheet.cell_value(rx, 0) == 'TOT ':
                break
            pezzi, larghezza, altezza, descrizione = self.sheet.row_values(rx)
            s = GoitreSerramento(pezzi, larghezza, altezza)
            s.type = s.get_type(descrizione)
            s.tabella_tecnica = s.get_tabtec(self.telaio)
            s.colore = self.colore
            serramenti.append(s)
        
        return serramenti
