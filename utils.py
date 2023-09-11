
def fmt(s: str, **kwargs):
    for k in kwargs.keys():
        s = s.replace('{' + k + '}', kwargs[k])
    return s
