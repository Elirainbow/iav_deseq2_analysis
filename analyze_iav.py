import argparse


def parse_arguments():
    """
    Guardar los argumentos de la línea de comandos en un objeto argparse.

    Returns:
        argparse.Namespace: Objeto argparse con los argumentos de entrada y salida.
    """
    parser = argparse.ArgumentParser(
        description="Analiza los resultados de DESeq2 para identificar genes con expresión diferencial."
    )
    parser.add_argument(
        "input",
        type=str,
        help="Archivo TSV de entrada con los resultados de DESeq2 (obligatorio)",
    )
    parser.add_argument(
        "output",
        type=str,
        help="Archivo TSV de salida para el resumen de genes (obligatorio)",
    )
    parser.add_argument(
        "--padj",
        type=float,
        default=0.05,
        help="Umbral de padj para considerar un gen como diferencialmente expresado (default: 0.05)",
    )
    parser.add_argument(
        "--FC",
        type=float,
        default=1.0,
        help="Umbral de log2FoldChange para considerar un gen como diferencialmente expresado (default: 1.0)",
    )
    return parser.parse_args()


def validate_arguments(args):
    """
    Validar los argumentos de la línea de comandos.

    Args:
        args (argparse.Namespace): Objeto argparse con los argumentos de entrada, salida y umbrales.

    Returns:
        None
    """
    errors = []

    if args.padj < 0 or args.padj > 1:
        errors.append("Error: El umbral de padj debe estar entre 0 y 1.")
    if args.FC < 0:
        errors.append("Error: El umbral de log2FoldChange debe ser un valor positivo.")

    if errors:
        print("\nErrores de validación:")
        for error in errors:
            print(f"  - {error}")
        exit(1)


def is_significant(log2FoldChange, padj, log2fc_threshold, padj_threshold):
    """
    Evaluar si un gen cumple con los criterios de significancia para el filtrado.

    Args:
        log2FoldChange (float): Valor del cambio de expresión en escala logarítmica.
        padj (float): Valor de p-valor ajustado.
        log2fc_threshold (float): Umbral mínimo de log2FoldChange.
        padj_threshold (float): Umbral máximo de p-valor ajustado.

    Returns:
        bool: True si el gen es significativo, False en caso contrario.
    """
    if abs(log2FoldChange) >= log2fc_threshold and padj < padj_threshold:
        return True
    return False


def classify_gene(log2FoldChange):
    """
    Clasificar un gen según su log2FoldChange.

    Args:
        log2FoldChange (float): Valor del cambio de expresión en escala logarítmica.

    Returns:
        str: "upregulated" si log2FoldChange > 0, "downregulated" si < 0, o "not_significant" si = 0.
    """
    if log2FoldChange > 0:
        return "upregulated"
    elif log2FoldChange < 0:
        return "downregulated"
    else:
        return "not_significant"


def load_deseq2_results(filename):
    """
    Cargar resultados de DESeq2 desde un archivo TSV.

    Args:
        filename (str): Ruta al archivo TSV con los resultados de DESeq2.

    Returns:
        list: Lista de tuplas (gene_id, log2FoldChange, padj) con los genes válidos.
    """
    genes = []
    try:
        with open(filename, "r") as file:
            header = file.readline().strip().split("\t")
            for line in file:
                line = line.strip()
                if not line:
                    continue
                columns = line.split("\t")
                if len(columns) < 6:
                    continue
                gene_id = columns[0]
                try:
                    log2FoldChange = float(columns[2])
                    padj = float(columns[5])
                    genes.append((gene_id, log2FoldChange, padj))
                except ValueError:
                    continue
    except FileNotFoundError:
        print(f"\nError: El archivo '{filename}' no existe.")
        print("Por favor, introduce una ruta válida para el archivo de entrada.")
        exit(1)
    return genes


def filter_genes(genes, log2fc_threshold, padj_threshold):
    """
    Filtrar genes significativos y clasificarlos.

    Args:
        genes (list): Lista de tuplas (gene_id, log2FoldChange, padj).
        log2fc_threshold (float): Umbral mínimo de log2FoldChange.
        padj_threshold (float): Umbral máximo de p-valor ajustado.

    Returns:
        list: Lista de tuplas (gene_id, log2FoldChange, padj, classification) con los genes filtrados.
    """
    filtered_genes = []
    for gene_id, log2FoldChange, padj in genes:
        if is_significant(log2FoldChange, padj, log2fc_threshold, padj_threshold):
            classification = classify_gene(log2FoldChange)
            filtered_genes.append((gene_id, log2FoldChange, padj, classification))
    return filtered_genes


def write_results(filtered_genes, output_file_path):
    """
    Escribir los resultados filtrados en un archivo TSV.

    Args:
        filtered_genes (list): Lista de tuplas (gene_id, log2FoldChange, padj, classification).
        output_file_path (str): Ruta del archivo TSV de salida.

    Returns:
        None
    """
    with open(output_file_path, "w") as file:
        file.write("gene_id\tlog2FoldChange\tpadj\tclassification\n")
        for gene_id, log2FoldChange, padj, classification in filtered_genes:
            file.write(f"{gene_id}\t{log2FoldChange}\t{padj}\t{classification}\n")
    print(f"\nResultados escritos en '{output_file_path}' con éxito.")


def print_summary(filtered_genes):
    """
    Imprimir un resumen de los resultados del análisis.

    Args:
        filtered_genes (list): Lista de tuplas (gene_id, log2FoldChange, padj, classification).

    Returns:
        None
    """
    total_genes = len(filtered_genes)
    upregulated = sum(1 for gene in filtered_genes if gene[3] == "upregulated")
    downregulated = sum(1 for gene in filtered_genes if gene[3] == "downregulated")
    not_significant = sum(1 for gene in filtered_genes if gene[3] == "not_significant")

    print("\nResumen de resultados:")
    print(f"Total de genes analizados: {total_genes}")
    print(f"Genes upregulated: {upregulated}")
    print(f"Genes downregulated: {downregulated}")
    print(f"Genes no significativos: {not_significant}")


def main():
    """
    Función principal que coordina el análisis de genes con expresión diferencial.

    Lee argumentos de la línea de comandos, carga resultados de DESeq2, filtra genes significativos,
    escribe resultados en un archivo de salida e imprime un resumen.

    Returns:
        None
    """

    args = parse_arguments()
    validate_arguments(args)
    genes = load_deseq2_results(args.input)
    filtered_genes = filter_genes(genes, args.FC, args.padj)
    write_results(filtered_genes, args.output)
    print_summary(filtered_genes)


if __name__ == "__main__":
    main()
