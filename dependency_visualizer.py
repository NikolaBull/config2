import os
import configparser
from graphviz import Digraph
import subprocess
import sys

class DependencyVisualizer:
    def __init__(self, config_path):
        self.config = self.read_config(config_path)
        self.graphviz_path = self.config['Paths']['visualizer_path']
        self.root_package = self.config['Analysis']['package_name']
        self.max_depth = int(self.config['Analysis']['max_depth'])
        self.repository_url = self.config['Repository']['url']
        self.graph = Digraph(comment="Dependency Graph")
        self.visited = set()

    def read_config(self, path):
        """Чтение конфигурационного файла .ini."""
        config = configparser.ConfigParser()
        config.read(path)
        return config

    def analyze_dependencies(self, package, depth):
        """
        Рекурсивный анализ зависимостей пакета.
        В реальной задаче мы бы выполняли HTTP-запросы к репозиторию.
        Здесь это эмуляция зависимостей.
        """
        if depth > self.max_depth or package in self.visited:
            return
        self.visited.add(package)

        # Эмуляция зависимостей
        dependencies = self.mock_dependencies(package)

        for dep in dependencies:
            self.graph.edge(package, dep)
            self.analyze_dependencies(dep, depth + 1)

    def mock_dependencies(self, package):
        """Эмуляция получения зависимостей."""
        mock_data = {
            "org.example:root": ["org.example:module1", "org.example:module2"],
            "org.example:module1": ["org.example:module3"],
            "org.example:module2": ["org.example:module3", "org.example:module4"],
            "org.example:module3": [],
            "org.example:module4": ["org.example:module5"],
            "org.example:module5": [],
        }
        return mock_data.get(package, [])

    def render_graph(self, output_format="png"):
        """Создание графа и его сохранение."""
        output_path = "dependency_graph"
        self.graph.render(output_path, format=output_format, cleanup=True)
        print(f"Граф сохранен в файл: {output_path}.{output_format}")

        if os.path.exists(self.graphviz_path):
            subprocess.run([self.graphviz_path, f"{output_path}.{output_format}"])
        else:
            print("Ошибка: неверный путь к программе для визуализации.")

    def visualize(self):
        """Запуск анализа и визуализации."""
        print("Анализ зависимостей...")
        self.analyze_dependencies(self.root_package, 0)
        self.render_graph()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python dependency_visualizer.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    if not os.path.exists(config_file):
        print(f"Ошибка: файл конфигурации {config_file} не найден.")
        sys.exit(1)

    visualizer = DependencyVisualizer(config_file)
    visualizer.visualize()
