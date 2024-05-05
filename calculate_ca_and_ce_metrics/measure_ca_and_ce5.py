import ast
import json
import os
from pathlib import Path
from typing import Any, Dict, Final, List, Set, Tuple


def extract_imports(path: str) -> List[str]:
    """Extrae todos los nombres de módulos importados en un archivo Python."""

    if Path(path).exists():
        with open(path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=path)
    else:
        tree = ast.parse(path, filename=path)

    current_imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = node.module if isinstance(node, ast.ImportFrom) else None
            for alias in node.names:
                import_path = f"{module}.{alias.name}".strip(".") if module else alias.name
                # Filtra solo los paquetes relevantes en las importaciones
                current_imports.append(import_path)
    return current_imports


def map_dependencies(directory: str | Path, packages: List[str]) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Mapa de dependencias de importación y referencia cruzada entre paquetes específicos."""
    imports_map: Dict[str, Set[str]] = {}
    referenced_by: Dict[str, Set[str]] = {}

    for root, _, files in os.walk(directory):
        if any(pkg in root for pkg in packages):  # Filtrar por paquetes específicos
            package_name = os.path.relpath(root, directory)
            if package_name not in imports_map:
                imports_map[package_name] = set()
            if package_name not in referenced_by:
                referenced_by[package_name] = set()

            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    imports = extract_imports(full_path)
                    for imp in imports:
                        imp_package = imp.split(".")[0]  # Extrae el nombre del paquete de la importación
                        if imp_package not in referenced_by:
                            referenced_by[imp_package] = set()
                        referenced_by[imp_package].add(package_name)

                    imports_map[package_name].update(imports)

    return imports_map, referenced_by


def calculate_coupling(
    imports_map: Dict[str, Set[str]], referenced_by: Dict[str, Set[str]]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Calcula el acoplamiento eferente (CE) y aferente (CA) para cada paquete."""
    CE = {key: sorted(value) for key, value in imports_map.items()}
    CA = {key: sorted(value) for key, value in referenced_by.items()}
    return CE, CA


def get_project_folder() -> Path:
    project_folder = Path(__file__).parent.parent / "src/jasm"
    assert project_folder.name == "jasm", "This script should be run from the project's root folder"
    return project_folder


def save_results(CE: Dict[str, Any], CA: Dict[str, Any], *, filename: str) -> None:
    # Join results as a single JSON
    results = {"acoplamiento_eferente": CE, "acoplamiento_aferente": CA}

    # local function to serialize sets as lists
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, default=set_default)


def filter_out_dirs(CE: Dict[str, Any], CA: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    dirs = [".mypy_cache", "__pycache__"]
    CE_copy = CE.copy()
    CA_copy = CA.copy()

    for directory in dirs:
        for key in CE:
            if directory in key:
                del CE_copy[key]
        for key in CA:
            if directory in key:
                del CA_copy[key]
    return CE_copy, CA_copy


def clean_empty_values(input_file: str, output_file: str) -> None:
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Remove empty values
    for key, value in data.items():
        data[key] = {k: v for k, v in value.items() if v}
        for k, v in data[key].items():
            data[key][k] = [i for i in v if i]
            for i in data[key][k]:
                if not i:
                    data[key][k].remove(i)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def main() -> None:

    DEBUG_MODE: Final[bool] = False

    # Directorio del proyecto y paquetes específicos a analizar
    project_directory: Path = get_project_folder()

    specific_packages = ["src/jasm/regex", "src/jasm/stringify_asm", "src/jasm/match"]

    # Mapeo y cálculo
    imports, references = map_dependencies(project_directory, specific_packages)
    CE, CA = calculate_coupling(imports, references)

    # Remove .mypy_cache and __pycache__ from the results
    CE_filtered, CA_filtered = filter_out_dirs(CE, CA)

    # Save files to disk
    save_results(CE_filtered, CA_filtered, filename="results_filtered.json")
    clean_empty_values(input_file="results_filtered.json", output_file="results_no_empty.json")

    if DEBUG_MODE:
        # Remove the unfiltered results file
        save_results(CE, CA, filename="results.json")
    else:
        os.remove(Path("results_filtered.json"))


if __name__ == "__main__":
    main()
