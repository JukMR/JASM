import ast
import os

# Add directory folder to path
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from measure_ca_and_ce5 import extract_imports


class TestImportExtraction(unittest.TestCase):
    def test_simple_import(self):
        code = "import numpy"
        expected = ["numpy"]
        self.assertEqual(extract_imports(code), expected)

    def test_from_import(self):
        code = "from os import path"
        expected = ["os.path"]
        self.assertEqual(extract_imports(code), expected)

    def test_multiple_imports(self):
        code = "import sys\nfrom os import path"
        expected = ["sys", "os.path"]
        self.assertEqual(extract_imports(code), expected)

    def test_conditional_imports(self):
        code = "if True:\n    import yaml"
        expected = ["yaml"]
        self.assertEqual(extract_imports(code), expected)


# Para ejecutar las pruebas
if __name__ == "__main__":
    unittest.main()
