
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
    
    def test(self):
        val = '\n'.join(list(vim.current.buffer))
        new = self.run_replacements(val)
        vim.current.buffer[:] = new.split('\n')

