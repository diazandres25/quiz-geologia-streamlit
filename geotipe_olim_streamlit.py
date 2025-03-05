import streamlit as st
import random

# Configurar la página con un diseño llamativo
st.set_page_config(page_title="Geolimpiadas - ACGGP", page_icon="🌍", layout="wide")

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
        .category-button {
            font-size: 24px !important;
            font-weight: bold;
            padding: 20px;
            width: 100%;
        }
        .container {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Mostrar logo de ACGGP con diseño mejorado
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image("/mnt/data/image.png", width=400)

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

# Estado inicial
if "nombre_jugador" not in st.session_state:
    st.session_state.nombre_jugador = ""
if "categoria_seleccionada" not in st.session_state:
    st.session_state.categoria_seleccionada = ""
if "preguntas" not in st.session_state:
    st.session_state.preguntas = []
if "indice_pregunta" not in st.session_state:
    st.session_state.indice_pregunta = 0
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "respuesta_mostrada" not in st.session_state:
    st.session_state.respuesta_mostrada = False

# Solicitar el nombre
st.session_state.nombre_jugador = st.text_input("✍️ Ingresa tu nombre para comenzar:")

if st.session_state.nombre_jugador and not st.session_state.categoria_seleccionada:
    st.write("### 🔎 Selecciona una categoría de preguntas:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🌎 General", key="general"):
        st.session_state.categoria_seleccionada = "General"
        st.session_state.preguntas = random.sample(preguntas_por_categoria["General"], len(preguntas_por_categoria["General"]))
    if col2.button("🏗️ Estructural", key="estructural"):
        st.session_state.categoria_seleccionada = "Estructural"
        st.session_state.preguntas = random.sample(preguntas_por_categoria["Estructural"], len(preguntas_por_categoria["Estructural"]))
    if col3.button("⛏️ Sedimentología", key="sedimentologia"):
        st.session_state.categoria_seleccionada = "Sedimentología"
        st.session_state.preguntas = random.sample(preguntas_por_categoria["Sedimentología"], len(preguntas_por_categoria["Sedimentología"]))

# Mostrar preguntas
if st.session_state.categoria_seleccionada:
    if st.session_state.indice_pregunta < len(st.session_state.preguntas):
        pregunta_actual = st.session_state.preguntas[st.session_state.indice_pregunta]
        st.subheader(f"❓ Pregunta {st.session_state.indice_pregunta + 1} de {len(st.session_state.preguntas)}")
        st.write(pregunta_actual["pregunta"])
        respuesta_usuario = st.radio("Selecciona una opción:", pregunta_actual["opciones"], index=None)
        
        if st.button("Responder") and not st.session_state.respuesta_mostrada:
            if respuesta_usuario is not None:
                if pregunta_actual["opciones"].index(respuesta_usuario) == pregunta_actual["respuesta"]:
                    st.success("✅ ¡Correcto!")
                    st.session_state.puntaje += 1
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}")
                st.session_state.respuesta_mostrada = True

        if st.session_state.respuesta_mostrada and st.button("Siguiente pregunta ➡️"):
            st.session_state.indice_pregunta += 1
            st.session_state.respuesta_mostrada = False
            st.rerun()
    else:
        st.subheader(f"🎉 ¡Juego terminado, {st.session_state.nombre_jugador}! Tu puntaje final es {st.session_state.puntaje}/{len(st.session_state.preguntas)}")


