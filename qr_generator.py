import os
import qrcode
import streamlit as st
from datetime import datetime

# Carpeta donde se guardan temporalmente los QR
OUTPUT_DIR = "qr_code"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Configuración de página ----------
st.set_page_config(
    page_title="QR Code Generator",
    page_icon=":guardsman:",
    layout="centered",
)
# ---------- Imagen superior ----------
st.image("images/support.png", use_container_width=True)

# ---------- Título principal ----------
st.title("Generador de códigos QR")

# ---------- Entrada de URL ----------
url = st.text_input("Introducí la URL para generar el código QR:")

# ---------- Colores personalizables ----------
st.subheader("Personaliza tu código QR")
col1, col2 = st.columns(2)
with col1:
    fill_color = st.color_picker("Color del código", "#1C13BF")
with col2:
    back_color = st.color_picker("Color de fondo", "#FFFFFF")

# ---------- Toggle para modo oscuro ----------
modo_oscuro = st.toggle("🌙 Activar modo oscuro")

if modo_oscuro:
    st.markdown(
        """
        <style>
        body { background-color: #0e1117; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- Función para generar QR ----------
def generate_qr_code(url, filename, fill, back):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back)
    img.save(filename)

# ---------- Botón principal ----------
if st.button("Generar código QR") and url:
    timestamp = datetime.now().strftime("%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"qr_{timestamp}.png")
    generate_qr_code(url, filename, fill_color, back_color)

    # Mostrar imagen
    st.image(filename, use_container_width=True)

    # Botón de descarga
    with open(filename, "rb") as f:
        image_data = f.read()
        st.download_button(
            label="Descargar QR",
            data=image_data,
            file_name="qr_generado.png",
            mime="image/png"
        )

    # Guardar historial en sesión
    if "historial" not in st.session_state:
        st.session_state.historial = []

    st.session_state.historial.insert(0, filename)
    st.session_state.historial = st.session_state.historial[:3]  # Máx 3 elementos

# ---------- Historial de códigos ----------
if "historial" in st.session_state and st.session_state.historial:
    st.subheader("🕘 Últimos códigos generados")
    for path in st.session_state.historial:
        st.image(path, width=150)