import re
from f3000 import *
from abc import ABC

class Offset:
    sx: int
    dx: int
    su: int
    giu: int
    fix: int

    def __init__(self, sx: int, dx: int, su: int, giu: int, fix: int) -> None:
        self.sx = sx
        self.dx = dx
        self.su = su
        self.giu = giu
        self.fix = fix


class Serramento(ABC):
    txt: str = ''
    pos: int = 0
    pezzi: int = 1
    colore: str = ''
    montantino: bool = False
    minima: bool = False
    hasFrame: bool = True
    isFix: bool = False
    larghezza: int = 0
    altezza: int = 0
    tabtect: int = 0
    type: int = 0
    numero_ante: int = 0

    def __init__(self, txt_pos: str, pos: int) -> None:
        self.pos = pos
        self.txt = txt_pos
        self.type = input(f"Numero tipologia pos.{pos} : ")
        self.numero_ante = int(self.type[0])
        self.isFix = self.type in ['90', '96']
        self.larghezza, self.altezza = self.get_misure(self.get_offset())
        self.tabtec = self.get_tab_tec()

    def get_offset(self) -> Offset:
        offset_sx, offset_dx, offset_su, offset_giu, delta_offset_fix = 0,0,0,0,0
        if self.isFix: delta_offset_fix = 15
        try:
            offset_sx = int(re.search(r"(?P<mis>\d{1,3})[ ]*SX", self.txt).group('mis'))
            offset_dx = int(re.search(r"(?P<mis>\d{1,3})[ ]*DX", self.txt).group('mis'))
            offset_su = int(re.search(r"(?P<mis>\d{1,3})[ ]*SUP", self.txt).group('mis'))
            offset_giu = int(re.search(r"(?P<mis>\d{1,3})[ ]*INF", self.txt).group('mis'))  
        except AttributeError:
            pass #manca il valore INF
        return Offset(offset_sx, offset_dx, offset_su, offset_giu, delta_offset_fix)

    def get_misure(self, offset: Offset) -> list[int, int]:
        match = re.search(r"(?P<L_int_Tel>\d{3,4})x(?P<H_int_Tel>\d*)", self.txt, re.MULTILINE)        

        if self.minima:
            l_anta = int(match.group('L_int_Tel'))
            h_anta = int(match.group('H_int_Tel'))
            self.larghezza = l_anta*self.numero_ante + 4 + 102*(self.numero_ante-1) + offset.sx + offset.dx
            self.altezza = h_anta + 4 + offset.su + offset.giu
            if self.type[1] == '3': self.altezza + 66
        else:
            self.larghezza = int(match.group('L_int_Tel')) + offset.sx + offset.dx + 2*offset.fix
            self.altezza = int(match.group('H_int_Tel')) + offset.su + offset.giu + 2*offset.fix
    
    def get_altezza(self) -> int:
        system = re.search("(STONDAT|SQUADR|PARI|BAROCCO|RETT.90|68ZERO|HS-Minima)", self.txt).group(0)
        self.tabtec = self.get_tab_tec(self.get_frame_profile(), system)


    def get_frame_profile(self) -> str|None:
        m = re.search(r"MSX.*(?P<msx>(JT|AK).*) .*MDX", self.txt, re.DOTALL)
        if not m:
            self.hasFrame = False
            return None
        return m.group('msx')


    def get_tab_tec(self, find_telaio: callable, system: str) -> int:
        tt = T_TABTEC[system]
        if find_telaio in ('JTN86.00',):
            return tt + 3
        return tt

    def get_extras(self) -> str:
        extra = []
        if self.minima and not self.hasFrame:
            extra.append('T,27,2028;')
            extra.append('T,28,2028;')
            extra.append('T,29,2028;')
        
        extra.append('\n')
        return '\n'.join(extra)

    def f3000_str(self, id_pos):
        return "P,{},{pos},{larghezza},{altezza},{pezzi},{tabtec},{type},{colore};\n{}".format(id_pos, self.get_extras(), **self.__dict__)