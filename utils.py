
import fitz
from unidecode import unidecode

import warnings
warnings.filterwarnings('ignore', module='unidecode')

def fmt(s: str, **kwargs):
    for k in kwargs.keys():
        s = s.replace('{' + k + '}', kwargs[k])
    return s

def parse(pdf: fitz.Document) -> (str, dict):
    s, idx, d = [], 0, {}
    for page in pdf.pages():
        tdict = page.get_text(
            'rawdict',
            flags=fitz.TEXTFLAGS_RAWDICT & ~fitz.TEXT_PRESERVE_IMAGES
        )
        for block in tdict['blocks']:
            for line in block['lines']:
                for span in line['spans']:
                    for char in span['chars']:
                        d[idx] = (page.number, *char['bbox'], span)
                        c = char['c']
                        uc = unidecode(c)
                        s.append(uc)
                        idx += len(uc)
                prev_span = line['spans'][-1]
                prev_char = prev_span['chars'][-1]
                if prev_char['c'] == '-':
                    for i in range(-1, -50, -1):
                        if s[i] == ' ':
                            s[i] = '\n'
                            break
                    s.pop()
                    idx -= 1
                else:
                    d[idx] = (page.number, *prev_char['bbox'], prev_span)
                    s.append('\n')
                    idx += 1
    return ''.join(s), d
