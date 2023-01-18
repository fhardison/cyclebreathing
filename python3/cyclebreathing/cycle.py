
import vim
from greek_normalisation.utils import nfc, nfd
from greek_accentuation.characters import add_breathing, Breathing,Accent, add_diacritic 
import re

class Cycle():
    def __init__(self):
        self.ACCENTS = [chr(int(x, 16)) for x in ['0301', '0300', '0342']]
        self.BREATHINGS = [chr(int(x, 16)) for x in ['0313', '0314']]
        self.SMOOTH = self.BREATHINGS[0]
        self.DAERESIS = chr(int('0308', 16))

        # IOTA SUBSCRIPT is last but is 0345

        self.VOWELS = [x for x in "αεηιυοω"]
        self.DIPTHONGS = [x for x in "αι ει ου ευ αυ ηυ οι".split(' ')] 

    # canonical order is letter < breathing < accent < iota subscript

    def fix_text(self, text):
        out = []
        for w in nfd(text).split(' '):
            #VV
            if w[0:2] in self.DIPTHONGS:
                if len(w) > 2:
                #already has breathing mark
                    if w[2] in self.BREATHINGS:
                        out.append(w)
                    #needs smooth
                    elif w[2] in self.ACCENTS:
                        w = w[0:2] + self.SMOOTH +  w[2:]
                        out.append(w)
                    else:
                        out.append(w[0:2] + self.SMOOTH + w[2:])
                else:
                    out.append(w + self.SMOOTH)
            #VA
            elif w[0] in self.VOWELS and w[1] in self.ACCENTS:

                if len(w) < 3:
                    out.append((w[0:1] + self.SMOOTH + w[1:]))
                elif w[2] not in self.BREATHINGS:
                    out.append((w[0:1] + self.SMOOTH + w[1:]))
                else:
                    out.append(w)
            #VVAB
            #VVD
            elif len(w) > 2 and w[0] in self.VOWELS and w[2] == self.DAERESIS:
                out.append((w[0] + self.SMOOTH + w[1:]))
            elif w[0] in self.VOWELS:
                if len(w) == 1:
                    out.append(w[0] + self.SMOOTH)
                elif w[1] not in self.BREATHINGS:
                    out.append((w[0] + self.SMOOTH + w[1:]))
                elif w[1] in self.ACCENTS:
                    out.append((w[0] + self.SMOOTH + w[1:]))
                else:
                    out.append(w)
                    print(w)
            else: 
                out.append(w)
        return ' '.join(out)


    def test(self):
        val = '\n'.join(list(vim.current.buffer))
        new = self.fix_text(val)
        vim.current.buffer[:] = new.split('\n')
