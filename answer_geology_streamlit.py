import streamlit as st
import random
import time

# Configurar la página con un diseño más profesional
st.set_page_config(page_title="Quiz de Geología - ACGGP", page_icon="⛏️", layout="centered")

# Cargar imágenes para cada sección
imagenes_categoria = {
    "General": "general.jpg",
    "Estructural": "estructural.jpg",
    "Sedimentología": "sedimentologia.jpg"
}

# Base de datos de preguntas
preguntas_por_categoria = {
    "General": [
        {"pregunta": "¿Qué es la geología?", "opciones": ["Estudio de los animales", "Estudio de la Tierra", "Estudio del clima", "Estudio del agua"], "respuesta": 1},
        {"pregunta": "¿Cuál es la capa más externa de la Tierra?", "opciones": ["Núcleo", "Manto", "Corteza", "Litosfera"], "respuesta": 2},
        {"pregunta": "¿Qué tipo de roca es el granito?", "opciones": ["Ígnea", "Metamórfica", "Sedimentaria", "Volcánica"], "respuesta": 0},
        {"pregunta": "¿Cuál es el mineral más abundante en la corteza terrestre?", "opciones": ["Feldespato", "Cuarzo", "Mica", "Olivino"], "respuesta": 0},
        {"pregunta": "¿Cómo se llama la escala que mide la dureza de los minerales?", "opciones": ["Richter", "Mohs", "Beaufort", "Mercalli"], "respuesta": 1}
    ],
    "Estructural": [
        {"pregunta": "¿Qué es una falla geológica?", "opciones": ["Un volcán", "Un pliegue de roca", "Un plano de fractura con desplazamiento", "Un depósito de minerales"], "respuesta": 2},
        {"pregunta": "¿Qué tipo de esfuerzo produce fallas inversas?", "opciones": ["Compresión", "Tensión", "Cizalla", "Flexión"], "respuesta": 0},
        {"pregunta": "¿Cómo se llama la fuerza que actúa en direcciones opuestas en un plano de falla?", "opciones": ["Esfuerzo compresivo", "Esfuerzo tensional", "Esfuerzo cortante", "Esfuerzo elástico"], "respuesta": 2}
    ],
    "Sedimentología": [
        {"pregunta": "¿Qué es una roca sedimentaria?", "opciones": ["Roca formada por enfriamiento de magma", "Roca formada por acumulación de sedimentos", "Roca metamórfica", "Roca con estructura cristalina"], "respuesta": 1},
        {"pregunta": "¿Cuál es un ejemplo de roca sedimentaria?", "opciones": ["Granito", "Caliza", "Basalto", "Cuarzo"], "respuesta": 1},
        {"pregunta": "¿Qué proceso transforma sedimentos en roca sedimentaria?", "opciones": ["Erosión", "Compactación y cementación", "Fusión", "Metamorfismo"], "respuesta": 1}
    ]
}

# Estado inicial
if "nombre_jugador" not in st.session_state:
    st.session_state.nombre_jugador = ""
if "categoria_seleccionada" not in st.session_state:
    st.session_state.categoria_seleccionada = ""
if "indice_pregunta" not in st.session_state:
    st.session_state.indice_pregunta = 0
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "preguntas" not in st.session_state:
    st.session_state.preguntas = []

# Pantalla de inicio
st.title("📡 Quiz de Geología - ACGGP")
if st.session_state.nombre_jugador == "":
    st.session_state.nombre_jugador = st.text_input("✍️ Ingresa tu nombre para comenzar:")

# Selección de categoría
if st.session_state.nombre_jugador and st.session_state.categoria_seleccionada == "":
    st.subheader("Selecciona una categoría")
    for categoria in preguntas_por_categoria.keys():
        if st.button(categoria):
            st.session_state.categoria_seleccionada = categoria
            st.session_state.preguntas = random.sample(preguntas_por_categoria[categoria], 5)
            st.session_state.indice_pregunta = 0
            st.session_state.puntaje = 0
            st.rerun()

# Mostrar preguntas
if st.session_state.categoria_seleccionada:
    categoria = st.session_state.categoria_seleccionada
    if imagenes_categoria[categoria]:
        st.image(imagenes_categoria[categoria], width=500)
    
    if st.session_state.indice_pregunta < len(st.session_state.preguntas):
        pregunta_actual = st.session_state.preguntas[st.session_state.indice_pregunta]
        st.subheader(f"Pregunta {st.session_state.indice_pregunta + 1} de 5")
        st.write(f"❓ {pregunta_actual['pregunta']}")
        respuesta_usuario = st.radio("Selecciona una opción:", pregunta_actual["opciones"], index=None)
        
        if st.button("Responder"):
            if respuesta_usuario is not None:
                if pregunta_actual["opciones"].index(respuesta_usuario) == pregunta_actual["respuesta"]:
                    st.success("✅ ¡Correcto!")
                    st.session_state.puntaje += 1
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}")
                
                if st.button("Siguiente pregunta ➡️"):
                    st.session_state.indice_pregunta += 1
                    st.rerun()
    else:
        st.subheader(f"🎉 ¡Juego terminado, {st.session_state.nombre_jugador}! Tu puntaje final es {st.session_state.puntaje}/5")
        if st.button("🔄 Volver a jugar"):
            st.session_state.categoria_seleccionada = ""
            st.session_state.nombre_jugador = ""
            st.rerun()
