import unittest
from aztecglyph import AztecGlyph


class TestAztecGlyph(unittest.TestCase):

    def test_base58_string(self):
        base58_str = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        glyph = AztecGlyph(s="jpXCZedGfVQ")
        self.assertTrue(all(c in base58_str for c in str(glyph)))

    def test_invalid_base58_string(self):
        with self.assertRaises(ValueError):
            AztecGlyph(s="INVALID0")

    def test_byte_length(self):
        glyph = AztecGlyph(b=b'\x00\x01\x02\x03\x04\x05\x06\x07')
        self.assertEqual(len(glyph.bytes), 8)

    def test_invalid_byte_length(self):
        with self.assertRaises(ValueError):
            AztecGlyph(b=b'\x00\x01\x02\x03\x04\x05\x06')

    def test_int_range(self):
        glyph = AztecGlyph(i=0xFFFFFFFFFFFFFFFF)
        self.assertLessEqual(glyph.int, 0xFFFFFFFFFFFFFFFF)

    def test_invalid_int_range(self):
        with self.assertRaises(ValueError):
            AztecGlyph(i=-1)
        with self.assertRaises(ValueError):
            AztecGlyph(i=0x10000000000000000)

    def test_hex_string(self):
        glyph = AztecGlyph(h="1234567890ABCDEF")
        self.assertTrue(all(c in "0123456789ABCDEFabcdef" for c in glyph.hex))

    def test_invalid_hex_string(self):
        with self.assertRaises(ValueError):
            AztecGlyph(h="INVALIDX")

    def test_from_int(self):
        glyph = AztecGlyph(i=0x1234567890ABCDEF)
        self.assertEqual(glyph.int, 0x1234567890ABCDEF)

    def test_immutable(self):
        glyph = AztecGlyph(i=0x1234567890ABCDEF)
        with self.assertRaises(TypeError):
            glyph.int = 0xFFFFFFFFFFFFFFFF

    def test_equality(self):
        glyph1 = AztecGlyph(i=0x1234567890ABCDEF)
        glyph2 = AztecGlyph(i=0x1234567890ABCDEF)
        self.assertEqual(glyph1, glyph2)



if __name__ == '__main__':
    unittest.main()
