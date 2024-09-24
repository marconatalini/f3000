'''
Elimina spazio iniziale
Elimina spazi doppi
Elimina pos pezzi fineriga
'''

import re

def clean_txt(path: str) -> str:
    '''Read TXT file and clean it for input'''
    stream = open(path, 'r')
    testo_originale = stream.read()
    testo_a = re.sub('  *',' ',testo_originale) #spazi doppi
    testo_b = re.sub('^ ','', testo_a, flags=re.MULTILINE) #spazio iniziale
    testo_c = re.sub('^\d+ \d+ $','', testo_b, flags=re.MULTILINE) 

    return testo_c  


if __name__ == '__main__':
    t = clean_txt(r"c:\Users\marco\Documents\Stampe\1.txt")
    result = open(r"c:\Users\marco\Documents\Stampe\1_mod.txt",'w')
    result.write(t)
    result.close()