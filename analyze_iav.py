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


# Responsabilidad: Clasificar un gen como "upregulated", "downregulated" o "not_significant" según su log2_fold_change y padj.
# Entrada: log2_fold_change
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
