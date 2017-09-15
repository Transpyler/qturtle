def splitindent(line):
    """Split a string into an indentation part and the rest of the string.

    Only process indentation of the first line of the string."""

    idx = 0
    while line[idx] in [' ', '\t']:
        idx += 1
    return line[:idx], line[idx:]