from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Tarea:
    id: int
    titulo: str
    prioridad: str          # "alta", "media" o "baja"
    hecha: bool = False


@dataclass(frozen=True)
class Crear:
    titulo: str
    prioridad: str


@dataclass(frozen=True)
class Completar:
    id: int


@dataclass(frozen=True)
class Eliminar:
    id: int


Accion = Union[Crear, Completar, Eliminar]


@dataclass(frozen=True)
class Estado:
    tareas: tuple[Tarea, ...] = ()
    historial: tuple[str, ...] = ()
    siguiente_id: int = 1