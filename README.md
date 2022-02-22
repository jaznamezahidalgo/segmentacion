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
  + $I_{i}$ considerando cada ítem evaluado 

5. Considerando el archivo CSV se calculan 2 columnas: ***nota y categoría***.

6. Cálculo de la nota (en base al puntaje)

> $
nota(p) =
\begin{cases}
(n_{apr}-n_{min}) \cdot \dfrac{p}{e\cdot p_{max}} + n_{min}\text{ si } p<e\cdot p_{max} \\
\\
\\
\\
(n_{max}-n_{apr}) \cdot \dfrac{p-e\cdot p_{max}}{p_{max}\cdot(1-e)} + n_{apr} \text{    si } p \ge e\cdot p_{max}
\end{cases}
$

donde:
>+ $n_{max}$ = nota máxima
>+ $n_{min}$ = nota mínima
>+ $n_{min}$ = nota mínima
>+ $e$ = Exigencia 
>+ $p_{max}$ = puntaje máximo
>+ $p_{min}$ = puntaje mínimo
>+ $n_{aprob}$ = nota aprobación

7. Cálculo de la **categoría** se usa la función:


> $
categoria(nota)= \left\{ \begin{array}{lcc}
             1 & si  & nota \geq 6.0 \\            
             \\ 2 & si & 5.0 \leq nota \leq 5.9\\
             \\ 3 & si & 4.0 \leq nota \leq 4.9\\
             \\ 4 & si & 3.0 \leq nota \leq 3.9\\
             \\ 5 & si & nota \leq 2.9
             \end{array}
   \right.
$



8. Los candidatos a tutoría serán aquellos que estén en la **categoría 4 o 5**
