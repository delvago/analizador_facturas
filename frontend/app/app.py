import reflex as rx
import httpx
from app import style
from typing import Any

# ==========================================
# 1. State (Back)
# ==========================================

class Estado(rx.State):
    mensaje_api: str = ""
    texto_factura : str = ""
    chat_history : list[tuple[str, str]] = []
    datos : list[dict] = []
    gastos_por_categoria : list[dict[str, Any]] = [
        {"categoria": "alimentacion", "valor": 0},
        {"categoria": "vivienda", "valor": 0},
        {"categoria": "servicios", "valor": 0},
        {"categoria": "transporte", "valor": 0},
        {"categoria": "salud", "valor": 0},
        {"categoria": "deudas", "valor": 0},
        {"categoria": "ahorro", "valor": 0},
        {"categoria": "ocio", "valor": 0},
    ]
    
    @rx.event
    def datos_api(self):
        respuesta = httpx.get("http://api:8000/")
        datos = respuesta.json()
        self.mensaje_api = datos["mensaje"]
        
    @rx.event
    def cargar_historial(self):
        respuesta = httpx.get("http://api:8000/gastos/")
        self.datos = respuesta.json()
        
        for item in self.gastos_por_categoria:
            item["valor"] = 0
        
        for gasto in self.datos:
            categoria_gasto = gasto.get("categoria")
            valor_gasto = gasto.get("valor", 0)
            for item in self.gastos_por_categoria:
                if item["categoria"] == categoria_gasto:
                    item["valor"] += valor_gasto
                    break
        
    
    @rx.event
    def enviar_datos(self):
        if self.texto_factura.strip() == "":
            return
        enviar = {"texto" : self.texto_factura}
        respuesta = httpx.post("http://api:8000/factura/", json=enviar)
        self.mensaje_api = respuesta.json()["mensaje"]
        self.chat_history.append((self.texto_factura, self.mensaje_api))
        self.texto_factura = ""
        
    @rx.event
    def limpiar_chat(self):
        self.chat_history = []

# ==========================================
# 2. FRONT
# ==========================================

def qa(question:str, answer:str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=style.question_style), 
            text_align="right",
            ),
        rx.box(
            rx.text(answer, style=style.answer_style), 
            text_align="left",
        ),
        margin_y="1em",
        width="100%",
    )

def chat() -> rx.Component:
    qa_pairs = [
        (
            "En este chat puedes enviar tus facturas",
            "Y se te informará si se registraron correctamente o no"
        ), 
    ]
    return rx.box(
        *[
            qa(question, answer)
            for question, answer in qa_pairs
        ],
        rx.foreach(
            Estado.chat_history,
            lambda message: qa(message[0], message[1]),
        )
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Esperando datos factura...",
            style=style.input_style,
            value=Estado.texto_factura,
            on_change=Estado.set_texto_factura,
            ),
        rx.button(
            "Enviar Factura",
            style=style.button_style,
            on_click=Estado.enviar_datos,
            ),
        rx.button(
            "Limpiar Historial del chat",
            style=style.button_style,
            on_click=Estado.limpiar_chat,
        )
    )
    
def fila_gasto(gasto: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(gasto["fecha"]),
        rx.table.cell(gasto["valor"]),
        rx.table.cell(gasto["categoria"]),
        rx.table.cell(gasto["id_usuario"]),
    )

def tabla_gastos() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("fecha"),
                rx.table.column_header_cell("valor"),
                rx.table.column_header_cell("categoria"),
                rx.table.column_header_cell("id_usuario"),
            )
        ),
        rx.table.body(
            rx.foreach(
                Estado.datos,
                fila_gasto,
            )
        ),
        width="100%",
        margin_top="2em"
    )

def actualizar_tabla() -> rx.Component:
    return rx.button(
        "Actualizar tabla",
        on_click=Estado.cargar_historial,
    )
    
def grafica_gastos() -> rx.Component:
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="valor",
            fill="3b82f6",
            radius=[4,4,0,0],
        ),
        rx.recharts.x_axis(data_key="categoria"),
        rx.recharts.y_axis(),
        rx.recharts.graphing_tooltip(),
        data=Estado.gastos_por_categoria,
        height=300,
        width="100%",
    )
    
def panel_dashboard() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Resumen por Categoría", size="4", color="gray"),
            rx.divider(),
            grafica_gastos(),
            width="100%",
            spacing="4",
        ),
        width="100%",
        max_width="800px",
        box_shadow="lg",
        border_radius="md",
        padding="5",
    )
    
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Analizador de Facturas"),
            rx.text("Bienvenido al aplicativo 'Analizador de facturas'."),
            rx.text("Aquí podrás verificar el comportamiento de tus gastos."),
            chat(),
            action_bar(),
            actualizar_tabla(),
            tabla_gastos(),
            panel_dashboard(),
            align="center",
        )
    )

# ==========================================
# 3. APP
# ==========================================  
app = rx.App()
app.add_page(index)