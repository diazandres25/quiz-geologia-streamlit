import streamlit as st
import random
import time
import pandas as pd

# Configurar la página
st.set_page_config(page_title="Quiz de Geología - ACGGP", page_icon="🌍", layout="wide")

# Cargar imagen de ACGGP
st.image("https://www.acggp.org/images/logo.png", width=200)

# Categorías de preguntas
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

# Inicializar variables de estado
if "historial_puntajes" not in st.session_state:
    st.session_state.historial_puntajes = {}
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

# Solicitar el nombre del jugador
st.title("🌍 Quiz de Geología - ACGGP")
st.write("Pon a prueba tus conocimientos en geología con este quiz de la ACGGP.")

if st.session_state.nombre_jugador == "":
    st.session_state.nombre_jugador = st.text_input("✍️ Ingresa tu nombre para comenzar:")

if st.session_state.nombre_jugador and st.session_state.categoria_seleccionada == "":
    st.write("Selecciona una categoría de preguntas:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🌎 General"):
        st.session_state.categoria_seleccionada = "General"
        st.session_state.preguntas = random.sample(preguntas_por_categoria["General"], len(preguntas_por_categoria["General"]))
    if col2.button("🏗️ Estructural"):
        st.session_state.categoria_seleccionada = "Estructural"
        st.session_state.preguntas = random.sample(preguntas_por_categoria["Estructural"], len(preguntas_por_categoria["Estructural"]))
    if col3.button("⛏️ Sedimentología"):
        st.session_state.categoria_seleccionada = "Sedimentología"
        st.session_state.preguntas = random.sample(preguntas_por_categoria["Sedimentología"], len(preguntas_por_categoria["Sedimentología"]))

# Mostrar preguntas si hay una categoría seleccionada
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
        st.session_state.historial_puntajes[st.session_state.nombre_jugador] = st.session_state.puntaje

        # Mostrar ranking de los mejores 5 jugadores
        st.subheader("🏆 Ranking de jugadores")
        ranking = sorted(st.session_state.historial_puntajes.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (jugador, puntaje) in enumerate(ranking, start=1):
            st.write(f"{i}. {jugador}: {puntaje} puntos")

        if st.button("🔄 Volver a jugar"):
            st.session_state.categoria_seleccionada = ""
            st.session_state.indice_pregunta = 0
            st.session_state.puntaje = 0
            st.session_state.respuesta_mostrada = False
            st.rerun()

