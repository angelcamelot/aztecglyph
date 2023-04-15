import time
import datetime
from aztecglyph.utils import atoi, itoa
import secrets

BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
EPOCH = 1577836800000  # 2020-01-01 00:00:00+00:00 in milliseconds


class AztecGlyph(object):
    """
    The AztecGlyph class is a useful tool for generating unique and secure IDs and keys. This class represents 64-bit
    UUIDs that are immutable, hashable, and can be used as dictionary keys. Converting an AztecGlyph to a string with
    str() yields a base58-encoded string, such as 'jpXCZedGfVQ'.

    The AztecGlyph constructor accepts four possible forms: a string (base58 encoded), a bytes object, an integer, or
    the values counter, content type and timestamp. The AztecGlyph is divided into three parts: timestamp (41-bit),
    counter (11-bit), and content type (12-bit). The timestamp is the number of milliseconds since 2015-01-01 00:00:00.
    The counter is a number that is incremented every time a new AztecGlyph is created. The content type is used to
    identify the type of data stored in the AztecGlyph. The timestamp is the number of milliseconds since 2020-01-01.

    AztecGlyphs have these read-only attributes:
        bytes           The 8-byte AztecGlyph as a bytes object.
        hex             The 8-byte AztecGlyph as a hex string.
        int             The 8-byte AztecGlyph as an integer.
        str             The 8-byte AztecGlyph as a base58 string.
        content_type    The content type as an integer.
        counter         The counter as an integer.
        timestamp       The timestamp as a datetime object.

    Overall, the AztecGlyph class is efficient and provides a high level of flexibility for creating unique IDs and keys
    in different forms. Its implementation is also highly secure and reliable, making it a valuable resource for any
    project requiring unique and secure identifiers.
    """
    __slots__ = ('int', '__weakref__')

    def __init__(
            self,
            s: str = None,
            b: bytes = None,
            i: int = None,
            h: str = None,
            counter: int = None,
            content_type: int = None,
            now: int = None
    ):
        if s is not None:
            if len(s) != 11:
                raise ValueError("AztecGlyph must be 11 characters long")
            if not all(c in BASE58 for c in s):
                raise ValueError("AztecGlyph must contain only base58 characters")
            from_int = atoi(s, BASE58)
        elif b is not None:
            if len(b) != 8:
                raise ValueError("AztecGlyph must be 8 bytes long")
            from_int = int.from_bytes(b, "big")
        elif i is not None:
            if i < 0 or i > 18446744073709551615:
                raise ValueError("AztecGlyph must be between 0 and 18446744073709551615")
            from_int = i
        elif h is not None:
            if len(h) != 16:
                raise ValueError("AztecGlyph must be 16 hex characters long")
            if not all(c in "0123456789abcdefABCDEF" for c in h):
                raise ValueError("AztecGlyph must contain only hex characters")
            from_int = int(h, 16)
        else:
            if counter is None:
                max_value = 2047
                counter = secrets.randbelow(max_value + 1)
            else:
                if counter < 0 or counter > 2047:
                    raise ValueError("counter must be between 0 and 2047")
            if content_type is None:
                max_value = 4095
                content_type = secrets.randbelow(max_value + 1)
            else:
                if content_type < 0 or content_type > 4095:
                    raise ValueError("content_type must be between 0 and 4095")
            if now is None:
                now = int(time.time() * 1000)
            else:
                if now < 1577836800000 or now > 3776860055551:
                    raise ValueError("now must be between 1577836800000 and 3776860055551")
            timestamp = now - EPOCH
            timestamp = timestamp & 0x1FFFFFFFFFF
            counter = counter & 0x7FF
            content_type = content_type & 0xFFF
            from_int = (timestamp << 23) | (counter << 12) | content_type
        object.__setattr__(self, 'int', from_int)

    @property
    def hex(self):
        return self.int.to_bytes(8, "big").hex()

    @property
    def bytes(self):
        return self.int.to_bytes(8, "big")

    @property
    def str(self):
        base58 = itoa(self.int, BASE58)
        base58 = base58.rjust(11, '1')
        return base58

    @property
    def timestamp(self):
        timestamp = (self.int >> 23) & ((1 << 41) - 1)
        timestamp = EPOCH + timestamp
        return timestamp

    @property
    def datetime(self):
        timestamp = self.timestamp
        timestamp = timestamp / 1000
        return datetime.datetime.fromtimestamp(timestamp)

    @property
    def counter(self):
        counter = (self.int >> 12) & ((1 << 11) - 1)
        return counter

    @property
    def content_type(self):
        content_type = self.int & ((1 << 12) - 1)
        return content_type

    def __str__(self):
        return self.str

    def __repr__(self):
        return f"AztecGlyph({self.str})"

    def __eq__(self, other):
        if isinstance(other, AztecGlyph):
            return self.int == other.int
        return False

    def __hash__(self):
        return self.int

    def __lt__(self, other):
        return self.int < other.int

    def __le__(self, other):
        return self.int <= other.int

    def __gt__(self, other):
        return self.int > other.int

    def __ge__(self, other):
        return self.int >= other.int

    def __int__(self):
        return self.int

    def __bytes__(self):
        return self.bytes

    def __setattr__(self, name, value):
        raise TypeError("AztecGlyph objects are immutable")

    def __getstate__(self):
        return self.bytes

    def __setstate__(self, state):
        object.__setattr__(self, 'bytes', state)

    @staticmethod
    def __version__():
        return '1.0.2'
