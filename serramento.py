from dataclasses import dataclass

@dataclass
class Serramento:
    '''
    "P",[Numero progressivo],"Testo descr.Abbr.",[L],[H],[PZ],[Tab.Tec],[Tipol],[Colore]
    '''
    rif_pos: str = ''
    larghezza: int = 4321
    altezza: int = 4321
    pezzi: int = 1
    tabella_tecnica: int = 11
    type: int = 90
    colore: int = 51

    def get_extras(self) -> list[str]:
        '''
            "T",[N.Riga TabTec],[Valore]
            "T",....
            "A",[N.ProfiloCSM],[Lunghezza],[Pezzi]
        '''
        extra = []  
        
        extra.append('\n')
        return '\n'.join(extra)
    
    def f3000_txt(self, idx_pos: int = 1) -> str:
        return "P,{},{rif_pos},{larghezza},{altezza},{pezzi},{tabella_tecnica},{type},{colore};\n{}".format(idx_pos, self.get_extras(), **self.__dict__)
