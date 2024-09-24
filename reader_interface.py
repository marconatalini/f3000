from abc import ABC
from serramento import Serramento

class ReaderInterface(ABC):
    '''
    Nr Versione;	1
    Nr.cliente;	
    Riferimento cliente;
    Numero proprio dell'ordine;
    Commento all'ordine;
    "P",[Numero progressivo],"Testo descr.Abbr.",[L],[H],[Qt�],[Tab.Tec],[Tipol],[Colore]
    "T",[N.Riga TabTec],[Valore]
    "T",....
    "A",[N.ProfiloCSM],[Lunghezza],[Qt�]
    '''

    def __init__(self, file_path: str) -> None:
        super().__init__()

    @property
    def cliente(self) -> int:
        while True:
            codice_cliente = input('Numero Cliente? ')
            if codice_cliente.isnumeric():
                return int(codice_cliente)
    
    @property
    def riferimento(self) -> str:
        return '...'

    @property
    def commento(self) -> str:
        return f'Ordine importato con {self.__class__}'

    
    @property
    def serramenti(self) -> list[Serramento]:
        return []
    

