import argparse
import ast
import json
import os
from collections import Counter, defaultdict
from typing import Dict


def write_json(file_name: str, data: Dict) -> None:
    """Escribe un diccionario en un archivo JSON."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def parse_ast(filename: str):
    """Parsea el contenido de un archivo Python y devuelve el árbol AST."""
    with open(filename, "r", encoding="utf-8") as file:
        return ast.parse(file.read(), filename=filename)


def extract_imports(ast_tree):
    """Extrae todos los nombres de módulos importados en el árbol AST."""
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def map_dependencies(directory: str):
    """Mapea las dependencias de importación de cada archivo en un directorio."""
    import_map = defaultdict(set)
    reverse_import_map = defaultdict(set)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                tree = parse_ast(full_path)
                current_package = full_path.replace(directory, "").split(os.sep)[1]
                imported_modules = set(extract_imports(tree))

                for module in imported_modules:
                    import_map[current_package].add(module.split(".")[0])
                    reverse_import_map[module.split(".")[0]].add(current_package)

    return import_map, reverse_import_map


def calculate_coupling(directory: str):
    """Calcula el acoplamiento eferente y aferente para cada paquete en un directorio."""
    import_map, reverse_import_map = map_dependencies(directory)
    efferent_coupling = {package: len(dependencies) for package, dependencies in import_map.items()}
    afferent_coupling = {package: len(dependers) for package, dependers in reverse_import_map.items()}

    return efferent_coupling, afferent_coupling


def main() -> None:

    # Get source folder path to analyze as argument using pyarg

    parser = argparse.ArgumentParser(description="Analyze Python package imports.")
    parser.add_argument("source_folder", type=str, help="Path to the source folder to analyze")
    args = parser.parse_args()

    project_directory = args.source_folder

    ce, ca = calculate_coupling(project_directory)
    print({"Acoplamiento Eferente (CE):": ce, "Acoplamiento Aferente (CA):": ca})

    write_json(data={"CE": ce, "CA": ca}, file_name="results_measure_ca_and_ce2.json")


if __name__ == "__main__":
    main()
