# Responsabilidad:Evaluar si los genes cumplen con los criterios de significancia para le filtrado
# Entrada:log2FoldChange, padj, lfc_threshold, padj_threshold
# Salida:True o False
def is_significant(log2FoldChange, padj, log2fc_threshold, padj_threshold):
    if abs(log2FoldChange) >= log2fc_threshold and padj < padj_threshold:
        return True
    return False


print(is_significant(4.2, 0.0001, 1, 0.05))
print(is_significant(0.3, 0.0001, 1, 0.05))
print(is_significant(3.0, 0.8, 1, 0.05))


# Responsabilidad: Clasificar un gen como "upregulated", "downregulated" o "not_significant" según su log2FoldChange y padj.
# Entrada: log2FoldChange
# Salida:"upregulated" o "downregulated", "not_significant"
def classify_gene(log2FoldChange):
    if log2FoldChange > 0:
        return "upregulated"
    elif log2FoldChange < 0:
        return "downregulated"
    else:
        return "not_significant"


print(classify_gene(4.2))
# "upregulated"

print(classify_gene(-3.0))
# "downregulated"


# Responsabilidad: abrir el archivo, leer línea por línea, ignorar líneas vacías, ignorar encabezado, separar columnas, validar columnas suficientes, convertir valores numéricos, ignorar líneas inválidas.
# Entrada: file_path (ruta al archivo CSV)
# Salida: Lista de genes válidos.
# load_deseq2_results()
def load_deseq2_results(filename):
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


# Responsabilidad: Filtrar genes significativos utilizando is_significant() y clasificar cada gen utilizando classify_gene().
# Entrada: Lista de genes (gene_id, log2FoldChange, padj)
# Salida: Lista de genes filtrados con su clasificación.
def filter_genes(genes):
    filtered_genes = []
    for gene_id, log2FoldChange, padj in genes:
        if is_significant(log2FoldChange, padj):
            classification = classify_gene(log2FoldChange)
            filtered_genes.append((gene_id, log2FoldChange, padj, classification))
    return filtered_genes


# Responsabilidad: Escribir los resultados filtrados en un nuevo archivo TSV con encabezado.
# Entrada: Lista de genes filtrados con su clasificación, output_file_path (ruta al archivo de salida)
# Salida: Archivo TSV con los resultados filtrados.
def write_results(filtered_genes, output_file_path):
    with open(output_file_path, "w") as file:
        file.write("gene_id\tlog2FoldChange\tpadj\tclassification\n")
        for gene_id, log2FoldChange, padj, classification in filtered_genes:
            file.write(f"{gene_id}\t{log2FoldChange}\t{padj}\t{classification}\n")
    print(f"\nResultados escritos en '{output_file_path}' con éxito.")
