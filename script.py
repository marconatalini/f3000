from campesato import CampesatoReader
from ordine import Ordine

# filepath_ordine = '04489 ORDINE TELAIETTI ALLUMINIO.pdf'
filepath_ordine = 'LP24120.pdf'

reader = CampesatoReader(filepath_ordine)
reader.get_all_text()

print(reader.riferimento)
print(reader.colore)
print(reader.system)

ordine = Ordine(reader)

ordine.save_to_file('CAMPESATO.txt')
