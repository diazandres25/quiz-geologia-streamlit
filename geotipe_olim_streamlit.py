import streamlit as st
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurar la página con un diseño llamativo
st.set_page_config(page_title="Geolimpiadas - ACGGP", page_icon="🌍", layout="wide")

# Configuración de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Geolimpiadas_Puntajes").sheet1

# Estilos mejorados
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .subtext {
            text-align: center;
            font-size: 20px;
            color: #34495e;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='title'>🌍 Geolimpiadas - ACGGP</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Pon a prueba tus conocimientos en geología con este quiz.</div>", unsafe_allow_html=True)

# Preguntas por categoría
preguntas_por_categoria = {
    "General": [
        {"pregunta": "¿Qué es la geología?", "opciones": ["Estudio de los animales", "Estudio de la Tierra", "Estudio del clima", "Estudio del agua"], "respuesta": 1},
        {"pregunta": "¿Cuál es la capa más externa de la Tierra?", "opciones": ["Núcleo", "Manto", "Corteza", "Litosfera"], "respuesta": 2},
    ],
    "Estructural": [
        {"pregunta": "¿Qué es una falla geológica?", "opciones": ["Un volcán", "Un pliegue de roca", "Un plano de fractura con desplazamiento", "Un depósito de minerales"], "respuesta": 2},
        {"pregunta": "¿Qué tipo de esfuerzo produce fallas inversas?", "opciones": ["Compresión", "Tensión", "Cizalla", "Flexión"], "respuesta": 0},
    ],
    "Sedimentología": [
        {"pregunta": "¿Qué es una roca sedimentaria?", "opciones": ["Roca formada por enfriamiento de magma", "Roca formada por acumulación de sedimentos", "Roca metamórfica", "Roca con estructura cristalina"], "respuesta": 1},
        {"pregunta": "¿Cuál es un ejemplo de roca sedimentaria?", "opciones": ["Granito", "Caliza", "Basalto", "Cuarzo"], "respuesta": 1},
    ],
}

# Registro del jugador individual
nombre = st.text_input("✍️ Ingresa tu nombre:")
if nombre and st.button("Registrarse"):
    sheet.append_row([nombre, 0])
    st.success(f"Jugador {nombre} registrado. Puedes comenzar el quiz.")

# Seleccionar categoría
categoria_seleccionada = st.selectbox("🔎 Selecciona una categoría de preguntas:", list(preguntas_por_categoria.keys()))

# Mostrar preguntas
def iniciar_quiz(nombre):
    preguntas = random.sample(preguntas_por_categoria[categoria_seleccionada], len(preguntas_por_categoria[categoria_seleccionada]))
    puntaje = 0
    for i, pregunta in enumerate(preguntas):
        st.subheader(f"❓ Pregunta {i + 1} de {len(preguntas)}")
        st.write(pregunta["pregunta"])
        respuesta_usuario = st.radio("Selecciona una opción:", pregunta["opciones"], index=None)

        if st.button("Responder", key=f"resp_{i}"):
            if respuesta_usuario is not None:
                if pregunta["opciones"].index(respuesta_usuario) == pregunta["respuesta"]:
                    st.success("✅ ¡Correcto!")
                    puntaje += 1
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta era: {pregunta['opciones'][pregunta['respuesta']]}")

    # Guardar puntaje en Google Sheets
    cell = sheet.find(nombre)
    sheet.update_cell(cell.row, 2, puntaje)
    st.subheader(f"🎉 Has terminado el quiz, {nombre}!")
    st.write(f"Tu puntaje final: {puntaje}")

if st.button("Comenzar Quiz") and nombre:
    iniciar_quiz(nombre)

# Mostrar clasificación
datos = sheet.get_all_values()
st.subheader("🏆 Clasificación Total")
st.table(datos)

