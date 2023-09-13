

# Configuration file for fpdf

# Do not change the names of existing variables; some of them
# are used by fpdf internally. Add new variables as needed.

# Python regex syntax documentation:
# https://docs.python.org/3/library/re.html#regular-expression-syntax


# The `fmt` function allows you to reuse regex subpatterns.
# It will replace any occurence of {x} in the input string
# with the value of the kwarg whose key is x. Essentially,
# this is a more restrictive version of Python's built-in
# str.format() method. Usage examples are given below.
from utils import fmt


# This searches for the point in the PDF where fpdf will
# start looking for reference destinations (i.e. where in-text
# citations will link to)
start_of_ref_list = r'^(?:References|REFERENCES|Bibliography|BIBLIOGRAPHY) ?$'


# Define regex subpatterns here. The convention is to make
# any groups in subpatterns non-capturing and explicitly wrap
# groups in brackets in the top-level pattern if needed. This
# is to avoid confusion on how many capturing groups are in
# a top-level pattern.
valid_year = r'(?:19[5-9]\d|20[0-4]\d|2050)[a-z]?'
#lastname = r'(?:[a-zA-Z]{2,}(?:-[a-zA-Z]{2,})*)'
lastname = r'(?:[\w]{2,}(?:-[\w]{2,})*)'


# A note on capture groups

# They are used directly by fpdf as the keys for linking references.
# For instance, the IEEE style regex captures the positive integer
# inside the square brackets (e.g. [1], [2,3,4], etc.) and uses it
# as the citation key, so an in-text citation like [6] will link to
# the entry marked as [6] in the reference list.

# The APA style is a little more involved. In-text citations are of
# the form (Author, Year), where Author can be:

#   1. One last name, e.g. Smith
#   2. Two last names, e.g. Smith and Jones
#   3. One last name followed by `et al.`, e.g. Smith et al.

# The Year can also have a letter suffix, e.g. 2019a, 2015b, etc. to
# denote different works published by the same author in the same year.

# As a result, we have to define three capturing groups: two for the
# author names (the 2nd may be None), and one for the year.

# The APA style also have two in-text citation styles:
#   1. (Author1, Year1; Author2, Year2; ...)
#   2. Author1 (Year1)
# which we refer to as 'refs' and 'alt-ref' respectively
# in the dictionary below.


# IEEE style. Commonly used in computer science.
ieee_ref = '([1-9][0-9]*)'
ieee = {
    'ref': ieee_ref,
    'refs': fmt(r'\[{r}((,|-)\s*{r})*\]', r=ieee_ref),
    'dst': fmt(r'^\[{r}\] ', r=ieee_ref),
}


# APA style.
# Known limitations:
#
#   1. In-text citations split across pages with interjecting
#      text are not recognized. Example: bottom of page 35
#      of apa-std-1.pdf
#
#   2. Last names containing spaces are not recognized.
#      Example: 'van den Oord et al., 2017' (page 37 of
#      apa-std-1.pdf)
#
apa_ref = fmt(r'({l})(?:|\set\sal\.|\sand\s({l}))'
              r',\s({y})(?:,\s{y})*', l=lastname, y=valid_year)
apa = {
    'ref': apa_ref,
    'alt-ref': fmt(r'({l})(?:|\set\sal\.|\sand\s({l}))'
                   r'\s\(({y})\)', l=lastname, y=valid_year),
    'refs': fmt(r'\((e\.g\.,\s)?{r}(;\s*{r})*\)', r=apa_ref),
    'dst': fmt(r'^({l}),(?:(?:\s|-)[A-Z]\.)+'
               r'(?:|,\s.*?\.|\sand\s({l}),(?:(?:\s|-)[A-Z]\.)+)'
               r'\s\(({y})\)\.\s', l=lastname, y=valid_year),
}


# Define your own styles here...


# Add your styles to this dict, so fpdf can use them.
patterns = {
    'ieee': ieee,
    'apa': apa,
}

