
import fitz
from unidecode import unidecode

import warnings
warnings.filterwarnings('ignore', module='unidecode')


def fmt(s: str, **kwargs):
    for k in kwargs.keys():
        s = s.replace('{' + k + '}', kwargs[k])
    return s


# Return the PDF text content as a single string, and
# a mapping from character position to page number, 
# bounding box, and its containing fitz span.

def parse(pdf: fitz.Document) -> (str, dict):

    s, d, idx = [], {}, 0

    for page in pdf.pages():

        tdict = page.get_text(
            'rawdict',
            flags =  fitz.TEXTFLAGS_RAWDICT
                  & ~fitz.TEXT_PRESERVE_IMAGES
        )

        for block in tdict['blocks']:
            for line in block['lines']:
                for span in line['spans']:
                    for char in span['chars']:
                        d[idx] = (page.number, *char['bbox'], span)
                        c = unidecode(char['c'])
                        s.append(c)
                        idx += len(c)

                prev_span = line['spans'][-1]
                prev_char = prev_span['chars'][-1]

                # Separate each line by '\n'.
                # Remove line-breaking hyphens if needed.
                if prev_char['c'] == '-':
                    space_found = False
                    for i in range(-1, -100, -1):
                        if str.isspace(s[i]):
                            s[i] = '\n'
                            space_found = True
                            break
                    assert(space_found)
                    s.pop()
                    idx -= 1
                else:
                    d[idx] = (page.number, *prev_char['bbox'], prev_span)
                    s.append('\n')
                    idx += 1

    return ''.join(s), d
