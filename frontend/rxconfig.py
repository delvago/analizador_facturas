import reflex as rx

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    backend_port=8001,
    vite_allowed_hosts= ["fedora.local", "localhost", "192.168.1.20"]
)
