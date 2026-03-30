import reflex as rx
import httpx
from app import style

# ==========================================
# 1. State (Back)
# ==========================================

class Estado(rx.State):
    mensaje_api: str = ""
    texto_factura : str = ""
    chat_history : list[tuple[str, str]] = []
    
    @rx.event
    def obtener_datos(self):
        respuesta = httpx.get("http://api:8000/")
        datos = respuesta.json()
        self.mensaje_api = datos["mensaje"]
    
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
            on_click=Estado.limpiar_chat
        )
    )
    
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Analizador de Facturas"),
            rx.text("Bienvenido al aplicativo 'Analizador de facturas'."),
            rx.text("Aquí podrás verificar el comportamiento de tus gastos."),
            chat(),
            action_bar(),
            align="center",
        )
    )

# ==========================================
# 3. APP
# ==========================================  
app = rx.App()
app.add_page(index)