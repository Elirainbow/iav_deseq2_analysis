# Casos de prueba

Estos casos permiten verificar si el programa funciona correctamente.

No son todavía pruebas automatizadas con pytest. Son escenarios para razonar, ejecutar y comparar resultados.

## Caso 1: gen sobreexpresado significativo

Entrada: 

```text
MX1 4.2 0.0001
```
Resultado esperado:

```text
El gen se reporta como significativo y sobreexpresado.
```

Criterio evaluado:
El programa identifica correctamente genes con log2FoldChange positivo, padj significativo y magnitud suficiente.

## Caso 2: gen subexpresado significativo

Entrada: 
```text
GENE1   -3.0    0.001
```

Resultado esperado:

```text
El gen se reporta como significativo y subexpresado.
```

Criterio evaluado:
El programa identifica correctamente genes con log2FoldChange negativo, padj significativo y magnitud suficiente.

## Caso 3:   gen no significativo por padj

Entrada: 
```text
GENE2   3.0 0.8
```

Resultado esperado:

```text
El gen no aparece en el archivo de salida.
```

Criterio evaluado:
El programa no debe reportar genes cuyo cambio sea pequeño, aunque tengan padj significativo.

## Caso 4: gen no significativo por magnitud de cambio

Entrada: 
```text
GENE3   0.3 0.001
```

Resultado esperado:

```text
El gen no aparece en el archivo de salida.
```

Criterio evaluado:
El programa no debe reportar genes cuyo cambio sea pequeño, aunque tengan padj significativo.

## Caso 5: (límite): Valor NA

Entrada: 
```text
GENE4   NA  0.001
```

Resultado esperado:

```text
La línea se ignora o se maneja con un mensaje claro.
El programa no debe romperse.
```

Criterio evaluado:
El programa maneja valores no numéricos en columnas que deben convertirse a float.

## Caso 6 (límite): línea incompleta

Entrada: 
```text
GENE5   0.5
```

Resultado esperado:

```text
La línea se ignora.
El programa continúa procesando las demás líneas.
```

Criterio evaluado:
El programa valida que existan suficientes columnas antes de intentar extraer datos.

## Caso 7 (límite): archivo inexistente

Entrada: 
```text
python analyze_iav.py data/no_existe.tsv results/iav_significant_genes.tsv
```

Resultado esperado:

```text
El programa muestra un mensaje claro indicando que el archivo no existe.

```

Criterio evaluado:
El programa maneja errores de lectura del archivo de entrada.

