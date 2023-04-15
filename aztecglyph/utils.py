from functools import lru_cache


@lru_cache(2)
def _index_alphabet(alphabet):
    return {char: i for i, char in enumerate(alphabet)}


def itoa(value, alphabet, padding=None):
    if value < 0:
        raise ValueError("Only positive numbers are allowed")
    elif value == 0:
        return alphabet[0]

    result = ""
    base = len(alphabet)

    while value:
        value, rem = divmod(value, base)
        result = alphabet[rem] + result

    if padding:
        fill = max(padding - len(result), 0)
        result = (alphabet[0] * fill) + result

    return result


def atoi(value, alphabet):
    if value == alphabet[0]:
        return 0

    index = _index_alphabet(alphabet)
    result = 0
    base = len(alphabet)

    for char in value:
        result = result * base + index[char]

    return result
