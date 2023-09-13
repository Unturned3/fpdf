
import fitz
import pats
import argparse
from unidecode import unidecode

#import warnings
#warnings.filterwarnings('ignore', module='unidecode')


def fmt(s: str, **kwargs):
    for k in kwargs.keys():
        s = s.replace('{' + k + '}', kwargs[k])
    return s


# Return the PDF text content as a single string, and
# a mapping from character position to page number, 
# bounding box, and its containing fitz span.

def parse_pdf(pdf: fitz.Document) -> (str, dict):

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
                        c = unidecode(char['c'], errors='replace', replace_str='?')
                        if not str.isascii(c):
                            c = '?'
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


class HelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action: argparse.Action) -> str:
        f = super()._format_action_invocation(action)
        if action.option_strings and action.nargs != 0:
            metavar = self._format_args(action, self._get_default_metavar_for_optional(action))
            f = f.replace(' ' + metavar, '',)
        return f


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=HelpFormatter)
    parser.add_argument('-p', '--print-parsed', action='store_true',
                        help='print parsed pdf text to file')
    parser.add_argument('-l', '--highlight', action='store_true',
                        help='')
    parser.add_argument('-s', '--ref-style', metavar='style',
                        choices=list(pats.patterns.keys()), default='ieee',
                        help='')
    parser.add_argument('-o', '--output', metavar='name', default=None,
                        help='output file path')
    parser.add_argument('file')
    args = parser.parse_args()
    return args
