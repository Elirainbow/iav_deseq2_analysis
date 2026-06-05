# IAV DESeq2 Analysis

Programa en Python para identificar genes diferencialmente expresados a partir de resultados de DESeq2 durante infección por Influenza A Virus.

# Estructura del proyecto
iav_deseq2_analysis/
├── data/
├── results/
├── docs/
├── analyze_iav.py
└── README.md

# Cómo ejecutar el programa
python analyze_iav.py \
    data/iav_deseq2_results.tsv \
    results/iav_significant_genes.tsv

# Uso de thresholds opcionales 
--Fold_Change = valor positivo 
--p_adjusted = valor entre 0 y 1

# Valores por defecto de los threshold
--Fold_Change = 1
--p_adjusted = 0.05

## Ejemplo:

python analyze_iav.py data/iav_deseq2_results.tsv results/iav_significant_genes.tsv --Fold_Change 2.0 --p_adjusted 0.01

# Salida esperada
gene    log2FoldChange  padj    status
MX1 4.2 0.0001  upregulated