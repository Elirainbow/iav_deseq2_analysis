# Contexto del proyecto

## Problema

Se desea analizar un archivo de resultados de DESeq2 para identificar genes diferencialmente expresados durante una infección por Influenza A Virus.

## Objetivo del programa

Construir una primera versión de un programa en Python que lea un archivo TSV, filtre genes significativos y clasifique genes sobreexpresados y subexpresados.

## Archivos de entrada

- data/iav_deseq2_results.tsv

## Archivo de salida esperado

- results/iav_significant_genes.tsv

## Ejemplo de salida esperada

```text
gene    log2FoldChange  padj    status
MX1 4.2 0.0001  upregulated
IFIT1   5.1 0.00001 upregulated

## 3.4 Requisitos funcionales

El programa debe:

1. Leer el archivo `iav_deseq2_results.tsv`.
2. Ignorar encabezados correctamente.
3. Extraer para cada gen:
   - nombre del gen
   - `log2FoldChange`
   - `padj`
4. Ignorar líneas incompletas o con valores no numéricos.
5. Identificar genes significativos usando:
   - `padj < 0.05`
   - `abs(log2FoldChange) >= 1`
6. Clasificar genes significativos como:
   - sobreexpresados
   - subexpresados
7. Mostrar un resumen en pantalla.
8. Guardar los genes significativos en un archivo de salida.


## 3.5 Actualiza `docs/context.md`

Agrega:

```markdown
## Requisitos funcionales

1. Leer un archivo TSV con resultados de DESeq2.
2. Extraer el nombre del gen, log2FoldChange y padj.
3. Ignorar líneas inválidas o incompletas.
4. Identificar genes significativos usando padj < 0.05 y abs(log2FoldChange) >= 1.
5. Clasificar genes como sobreexpresados o subexpresados.
6. Mostrar un resumen en pantalla.
7. Guardar los genes filtrados en un archivo de salida.

## Criterios de significancia

Un gen se considerará diferencialmente expresado si cumple:

- padj < 0.05
- abs(log2FoldChange) >= 1

Si log2FoldChange > 0, el gen se clasificará como sobreexpresado.
Si log2FoldChange < 0, el gen se clasificará como subexpresado.