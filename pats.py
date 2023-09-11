
from utils import fmt

start_of_ref_list = r'^ *(References|REFERENCES|Bibliography) *$'
valid_year = r'(?:19[5-9]\d|20[0-4]\d|2050)[a-z]?'
pos_int = r'[1-9][0-9]*'

# I'm sorry. Fuck those whose lastnames contain spaces. They're impossible to parse.
#badlastname = r'([a-zA-Z?]{2,}(?:(?:\s|-)[a-zA-Z?]{2,})*)'
lastname = r'([a-zA-Z?]{2,}(?:-[a-zA-Z?]{2,})*)'

ieee_ref = fmt(r'({i})', i=pos_int)
ieee = {
    'ref': ieee_ref,
    'alt-ref': None,
    'refs': fmt(r'\[{r}((,|-)\s*{r})*\]', r=ieee_ref),
    'dst': fmt(r'^\[{r}\] ', r=ieee_ref),
}

# One capitalized word, comma, any spaces, valid year.
# Capture groups: author name and year.
apa_ref = fmt(r'{l}(?:|\set\sal\.|\sand\s{l})'
              r',\s({y})', l=lastname, y=valid_year)
apa = {
    'ref': apa_ref,

    'alt-ref': fmt(r'{l}(?:|\set\sal\.|\sand\s{l})'
                   r'\s\(({y})\)', l=lastname, y=valid_year),

    # Any number of semicolon-separated refs,
    # enclosed in parentheses or square brackets
    'refs': fmt(r'\((e\.g\.,\s)?{r}(;\s*{r})*\)', r=apa_ref),

    # Start of the line, any spaces, one capitalized word (author name),
    # comma, any number of characters (including newline), period, any spaces,
    # open parentheses, valid year, close parentheses, period.
    # Capture groups: author name and year.
    'dst': fmt(r'^{l},(?:(?:\s|-)[A-Z]\.)+'
               r'(?:|,\s.*?\.|\sand\s{l},(?:(?:\s|-)[A-Z]\.)+)'
               r'\s\(({y})\)\.\s', l=lastname, y=valid_year),
}

patterns = {
    'ieee': ieee,
    'apa': apa,
}

