import unittest
from dependency_visualizer import DependencyVisualizer
import os

class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.config_path = "test_config.ini"
        with open(self.config_path, "w") as f:
            f.write("""
[Paths]
visualizer_path = C:/Program Files/Graphviz/bin/dot.exe

[Analysis]
package_name = org.example:root
max_depth = 2

[Repository]
url = https://example.maven.repo
            """)
        self.visualizer = DependencyVisualizer(self.config_path)

    def tearDown(self):
        os.remove(self.config_path)

    def test_read_config(self):
        self.assertEqual(self.visualizer.root_package, "org.example:root")
        self.assertEqual(self.visualizer.max_depth, 2)

    def test_mock_dependencies(self):
        deps = self.visualizer.mock_dependencies("org.example:root")
        self.assertListEqual(deps, ["org.example:module1", "org.example:module2"])

    def test_analyze_dependencies(self):
        self.visualizer.analyze_dependencies("org.example:root", 0)
        self.assertTrue("org.example:module1" in self.visualizer.visited)

if __name__ == "__main__":
    unittest.main()
