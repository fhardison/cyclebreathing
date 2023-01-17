
import vim
from greek_normalisation.utils import nfc, nfd
from greek_accentuation.characters import add_breathing, Breathing,Accent, add_diacritic 
import re


class Cycle():
    FIND = [x for x in "α ε η υ ο ω i".split(' ') if x]
    DIPTH = [x for x in "ει αι οι ου αυ ευ ηυ".split(' ') if x]

    def create_replacement(ilist, ilist2, accent):
        a = [add_diacritic(x, accent) for x in ilist]
        di = [x[0] + add_diacritic(x[1], accent) for x in ilist2]
        one = [(x, add_breathing(x, Breathing.PSILI)) for x in a]
        two = [(x, 'DIPTHDIPTH' + x[0] + add_breathing(x[1], Breathing.PSILI)) for x in di]
        return one, two


    accute,di_accute = create_replacement(FIND, DIPTH, Accent.ACUTE)
    circumflex,di_circumflex = create_replacement(FIND, DIPTH, Accent.CIRCUMFLEX)

    no_accent = [(x, add_breathing(x, Breathing.PSILI)) for x in FIND]
    di_no_accent = [(x, 'DIPTHDIPTH' + x[0] + add_breathing(x[1], Breathing.PSILI)) for x in DIPTH]

    DI_REPLACEMENTS = [di_no_accent,di_circumflex,di_accute]
    REPLACEMENTS = [no_accent, accute, circumflex ]


    def run_replacements(self, text):
        text = nfc(text)
        for l in self.DI_REPLACEMENTS:
            for x, y in l:
                text = re.sub('\\b' + x, y, text)
        for l in self.REPLACEMENTS:
            for x, y in l:
                text = re.sub('\\b' + x, y, text)
        return text.replace('DIPTHDIPTH', '')
       
    ACCENTS = [chr(int(x, 16)) for x in ['0301', '0300', '0342']]
    BREATHINGS = [chr(int(x, 16)) for x in ['0313', '0314']]
    SMOOTH = BREATHINGS[0]
    DAERESIS = chr(int('0308', 16))

    # IOTA SUBSCRIPT is last but is 0345

    VOWELS = [x for x in "αεηιυοω"]
    DIPTHONGS = [x for x in "αι ει ου ευ αυ ηυ οι".split(' ')] 

    # canonical order is letter < breathing < accent < iota subscript

    def fix_text(self, text):
        out = []
        for w in nfd(text).split(' '):
            #VV
            if w[0:2] in DIPTHONGS:
                #already has breathing mark
                if w[2] in BREATHINGS:
                    out.append(w)
                #needs smooth
                elif w[2] in ACCENTS:
                    w = w[0:2] + SMOOTH +  w[2:]
                    out.append(w)
                else:
                    out.append(w[0:2] + SMOOTH + w[2:])
            #VA
            elif w[0] in VOWELS and w[1] in ACCENTS:

                if len(w) < 3:
                    out.append((w[0:1] + SMOOTH + w[1:]))
                elif w[2] not in BREATHINGS:
                    out.append((w[0:1] + SMOOTH + w[1:]))
                else:
                    out.append(w)
            #VVAB
            #VVD
            elif len(w) > 2 and w[0] in VOWELS and w[2] == DAERESIS:
                out.append((w[0] + SMOOTH + w[1:]))
            elif w[0] in VOWELS:
                if len(w) == 1:
                    out.append(w[0] + SMOOTH)
                elif w[1] not in BREATHINGS:
                    out.append((w[0] + SMOOTH + w[1:]))
                elif w[1] in ACCENTS:
                    out.append((w[0] + SMOOTH + w[1:]))
                else:
                    out.append(w)
                    print(w)
            else: 
                out.append(w)
        return ' '.join(out)
 
    def test(self):
        val = '\n'.join(list(vim.current.buffer))
        # new = self.run_replacements(val)
        new = fix_text(val)
        vim.current.buffer[:] = new.split('\n')

