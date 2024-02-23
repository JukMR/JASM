# Log de diagnostico capture group bug JASM

Y tengo una mala noticia, tengo un bug en la feature de capture group.

No afecta al uso o producto pero es para tenerlo en el radar (Capaz es algo interesante para trabajarlo en la tesis pero tengo la sensación que al final va a ser una boludes):

Tengo un bug de estado en los tests que involucran capture groups
Básicamente se está compartiendo la cantidad de grupos que se matchean entre reglas

# Como sé esto?

* Si se ejecutan todos los test en un single core secuencialmente, se rompen siempre en los mismos casos, con los mismos errores (errores replicables)

* Si se ejecutan por separado anda todo bien

* Si se ejecutan en paralelo, veo que andan si los que tienen conflictos se ejecutan en hilos separados

## Que esta pasando?

* Ejemplo: Al debuggear los test, veo que en una regex se esta queriendo llamar al capture group 2, pero nunca hubo un grupo 2 en la regla

## Cosas que probeé

* Cambiar la librería regex por la estándar re para ver si funcionaba ==> No éxito

* Borrar los atributos y las instancias de las clases al terminar de usarlas por las dudas ==> No éxito

* Aplicarle un fixture de scope a cada función de test ==> No éxito

# Hipotesis

* La regex se esta cacheando de alguna forma

* Las clases se están cacheando de alguna forma

* Los tests no están realmente corriendo en paralelo (de todas formas no entiendo porque se comparte el estado entre tests)

* Hay una atributo de una clase que uso para guardar que grupos fui encontrando, supongo que el problema esta cerca de esto

# Gravedad

* **Media/Baja**

  * Porque JASM solo hace un finding a la vez, así que en la ejecución normal de JASM no debería haber problema
Igual habría que ver como se va a usar en Abraham
