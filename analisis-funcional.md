# Análisis funcional: Gestor de Tareas Funcional

## 1. Problema que resuelve
Es un gestor de tareas con interfaz gráfica. Permite crear tareas con una
prioridad (alta, media o baja), completarlas, eliminarlas, completarlas
todas a la vez y filtrarlas por prioridad. Muestra cuántas tareas pendientes
hay en la vista actual y guarda un historial de eventos.

## 2. Estructuras de datos
- `Tarea` (dataclass frozen): id, titulo, prioridad, hecha.
- `Crear`, `Completar` y `Eliminar` (dataclass frozen): las acciones del sistema.
- `Accion = Union[Crear, Completar, Eliminar]`.
- `Estado` (dataclass frozen): tupla de tareas, tupla de historial y el
  siguiente id disponible.

Se usan tuplas en lugar de listas para que el estado no se pueda modificar
con `.append()` u otras operaciones que mutan.

## 3. Dónde se aplicó la Unidad 1
- **Funciones de orden superior:** `filtrar_por_prioridad` recibe como
  argumento la función que devuelve el closure y se la pasa a `filter`.
  `map`, `filter` y `reduce` también reciben funciones como parámetro.
- **match/case:** en `ejecutar_accion` y en `describir_accion`. Cada tipo
  de acción (`Crear`, `Completar`, `Eliminar`) hace algo distinto, por eso
  `match/case` se justifica y no es un adorno.
- **Modelado de datos:** dataclass con `frozen=True` y `Union` en `modelos.py`.
- **Funcional vs. imperativo:** `contar_pendientes` (con `reduce`) frente a
  `contar_pendientes_imperativo` (con `for` y una variable `total` que
  cambia en cada vuelta).

## 4. Dónde se aplicó la Unidad 2
- **Lambda:** en `map` (`completar_todas`), en `reduce` (`contar_pendientes`),
  en `filter` (caso `Eliminar`) y en el `bind` del combo del filtro.
- **Closure:** `crear_filtro_prioridad`.
- **Inmutabilidad:** dataclass frozen, tuplas y `replace()`.
- **Pureza:** toda la lógica de `logica.py`.
- **map/filter/reduce:** `completar_todas` (map), `filtrar_por_prioridad`
  (filter) y `contar_pendientes` (reduce).

## 5. Partes puras e impuras
**Puras:** `estado_inicial`, `validar_titulo`, `describir_accion`,
`ejecutar_accion`, `crear_filtro_prioridad`, `filtrar_por_prioridad`,
`completar_todas` y `contar_pendientes`.
Son puras porque no hacen print, no leen archivos, no tocan la pantalla y
no modifican nada externo: con la misma entrada dan siempre la misma salida.

**Impuras:** `_refrescar` (modifica widgets), `_id_elegido` (lee la
selección de la tabla y puede mostrar un messagebox) y `_titulo_valido`
(lee el campo de texto y puede mostrar un aviso).

## 6. Efectos secundarios
Dibujar la tabla y el historial, actualizar la etiqueta de pendientes,
mostrar avisos con messagebox, y leer lo que el usuario escribe, selecciona
o elige en los combos. Todos están en `interfaz.py`.

## 7. Estado inmutable
Todo el `Estado`. Cuando el usuario crea, completa o elimina una tarea, el
estado no se modifica: `ejecutar_accion` devuelve un `Estado` nuevo con
`replace()` y la interfaz reemplaza `self.estado` por ese nuevo valor. El
estado anterior queda intacto, como se comprobó en la prueba de consola
(`e0` sigue con 0 tareas después de crear tareas en `e1` y `e2`).

## 8. Closure
`crear_filtro_prioridad(prioridad)` devuelve una función `filtro` que
recuerda la prioridad elegida aunque `crear_filtro_prioridad` ya terminó.
Se usa en `filtrar_por_prioridad` para quedarse solo con las tareas de la
prioridad que el usuario elige en el combo "Ver prioridad".

## 9. Qué sugirió la IA
La IA sugirió la estructura en tres capas (modelos, lógica e interfaz), las
dataclasses, el uso de match/case, el closure `crear_filtro_prioridad`, el
uso de map/filter/reduce, el código completo de la interfaz con
ttkbootstrap y la idea de pasar de la Arena a un gestor de tareas cuando
pregunté qué otro dominio podía haber elegido.

## 10. Qué corregí o rechacé
Decidí cambiar el contador de pendientes para que respete el filtro: antes
contaba todas las tareas del estado, aunque estuvieran ocultas. Para eso
cambié `contar_pendientes` y `contar_pendientes_imperativo` para que
reciban una tupla de tareas en lugar del `Estado`, y en `_refrescar` pasé
`visibles` en vez de `self.estado`.

Al hacer el cambio apareció el error `AttributeError: 'tuple' object has no
attribute 'tareas'`. La causa fue que cambié el parámetro de la función pero
dentro del `reduce` quedó `estado.tareas`. Lo corregí cambiándolo por
`tareas`, y volví a ejecutar `logica.py` y `main.py` para comprobar que
funcionaba.
Después de eso apareció un segundo error, TypeError: reduce() arg 2 must
support iteration, porque en interfaz.py todavía llamaba a
contar_pendientes(self.estado). Lo cambié por contar_pendientes(visibles).

## 11. Qué aprendí técnicamente
Aprendí que inmutabilidad significa no modificar un objeto sino crear uno
nuevo con el cambio, y que por eso el estado anterior no se pierde.
Aprendí que una función pura da siempre el mismo resultado y no hace print
ni toca la pantalla, y que por eso conviene que el contador reciba solo las
tareas que necesita y no todo el estado. Aprendí que un closure es una
función que recuerda valores de la función que la creó, como la prioridad en
`crear_filtro_prioridad`. También aprendí a leer un error de Python: el
mensaje y el número de línea me indicaron exactamente qué nombre faltaba
cambiar. Y que separar la interfaz de la lógica permite probar la lógica
sola en consola antes de abrir la ventana.

## Por qué no conviene lambda en algunos casos
Una lambda con varias condiciones es ilegible, no se puede documentar y sus
errores son poco claros.

MAL:

    prioridad_valida = lambda t, p: t.prioridad == p if p != "Todas" and not t.hecha else True

BIEN:

    def pasa_filtro(t, p):
        if p == "Todas":
            return True
        return t.prioridad == p

Para lógica con varias decisiones uso `def`. Las lambdas del proyecto son
cortas, se usan una sola vez y están dentro de `map`, `filter`, `reduce` o
de un `bind`.
