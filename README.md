# segmentacion

1. Se debe trabajar con un **archivo CSV** que contenga los resultados de la evaluación considerando los puntajes, de acuerdo a escala de valoración

2. La **cantidad de ítems**, dependerá de el detalle de la rúbrica asociada a la evaluación y debe ser definido.

3. La escala es la estándar que se maneja:

  + ED - Logro del aspecto en un 100%
  + AD - Logro del aspecto entre un 80% y un 99%
  + DA - Logro del aspecto entre un 60% y un 79%
  + DP - Logro del aspecto entre un 30% y un 59%
  + DC - Logro del aspecto inferior al 30%
  
  Cada uno de estos valores se escala de 1 a 5 

4. El archivo CSV de contar con las columnas OBLIGATORIAS:

  + ID del estudiante 
  + Puntaje asociado a cada ítem evaluado 

5. Considerando el archivo CSV se calculan 2 columnas: ***nota y categoría***.

6. Cálculo de la nota (en base al puntaje)

7. Cálculo de la **categoría** se usa la función:

8. Los candidatos a tutoría serán aquellos que estén en la **categoría 4 o 5**

## Configuración

+ El archivo model.config contiene los parámetros de cofiguracion
