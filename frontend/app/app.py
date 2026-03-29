import reflex as rx
import httpx

class Estado(rx.State):
    mensaje_api: str = "Esperando datos..."
    texto_factura : str = ""
    
    @rx.event
    def obtener_datos(self):
        respuesta = httpx.get("http://api:8000/")
        datos = respuesta.json()
        self.mensaje_api = datos["mensaje"]
    
    @rx.event    
    def enviar_datos(self):
        enviar = {"texto":self.texto_factura}
        respuesta = httpx.post("http://api:8000/factura/", json=enviar)
        self.mensaje_api = respuesta.json()["mensaje"]
        
        
    
def index() -> rx.Component:
    return rx.vstack(#Apila los elementos de arriba hacia abajo en la pantalla
        rx.heading("Analizador de Facturas"),
        rx.button("Conectar con API", on_click=Estado.obtener_datos),
        rx.text_area(
            placeholder = "Esperando datos factura...",
            value = Estado.texto_factura,
            on_change = Estado.set_texto_factura,
            ),
        rx.text(Estado.mensaje_api),
        rx.button("Enviar Factura", on_click=Estado.enviar_datos),
    )

app = rx.App()
app.add_page(index)