from dataclasses import replace
from functools import reduce
from modelos import Tarea, Crear, Completar, Eliminar, Accion, Estado


# ---------- FUNCIONES PURAS ----------

def estado_inicial() -> Estado:
    """PURA: siempre devuelve el mismo estado vacío."""
    return Estado()


def validar_titulo(texto: str) -> str | None:
    """PURA: devuelve el título sin espacios o None si está vacío."""
    limpio = texto.strip()
    return limpio if limpio else None


def describir_accion(accion: Accion) -> str:
    """PURA: texto para el historial, usando match/case."""
    match accion:
        case Crear(titulo=t, prioridad=p):
            return f"Tarea creada: {t} ({p})"
        case Completar(id=i):
            return f"Tarea #{i} completada"
        case Eliminar(id=i):
            return f"Tarea #{i} eliminada"
        case _:
            return "Acción desconocida"


def ejecutar_accion(estado: Estado, accion: Accion) -> Estado:
    """PURA: devuelve un Estado NUEVO, nunca modifica el original."""
    match accion:
        case Crear(titulo=t, prioridad=p):
            tareas = estado.tareas + (Tarea(estado.siguiente_id, t, p),)
            siguiente = estado.siguiente_id + 1
        case Completar(id=i):
            tareas = tuple(
                replace(t, hecha=True) if t.id == i else t
                for t in estado.tareas
            )
            siguiente = estado.siguiente_id
        case Eliminar(id=i):
            tareas = tuple(filter(lambda t: t.id != i, estado.tareas))
            siguiente = estado.siguiente_id
        case _:
            return estado

    return replace(
        estado,
        tareas=tareas,
        siguiente_id=siguiente,
        historial=estado.historial + (describir_accion(accion),),
    )


# ---------- CLOSURE ----------

def crear_filtro_prioridad(prioridad: str):
    """CLOSURE: la función interna recuerda la prioridad elegida."""
    def filtro(t: Tarea) -> bool:
        return t.prioridad == prioridad
    return filtro


# ---------- ORDEN SUPERIOR: map / filter / reduce ----------

def filtrar_por_prioridad(tareas: tuple[Tarea, ...], prioridad: str) -> tuple[Tarea, ...]:
    """PURA: filter recibe la función que crea el closure."""
    if prioridad == "Todas":
        return tareas
    return tuple(filter(crear_filtro_prioridad(prioridad), tareas))


def completar_todas(estado: Estado) -> Estado:
    """PURA: map aplica una lambda a cada tarea."""
    nuevas = tuple(map(lambda t: replace(t, hecha=True), estado.tareas))
    return replace(
        estado,
        tareas=nuevas,
        historial=estado.historial + ("Todas las tareas completadas",),
    )



def contar_pendientes(tareas: tuple[Tarea, ...]) -> int:
    """PURA: reduce acumula 1 por cada tarea no hecha."""
    return reduce(lambda acc, t: acc + (0 if t.hecha else 1), tareas, 0)


# ---------- FUNCIONAL vs IMPERATIVO ----------


def contar_pendientes_imperativo(tareas: tuple[Tarea, ...]) -> int:
    """Estilo IMPERATIVO: variable que cambia dentro de un for."""
    total = 0
    for t in tareas:
        if not t.hecha:
            total += 1
    return total

# ---------- PRUEBA EN CONSOLA ----------

if __name__ == "__main__":
    e0 = estado_inicial()
    e1 = ejecutar_accion(e0, Crear("Estudiar", "alta"))
    e2 = ejecutar_accion(e1, Crear("Lavar ropa", "baja"))
    e3 = ejecutar_accion(e2, Completar(1))

    print("Tareas en e0:", len(e0.tareas))
    print("Tareas en e2:", len(e2.tareas))
    print("Pendientes en e2:", contar_pendientes(e2.tareas))
    print("Pendientes en e3 (reduce):", contar_pendientes(e3.tareas))
    print("Pendientes en e3 (for):   ", contar_pendientes_imperativo(e3.tareas))
    print("Solo alta:", [t.titulo for t in filtrar_por_prioridad(e3.tareas, "alta")])
    print("Historial:", e3.historial)