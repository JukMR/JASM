# TODO TESIS

1. Reemplazar # por @ u otra cosa

2. Poder proveer un archivo de macros. Que se pre-pendean a las macros antes.

3. Arreglar/chequear valiaddrrange observer, que use el operando y no el address

4. Medir coverage

5. Soportar arboles como argumentos de macros (anycmp)

# Tesis

1. Diferencia register allocation vs register spilling. (no se si son dos distintas o sinonimos. Tengo que ver cual se refiere)

2. En la parte de optimizacion, la metodologia fue hipotesis, luego experimentos. Partimos de que el problema era el supuesto de agregar las instrucciones.

Fueron dos iteración, experimento, luego hipotesis (eso fue parser)

y la otra fue hipotessis luego experimento (appender)

3. Poner list appending y byte array en el mismo grafico

4. Agregar en la optimizacion los resultados de esta, diciendo la optimizacion elegida, el porque, ie justificacion.
Agregar que hicimos un `educated guest` en el caso de hipotesis y experimento.

5. Poner las dos iteraciones del parser y como se hizo la mejora e investigación.

6. Mover como solucion propuesto y requerimientos de la herramienta como un titulo aparte.

7. En el desarrollo:

    * contar la metodologia elegida (test driven develop)
    * contar que voy a medir coverage
    * tuve un `sme` (subject matter expert) que me ayudo a entender el problema y me guió en la solución. (buscar la traduccion al español de este termino). Este sme me brindo no solo los requerimientos sino tambien soluciones propuestas.
    * contar el metodo que segui, seguí el paradigma orientado a objetivo
    * el design approach fue responsability driven design (aca habló Rebecca_Wirfs-Brock)
    * seguimos solid principles (aca habló Robert_Cecil_Martin) y grasp patterns (aca habló Craig_Larman)
    * Y tambien mencionar los paquetes design
         * en cuanto a los paquetes poner una tablita de metricas,
                *el nombre del paquete y la metrica: `acoplamienta aferente y eferente`
                * y el porcentaje de clase abstractas (porcentaje por paquete, clases abstractas/clases totales)
                *metricas de coverage
                * metricas de complejidad ciclomatica

    metricas de qa:
        *cantidad de tests
        * coverage
    metricas de codigo:
        *cantidad de lineas
        * cantidad de clases
        *cantidad de metodos
        * cantidad de paquetes
        *cantidad de clases abstractas
        * cantidad de clases concretas
        *kloc, cantidad de lineas de comentario por lineas de codigo
        * complejidad ciclomatica

        * si encuentro agregar valores de referencia de la industria para comparar con las nuestras

        * dos diagramas, uno estatico y otro dinamico (clases y secuencia)
        * la notacion elegida fue uml 2.0
