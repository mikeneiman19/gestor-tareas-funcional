# Bitácora de uso de IA: Gestor de Tareas Funcional

## Interacción 1: elegir otro dominio
- Prompt: "si hubiera elegido otra cosa para crear cuál hubiera sido?" y
  luego "si sería gestor de tarea cómo quedaría, me ayudas a crearlo?".
- Fragmento sugerido: la IA propuso migrar la estructura de la Arena a un
  gestor de tareas, con una tabla de equivalencias entre conceptos (dataclass,
  Union y match/case, closure, map, filter y reduce).
- Aceptado: la idea de usar la misma estructura de tres capas.
- Modificado: nada en esta etapa.
- Rechazado: nada.
- Por qué: la estructura ya la había probado con la Arena y me permitía
  reutilizar lo que entendí de las dos unidades.

## Interacción 2: modelos.py y logica.py
- Prompt: el mismo pedido de crear el gestor de tareas.
- Fragmento sugerido: las dataclasses `Tarea`, `Crear`, `Completar`,
  `Eliminar`, la Union `Accion` y `Estado`; en la lógica, `ejecutar_accion`
  y `describir_accion` con match/case, el closure `crear_filtro_prioridad`,
  y `filtrar_por_prioridad`, `completar_todas` y `contar_pendientes` con
  filter, map y reduce, más la versión imperativa con for.
- Aceptado: todo el código. Ejecuté `python logica.py` y la salida fue la
  esperada (tareas en e0: 0, en e2: 2, pendientes 2 y 1, solo alta:
  ['Estudiar']).
- Modificado: más adelante cambié `contar_pendientes` (ver interacción 4).
- Rechazado: nada.
- Por qué: son funciones puras que devuelven un Estado nuevo en lugar de
  modificar el anterior, y la lógica queda separada de la interfaz.

## Interacción 3: interfaz.py y main.py
- Prompt: seguí pidiendo ayuda con el gestor hasta tener los 4 archivos y
  luego ejecuté `python main.py`.
- Fragmento sugerido: la clase `TareasApp` con formulario de título y
  prioridad, combo de filtro, tabla de tareas, botones (Completar, Eliminar,
  Completar todas, Reiniciar), etiqueta de pendientes e historial.
- Aceptado: la estructura completa. La ventana abrió bien y comprobé que el
  filtro "alta" muestra solo las tareas de prioridad alta, que Completar
  marca la tarea como hecha y que el historial registra cada evento.
- Modificado: nada en esta etapa.
- Rechazado: nada.
- Por qué: los botones solo llaman a funciones de logica.py. Identifiqué
  como impuras `_refrescar`, `_id_elegido` y `_titulo_valido`, porque
  modifican widgets, leen la pantalla y muestran mensajes.

## Interacción 4: contador de pendientes según el filtro
- Prompt: "cómo se hace eso de refrescar en las tareas", "cómo cambio eso
  o está bien así?", "dónde cambio eso de interfaz" y "en qué parte cambio
  esto" (sobre `contar_pendientes`).
- Fragmento sugerido: cambiar `contar_pendientes` y
  `contar_pendientes_imperativo` para que reciban una tupla de tareas, y en
  `_refrescar` llamar a `contar_pendientes(visibles)`.
- Aceptado: el cambio, porque hace que el número coincida con lo que se ve
  en la tabla.
- Error detectado: al ejecutar `python logica.py` apareció
  `AttributeError: 'tuple' object has no attribute 'tareas'`. Había
  cambiado el parámetro pero dentro del `reduce` seguía `estado.tareas`.
- Modificado: reemplacé `estado.tareas` por `tareas` dentro de
  `contar_pendientes`, guardé y volví a ejecutar. Después probé `main.py` y
  el contador funcionó.
- Rechazado: nada.
- Por qué: una función pura debe recibir solo lo que necesita. Contar
  tareas no requiere conocer todo el Estado.
- Lo que aprendí: un error de Python indica el archivo, la línea y el
  nombre exacto que falla. Al cambiar el parámetro de una función hay que
  revisar su cuerpo y también todos los lugares donde se la llama.
- Segundo error: después de arreglar logica.py, al ejecutar main.py
  apareció TypeError: reduce() arg 2 must support iteration, porque en
  interfaz.py seguía llamando contar_pendientes(self.estado). Lo corregí
  cambiándolo por contar_pendientes(visibles) y volví a ejecutar.
