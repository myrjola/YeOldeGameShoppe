from django.utils.functional import allow_lazy


def _format(string, *args, **kwargs):
    return string.format(*args, **kwargs)

# This solves reverse_lazy concatenation see:
# http://stackoverflow.com/questions/31236234/using-djangos-reverse-lazy-and-concatenizing-it
lazy_format = allow_lazy(_format, str)
