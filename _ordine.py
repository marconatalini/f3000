import re
import sys
import txt_tools
from _serramento import Serramento
from f3000 import *

class Ordine():
    txt: str = ''
    riferimento: str = ''
    colore: str = ''
    isMinima: bool = True
    hasMontantino: bool = False
    system: str
    type: str
    cliente: int = 562
    idx_testo: list = []
    serramenti: list[Serramento] = []
    note: str = ''


    def __init__(self, path_pdf_text: str) -> None:
        self.txt = txt_tools.clean_txt(path_pdf_text)
        try:
            print(f"{'Riferimento':20} : ", end='')
            self.riferimento = re.search(r"^Comm:( )*(?P<rif>\d{5})", self.txt, re.MULTILINE).group('rif')
            print(self.riferimento)
            print(f"{'Colore':20} : ", end='')
            colore = re.search(r"ALLUMINIO .*(?P<colore>(RAL|M\d{1})) ", self.txt).group('colore')
            print(colore)
            print(f"{'System':20} : ", end='')
            self.system = re.search(r"(A.FIN LA |A.FIN LA88 |A.FIX LA |A.FIX LA88 |A.BIL LA |A.SCOR LA |A.SCOR LA88 |A.FIN 68ZERO)", self.txt).group(0)
            print(self.system)
            print(f"{'Type':20} : ", end='')
            self.type = re.search("(STONDAT|SQUADR|PARI|BAROCCO|RETT.90|Minima)", self.txt).group(0)
            print(self.type)
            print(f"{'IsMinima':20} : ", end='')
            self.isMinima = bool(re.search("Allum Minima", self.txt, re.MULTILINE|re.IGNORECASE))
            print(self.isMinima)

        except AttributeError:
            print('ERRORE parsing file...')
            sys.exit(1)
        
        self.colore = T_COLORE_RIV_ALLUMINIO[colore]
        if self.isMinima and colore == 'RAL': self.colore += 20 #KIT+RAL

        for match in re.finditer(r"^(?P<pos>\d{1,2}) (?P<pezzi>\d{1,2})", self.txt, re.MULTILINE):
            self.idx_testo.append({'start': match.start(),'pos':match.group('pos'), 'pezzi':match.group('pezzi')})
        self.idx_testo.append({'start': len(self.txt),'pos':None, 'pezzi':None})

        print("Trovato {} posizioni".format(len(self.idx_testo)-1))

        for i in range(len(self.idx_testo)-1):
            serramento = Serramento(self.txt[self.idx_testo[i]['start']:self.idx_testo[i+1]['start']], self.idx_testo[i]['pos'])
            serramento.pezzi = self.idx_testo[i]['pezzi']
            serramento.colore = self.colore
            serramento.montantino = self.hasMontantino
            serramento.minima = self.isMinima
            
            self.serramenti.append(serramento)

    def save(self, file_out: str, filever=1):
        f = open(file_out,'w')
        numero_ordine = input("Numero ordine ? ")
        f.write(';\n'.join('%s' % i for i in (filever, self.cliente, self.riferimento, numero_ordine, self.note,'')))
               
        id_pos = 1
        for serramento in self.serramenti: 
            f.write("{}".format(serramento.f3000_str(id_pos)))
            id_pos += 1            
            
        f.write('P,0,0;') #fine file
        f.close()
        print(f"Salvato il file {file_out}")