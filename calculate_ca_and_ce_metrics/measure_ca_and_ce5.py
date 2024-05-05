import ast
import json
import os
from collections import OrderedDict
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

    # TOFIX: Agregar manualmente las importaciones de los módulos principales en el modulo regex
    # De nuevo no se porque no esta andando bien pero prefiero agregarlo a mano
    referenced_by["regex"].add("jasm.match")
    referenced_by["stringify_asm"].add("jasm.match")
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


def write_json_to_disk(data: dict[str, Any], *, output_file: str | Path) -> None:

    # local function to serialize sets as lists
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, default=set_default)


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


def clean_empty_values(input_file: str | Path, output_file: str | Path) -> None:
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


def get_ce_finished(acoplamiento_eferente: dict[str, Any]) -> Dict[str, int]:

    # Inicialización de conjuntos para contar importaciones únicas externas
    regex_imports = set()
    match_imports = set()
    stringify_asm_imports = set()

    # Definición de dominios internos para cada módulo principal
    regex_internal = set(k for k in acoplamiento_eferente if k.startswith("regex"))

    # Remove `regex` from regex_internal because this is the actual `re` module which is externa;
    regex_internal.remove("regex")

    match_internal = set(k for k in acoplamiento_eferente if k.startswith("match"))
    stringify_asm_internal = set(k for k in acoplamiento_eferente if k.startswith("stringify_asm"))

    # Filtrar solo importaciones externas

    for ae_key, ae_values in acoplamiento_eferente.items():
        for value in ae_values:
            # Asumiendo que los nombres de módulo externo no comienzan con "jasm" que es interno
            if not value.startswith("jasm"):
                if ae_key.startswith("regex") and value not in regex_internal:
                    regex_imports.add(value)
                elif ae_key.startswith("match") and value not in match_internal:
                    match_imports.add(value)
                elif ae_key.startswith("stringify_asm") and value not in stringify_asm_internal:
                    stringify_asm_imports.add(value)

    # TOFIX: Agregar a many las llamadas a stringify y regex dentro de match
    # No se bien porque no se estan contando y no tiene mucho sentido seguir buscando
    match_imports = match_imports.union(["jasm.regex", "jasm.stringify_asm"])

    ce_consolidado = {
        "match": len(match_imports),
        "regex": len(regex_imports),
        "stringify_asm": len(stringify_asm_imports),
    }

    return ce_consolidado


def sort_ca_dict(acoplamiento_aferente: dict[str, Any]) -> Dict[str, int]:

    ca_consolidado = {key: len(set(val)) for key, val in acoplamiento_aferente.items()}

    # Order the dict alphabetically by keys
    sorted_dict = OrderedDict(sorted(ca_consolidado.items()))

    return sorted_dict


def main() -> None:

    DEBUG_MODE: Final[bool] = True
    output_folder = Path(__file__).parent / "output"
    output_folder.mkdir(exist_ok=True, parents=True)

    # Directorio del proyecto y paquetes específicos a analizar
    project_directory: Path = get_project_folder()

    specific_packages = ["src/jasm/regex", "src/jasm/stringify_asm", "src/jasm/match"]

    # Mapeo y cálculo
    imports, references = map_dependencies(project_directory, specific_packages)
    CE, CA = calculate_coupling(imports, references)

    # Remove .mypy_cache and __pycache__ from the results
    CE_filtered, CA_filtered = filter_out_dirs(CE=CE, CA=CA)

    # Join results as a single JSON
    file_joined = {"acoplamiento_eferente": CE_filtered, "acoplamiento_aferente": CA_filtered}

    # Save files to disk
    write_json_to_disk(data=file_joined, output_file=output_folder / "results_filtered.json")
    clean_empty_values(
        input_file=output_folder / "results_filtered.json", output_file=output_folder / "results_no_empty.json"
    )

    if DEBUG_MODE:
        write_json_to_disk(data=file_joined, output_file=output_folder / "results_no_empty.json")
    else:
        # Remove the unfiltered results file
        os.remove(Path("results_filtered.json"))

    # Contar CE excluyendo duplicados y contando solo las importaciones externas
    ce_counts = {key: len(set(val)) for key, val in file_joined["acoplamiento_eferente"].items()}

    # Contar CA excluyendo duplicados
    ca_counts = {key: len(set(val)) for key, val in file_joined["acoplamiento_aferente"].items()}

    counts = {"ce_counts": ce_counts, "ca_counts": ca_counts}
    write_json_to_disk(data=counts, output_file=output_folder / "counts.json")

    # Consolidar las métricas de acoplamiento eferente para los módulos principales
    ce_consolidado = get_ce_finished(acoplamiento_eferente=file_joined["acoplamiento_eferente"])

    # El acoplamiento aferente ya está a nivel de módulo global. Solo calcular los elementos y para tener las metricas finales
    ca_consolidado = sort_ca_dict(acoplamiento_aferente=file_joined["acoplamiento_aferente"])

    consolidados = {"ce_consolidado": ce_consolidado, "ca_consolidado": ca_consolidado}
    write_json_to_disk(data=consolidados, output_file=output_folder / "consolidado.json")


if __name__ == "__main__":
    main()
