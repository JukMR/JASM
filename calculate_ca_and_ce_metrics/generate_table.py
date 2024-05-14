def generate_latex_table(ce_counts, ca_counts):
    combined_modules = set(ce_counts.keys()).union(ca_counts.keys())

    table_rows = []
    for module in sorted(combined_modules):
        ce_count = ce_counts.get(module, "-")
        ca_count = ca_counts.get(module, "-")
        double_backslash = "\\_"
        table_rows.append(f'{module.replace("_", double_backslash)} & {ce_count} & {ca_count} \\\\ \\hline')

    table_rows = "\n    ".join(table_rows)
    table = (
        "\\begin{table}[H]\n"
        "    \\centering\n"
        "    \\small\n"
        "    \\begin{tabular}{|l|c|c|}\n"
        "    \\hline\n"
        "    \\textbf{Módulo} & \\textbf{CE} & \\textbf{CA} \\\\ \\hline\n"
        f"    {table_rows}\n"
        "    \\end{tabular}\n"
        "    \\caption{Comparativa de Conteos CE y CA}\n"
        "    \\label{{tab:ce_ca_counts}}\n"
        "\\end{table}"
    )

    return table


def main():
    data = {
        "ce_counts": {
            "regex": 18,
            "regex/tree_generators": 20,
            "regex/tree_generators/pattern_node_type_builder": 28,
            "regex/tree_generators/pattern_node_implementations": 10,
            "regex/tree_generators/pattern_node_implementations/mnemonic_and_operand": 13,
            "regex/tree_generators/pattern_node_implementations/capture_group": 8,
            "regex/macro_expander": 10,
            "match": 14,
            "match/implementations": 15,
            "match/abstracts": 5,
            "stringify_asm": 0,
            "stringify_asm/implementations": 20,
            "stringify_asm/implementations/gnu_objdump": 12,
            "stringify_asm/implementations/llvm_objdump": 3,
            "stringify_asm/abstracts": 5,
        },
        "ca_counts": {
            "regex": 2,
            "typing": 12,
            "yaml": 1,
            "jasm": 14,
            "abc": 5,
            "regex/tree_generators": 0,
            "enum": 1,
            "dataclasses": 2,
            "regex/tree_generators/pattern_node_type_builder": 0,
            "regex/tree_generators/pattern_node_implementations": 0,
            "itertools": 1,
            "regex/tree_generators/pattern_node_implementations/mnemonic_and_operand": 0,
            "regex/tree_generators/pattern_node_implementations/capture_group": 0,
            "regex/macro_expander": 0,
            "copy": 1,
            "match": 0,
            "match/implementations": 0,
            "src": 6,
            "match/abstracts": 0,
            "stringify_asm": 1,
            "stringify_asm/implementations": 0,
            "subprocess": 1,
            "pathlib": 1,
            "stringify_asm/implementations/gnu_objdump": 0,
            "re": 1,
            "stringify_asm/implementations/llvm_objdump": 0,
            "stringify_asm/abstracts": 0,
        },
    }

    ce_counts = data["ce_counts"]
    ca_counts = data["ca_counts"]
    latex_table = generate_latex_table(ce_counts, ca_counts)
    print(latex_table)


if __name__ == "__main__":
    main()
