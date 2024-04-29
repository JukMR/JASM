import argparse
import ast
import json
import os
from typing import Dict, List, Set, Tuple


def write_json(file_name: str, data: Dict) -> None:
    """Escribe un diccionario en un archivo JSON."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def extract_imports(path: str) -> List[str]:
    """Extrae todos los nombres de módulos importados en un archivo Python."""
    with open(path, "r") as file:
        tree = ast.parse(file.read(), filename=path)

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = node.module if isinstance(node, ast.ImportFrom) else None
            for alias in node.names:
                if module:
                    imports.append(f"{module}.{alias.name}".strip("."))
                else:
                    imports.append(alias.name)
    return imports


def map_dependencies(directory: str) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Mapa de dependencias de importación y referencia cruzada entre paquetes."""
    imports_map: Dict[str, Set[str]] = {}  # Quién importa a quién
    referenced_by: Dict[str, Set[str]] = {}  # Quién es importado por quién

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                imports = extract_imports(full_path)
                for imp in imports:
                    if imp not in referenced_by:
                        referenced_by[imp] = set()
                    referenced_by[imp].add(full_path)

                if full_path not in imports_map:
                    imports_map[full_path] = set()
                imports_map[full_path].update(imports)

    return imports_map, referenced_by


def calculate_coupling(
    imports_map: Dict[str, Set[str]], referenced_by: Dict[str, Set[str]]
) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Calcula el acoplamiento eferente (CE) y aferente (CA) para cada archivo."""
    CE = {key: len(value) for key, value in imports_map.items()}
    CA = {key: len(value) for key, value in referenced_by.items()}
    return CE, CA


def main() -> None:

    # Get source folder path to analyze as argument using pyarg

    parser = argparse.ArgumentParser(description="Analyze Python package imports.")
    parser.add_argument("source_folder", type=str, help="Path to the source folder to analyze")
    args = parser.parse_args()

    project_directory = args.source_folder

    # Mapeo y cálculo
    imports, references = map_dependencies(project_directory)
    CE, CA = calculate_coupling(imports, references)

    write_json("results_measure_ca_and_ce.json", {"Acoplamiento Eferente (CE):": CE, "Acoplamiento Aferente (CA):": CA})


if __name__ == "__main__":
    main()
