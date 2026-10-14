import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

from modelos import Crear, Completar, Eliminar
from logica import (
    ejecutar_accion, estado_inicial, validar_titulo,
    filtrar_por_prioridad, contar_pendientes, completar_todas,
)

PRIORIDADES = ("alta", "media", "baja")


class TareasApp:
    def __init__(self, root: ttk.Window):
        self.root = root
        self.root.title("Gestor de Tareas Funcional")
        self.root.geometry("820x600")

        # Único lugar donde el estado se REEMPLAZA (nunca se muta)
        self.estado = estado_inicial()

        self._construir_widgets()
        self._refrescar()

    def _construir_widgets(self):
        ttk.Label(
            self.root, text="✔ Gestor de Tareas",
            font=("Segoe UI", 18, "bold"), bootstyle=PRIMARY,
        ).pack(pady=10)

        # Formulario para crear
        form = ttk.Frame(self.root)
        form.pack(pady=5)

        ttk.Label(form, text="Título:").grid(row=0, column=0, padx=5)
        self.entrada_titulo = ttk.Entry(form, width=30)
        self.entrada_titulo.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Prioridad:").grid(row=0, column=2, padx=5)
        self.combo_prioridad = ttk.Combobox(
            form, values=PRIORIDADES, state="readonly", width=8)
        self.combo_prioridad.set("media")
        self.combo_prioridad.grid(row=0, column=3, padx=5)

        ttk.Button(form, text="Agregar", bootstyle=SUCCESS,
                   command=self.on_crear).grid(row=0, column=4, padx=5)

        # Filtro
        filtro = ttk.Frame(self.root)
        filtro.pack(pady=5)
        ttk.Label(filtro, text="Ver prioridad:").grid(row=0, column=0, padx=5)
        self.combo_filtro = ttk.Combobox(
            filtro, values=("Todas",) + PRIORIDADES, state="readonly", width=8)
        self.combo_filtro.set("Todas")
        self.combo_filtro.grid(row=0, column=1, padx=5)
        self.combo_filtro.bind("<<ComboboxSelected>>", lambda e: self._refrescar())

        # Tabla de tareas
        self.tabla = ttk.Treeview(
            self.root, columns=("id", "titulo", "prioridad", "estado"),
            show="headings", height=8, bootstyle=INFO)
        for col, titulo, ancho in (("id", "ID", 50), ("titulo", "Título", 300),
                                   ("prioridad", "Prioridad", 100), ("estado", "Estado", 100)):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=ancho, anchor=CENTER)
        self.tabla.pack(padx=20, pady=5, fill=X)

        self.lbl_pendientes = ttk.Label(self.root, text="", bootstyle=WARNING)
        self.lbl_pendientes.pack()

        # Botones de acción
        botones = ttk.Frame(self.root)
        botones.pack(pady=8)
        ttk.Button(botones, text="Completar", bootstyle=SUCCESS,
                   command=self.on_completar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Eliminar", bootstyle=DANGER,
                   command=self.on_eliminar).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="Completar todas", bootstyle=WARNING,
                   command=self.on_completar_todas).grid(row=0, column=2, padx=5)
        ttk.Button(botones, text="Reiniciar", bootstyle=SECONDARY,
                   command=self.on_reiniciar).grid(row=0, column=3, padx=5)

        # Historial
        ttk.Label(self.root, text="Historial:").pack(anchor=W, padx=20)
        self.lista_historial = ttk.Treeview(
            self.root, columns=("evento",), show="headings", height=5)
        self.lista_historial.heading("evento", text="Evento")
        self.lista_historial.pack(padx=20, pady=5, fill=X)

    # ---------- LECTURA DE LA PANTALLA (impuras) ----------

    def _id_elegido(self):
        """IMPURA: lee la selección y puede mostrar un messagebox."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una tarea primero.")
            return None
        return int(self.tabla.item(seleccion[0])["values"][0])

    def _titulo_valido(self):
        """IMPURA: lee el campo y avisa. La validación la hace validar_titulo (pura)."""
        titulo = validar_titulo(self.entrada_titulo.get())
        if titulo is None:
            messagebox.showwarning("Aviso", "El título no puede estar vacío.")
        return titulo

    # ---------- CALLBACKS (solo delegan en logica.py) ----------

    def on_crear(self):
        titulo = self._titulo_valido()
        if titulo is None:
            return
        accion = Crear(titulo, self.combo_prioridad.get())
        self.estado = ejecutar_accion(self.estado, accion)
        self.entrada_titulo.delete(0, END)
        self._refrescar()

    def on_completar(self):
        tarea_id = self._id_elegido()
        if tarea_id is None:
            return
        self.estado = ejecutar_accion(self.estado, Completar(tarea_id))
        self._refrescar()

    def on_eliminar(self):
        tarea_id = self._id_elegido()
        if tarea_id is None:
            return
        self.estado = ejecutar_accion(self.estado, Eliminar(tarea_id))
        self._refrescar()

    def on_completar_todas(self):
        self.estado = completar_todas(self.estado)
        self._refrescar()

    def on_reiniciar(self):
        self.estado = estado_inicial()
        self._refrescar()

    # ---------- EFECTO SECUNDARIO: dibujar en pantalla ----------

    def _refrescar(self):
        """IMPURA: modifica widgets."""
        self.tabla.delete(*self.tabla.get_children())
        visibles = filtrar_por_prioridad(self.estado.tareas, self.combo_filtro.get())
        for t in visibles:
            estado_txt = "✔ Hecha" if t.hecha else "Pendiente"
            self.tabla.insert("", END, values=(t.id, t.titulo, t.prioridad, estado_txt))

        self.lbl_pendientes.config(
            text=f"Tareas pendientes: {contar_pendientes(visibles)}")

        self.lista_historial.delete(*self.lista_historial.get_children())
        for evento in self.estado.historial:
            self.lista_historial.insert("", END, values=(evento,))