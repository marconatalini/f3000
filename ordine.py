from dataclasses import dataclass
from reader_interface import ReaderInterface
from serramento import Serramento

class Ordine:
    versione: int = 1
    cliente: int
    riferimento: str = ''
    commento: str = ''
    serramenti: list[Serramento] = []

    def __init__(self, file_parser: ReaderInterface) -> None:
        self.cliente = file_parser.cliente
        self.riferimento = file_parser.riferimento
        self.commento = file_parser.commento
        self.serramenti = file_parser.serramenti

    def save_to_file(self, file_out: str = ''):
        f = open(file_out,'w')
        numero_ordine = input("Numero ordine ? ")
        f.write(';\n'.join('%s' % i for i in (self.versione, self.cliente, self.riferimento, numero_ordine, self.commento,'')))
                
        id_pos = 1
        for serramento in self.serramenti: 
            f.write("{}".format(serramento.f3000_txt(id_pos)))
            id_pos += 1            
            
        f.write('P,0,0;') #fine file
        f.close()
        print(f"Salvato il file {file_out}")


