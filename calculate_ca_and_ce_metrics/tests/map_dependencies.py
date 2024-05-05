import os
import shutil
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from measure_ca_and_ce5 import calculate_coupling, map_dependencies


class TestPackageCoupling(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_project"
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, "module1.py"), "w") as f:
            f.write("import module2\nfrom module3 import func")
        with open(os.path.join(self.test_dir, "module2.py"), "w") as f:
            f.write("from module3 import another_func")
        os.makedirs(os.path.join(self.test_dir, "subpackage"), exist_ok=True)
        with open(os.path.join(self.test_dir, "subpackage", "module3.py"), "w") as f:
            f.write("")

    def test_calculate_coupling(self):
        imports, references = map_dependencies(self.test_dir, ["test_project"])
        CE, CA = calculate_coupling(imports, references)
        self.assertEqual(CE, {"test_project": 2, "test_project/subpackage": 1})
        self.assertEqual(CA, {"test_project": 2, "test_project/subpackage": 1})

    def tearDown(self):
        shutil.rmtree(self.test_dir)


if __name__ == "__main__":
    unittest.main()
