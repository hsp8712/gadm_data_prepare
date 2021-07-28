from unittest import TestCase
from location_parser import hierarchy


class Test(TestCase):
    def test_hierarchy(self):
        self.assertEqual(["CHN", "CHN.1_1", "CHN.1_1.1"], hierarchy("CHN.1_1.1", "."))
