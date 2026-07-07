import reflex as rx
# IMPORTAMOS TU CÓDIGO ORIGINAL: Reflex va a usar tus funciones seguras desde acá
import Codigo_del_Sistema as backend

# --- ESTADO DE LA APLICACIÓN (REFLEX STATE) ---
class State(rx.State):
    nombre_alumno: str = ""
    curso_seleccionado: str = "Programacion"
    mensaje_alerta: str = ""
    tipo_alerta: str = "info"

    @rx.var
    def estadisticas_cursos(self) -> list[dict]:
        backend.inicializar_cursos()  # Llama a tu función original
        conteo_total = backend.obtener_todas_las_inscripciones()  # Llama a tu Counter original
        lineas_cursos = backend.leer_archivo_seguro(backend.ARCHIVO_CURSOS)
        
        cursos_data = []
        for curso, cupo_max in zip(lineas_cursos[0::2], lineas_cursos[1::2]):
            cupo_max = int(cupo_max)
            inscriptos = conteo_total[curso.casefold()]
            cursos_data.append({
                "nombre": curso,
                "inscriptos": inscriptos,
                "cupo_maximo": cupo_max,
                "disponibles": max(0, cupo_max - inscriptos)
            })
        return cursos_data

    @rx.var
    def total_inscriptos(self) -> int:
        return sum(c["inscriptos"] for c in self.estadisticas_cursos)

    @rx.var
    def total_cupos_disponibles(self) -> int:
        return sum(c["disponibles"] for c in self.estadisticas_cursos)

    @rx.var
    def total_espera(self) -> int:
        lineas_espera = backend.leer_archivo_seguro(backend.ARCHIVO_ESPERA)
        return len(lineas_espera) // 2

    def procesar_registro(self):
        nombre = self.nombre_alumno.strip()
        curso = self.curso_seleccionado
        
        if not nombre:
            self.mensaje_alerta = "El nombre del alumno no puede estar vacío."
            self.tipo_alerta = "error"
            return

        # Usamos tu regla de negocio exacta del archivo original sin duplicarla
        if backend.alumno_ya_inscripto(nombre, curso):
            self.mensaje_alerta = f"Error: {nombre} ya se encuentra inscripto en {curso}."
            self.tipo_alerta = "error"
            return

        cupo_maximo = backend.obtener_cupo_maximo(curso)
        inscriptos_actuales = backend.obtener_todas_las_inscripciones()[curso.casefold()]
        
        if cupo_maximo - inscriptos_actuales > 0:
            backend.registrar_inscripcion(nombre, curso)  # Guarda en tu archivo txt original
            self.mensaje_alerta = f"¡Estudiante {nombre} registrado con éxito en {curso}!"
            self.tipo_alerta = "success"
        else:
            backend.registrar_espera(nombre, curso)  # Envía a tu lista de espera original
            self.mensaje_alerta = f"Curso completo. {nombre} agregado a la lista de espera."
            self.tipo_alerta = "warning"

        self.nombre_alumno = ""

# --- INTERFAZ GRÁFICA (FRONTEND) ---
def index() -> rx.Component:
    return rx.hstack(
        # Sidebar izquierda
        rx.vstack(
            rx.hstack(rx.icon("graduation-cap", size=24), rx.heading("Academia", size="5")),
            rx.divider(opacity=0.2),
            rx.button(rx.icon("layout-dashboard", size=18), "Panel", variant="ghost", justify="start", width="100%", color_scheme="amber"),
            rx.button(rx.icon("users", size=18), "Inscripciones", variant="ghost", justify="start", width="100%"),
            rx.button(rx.icon("clock", size=18), "Lista de espera", variant="ghost", justify="start", width="100%"),
            rx.spacer(),
            background_color="#1e293b", color="white", width="250px", height="100vh", padding="2em", spacing="4"
        ),
        # Panel de Contenido
        rx.vstack(
            rx.heading("Panel de Administración", size="7"),
            rx.text("Gestione inscripciones visualmente.", color_scheme="gray"),
            rx.grid(
                rx.card(rx.hstack(rx.icon("users", size=24), rx.vstack(rx.text("Inscriptos"), rx.heading(f"{State.total_inscriptos}/60")))),
                rx.card(rx.hstack(rx.icon("check-circle", size=24), rx.vstack(rx.text("Disponibles"), rx.heading(State.total_cupos_disponibles)))),
                rx.card(rx.hstack(rx.icon("alert-circle", size=24), rx.vstack(rx.text("En Espera"), rx.heading(State.total_espera)))),
                columns="3", spacing="4", width="100%"
            ),
            rx.hstack(
                # Formulario
                rx.card(
                    rx.vstack(
                        rx.heading("Nueva Inscripción", size="4"),
                        rx.input(placeholder="Nombre", value=State.nombre_alumno, on_change=State.set_nombre_alumno),
                        rx.select(["Programacion", "Diseno Grafico", "Marketing Digital", "Contabilidad", "Ingles", "Redes y Soporte Técnico"], value=State.curso_seleccionado, on_change=State.set_curso_seleccionado, width="100%"),
                        rx.button("Registrar Estudiante", on_click=State.procesar_registro, background_color="#d97706", color="white", width="100%"),
                        rx.cond(State.mensaje_alerta != "", rx.callout(State.mensaje_alerta, color_scheme=State.tipo_alerta)),
                        spacing="3"
                    ), width="350px"
                ),
                # Tarjetas de Cursos
                rx.vstack(
                    rx.heading("Estado de Cursos", size="4"),
                    rx.grid(
                        rx.foreach(State.estadisticas_cursos, lambda curso: rx.card(
                            rx.vstack(
                                rx.hstack(rx.text(curso["nombre"], weight="bold"), rx.badge(rx.cond(curso["disponibles"] > 0, "Disponible", "Completo"), color_scheme=rx.cond(curso["disponibles"] > 0, "green", "red")), justify="space-between", width="100%"),
                                rx.text(f"Inscriptos: {curso['inscriptos']}/{curso['cupo_maximo']}", size="2"),
                                rx.progress(value=(curso["inscriptos"] / curso["cupo_maximo"]) * 100, width="100%"),
                                spacing="2"
                            )
                        )), columns="2", spacing="3", width="100%"
                    ), flex="1"
                ), width="100%", spacing="5", align_items="start"
            ), padding="2em", flex="1", background_color="#f8fafc", height="100vh", overflow_y="auto", spacing="5"
        ), width="100%", spacing="0"
    )

app = rx.App()
app.add_page(index)
