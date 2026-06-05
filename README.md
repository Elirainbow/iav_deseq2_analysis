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
--FC = valor positivo 
--padj = valor entre 0 y 1

# Valores por defecto de los threshold
--FC = 1
--padj = 0.05

## Ejemplo:

python analyze_iav.py data/iav_deseq2_results.tsv results/iav_significant_genes.tsv --FC 2.0 --padj 0.01

# Salida esperada
gene    log2FoldChange  padj    status
MX1 4.2 0.0001  upregulated