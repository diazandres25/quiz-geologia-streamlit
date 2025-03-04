import streamlit as st
import random
import time
import pandas as pd

# Configurar la página
st.set_page_config(page_title="Quiz de Geología Estructural - ACGGP", page_icon="\u26cf\ufe0f", layout="centered")

# Base de datos de preguntas
preguntas = [
    {
        "categoria": "ACGGP",
        "pregunta": "¿Qué es la ACGGP?",
        "opciones": [
            "Una asociación dedicada a la biología marina.",
            "Una organización que promueve la geología y geofísica en Colombia.",
            "Una empresa de perforación de pozos.",
            "Un sindicato de trabajadores petroleros."
        ],
        "respuesta": 1
    },
    {
        "categoria": "ACGGP",
        "pregunta": "¿Cuál es el objetivo de la ACGGP?",
        "opciones": [
            "Regular los precios del petróleo en Colombia.",
            "Capacitar y promover el desarrollo de geólogos y geofísicos.",
            "Realizar exploraciones en el Amazonas.",
            "Controlar la producción de gas en el país."
        ],
        "respuesta": 1
    },
    {
        "categoria": "Geología Estructural",
        "pregunta": "¿Cómo se mide el buzamiento de una capa?",
        "opciones": [
            "A través de la distancia lateral que recorre.",
            "Mediante el ángulo entre la horizontal y la capa.",
            "A través de la proyección sobre un plano vertical.",
            "Mediante el desplazamiento neto de los bloques adyacentes."
        ],
        "respuesta": 1
    },
    {
        "categoria": "Geología Estructural",
        "pregunta": "¿Qué representa el ángulo de cabeceo en una falla?",
        "opciones": [
            "La inclinación desde la base hasta la cima de una montaña.",
            "La distancia entre dos puntos de mayor elevación.",
            "La inclinación de la capa en relación con la superficie horizontal.",
            "La distancia vertical de un punto a un plano inclinado."
        ],
        "respuesta": 2
    }
]

# Barajar preguntas al iniciar
random.shuffle(preguntas)

# Inicializar estado de respuestas
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "indice_pregunta" not in st.session_state:
    st.session_state.indice_pregunta = 0
if "tiempo_inicio" not in st.session_state:
    st.session_state.tiempo_inicio = time.time()
if "nombre_jugador" not in st.session_state:
    st.session_state.nombre_jugador = ""

# Preguntar nombre del jugador al inicio
if st.session_state.nombre_jugador == "":
    st.session_state.nombre_jugador = st.text_input("\ud83d\udc64 Ingresa tu nombre para comenzar:")

if st.session_state.nombre_jugador and st.session_state.indice_pregunta < len(preguntas):
    # Obtener la pregunta actual
    indice = st.session_state.indice_pregunta
    pregunta_actual = preguntas[indice]

    # Mostrar pregunta y opciones
    st.subheader(f"\ud83d\udd39 {pregunta_actual['categoria']} - Pregunta {indice + 1}")
    st.write(f"❓ {pregunta_actual['pregunta']}")

    respuesta_usuario = st.radio("Selecciona una opción:", pregunta_actual["opciones"], index=None)

    # Calcular tiempo restante
    tiempo_transcurrido = time.time() - st.session_state.tiempo_inicio
    tiempo_restante = max(0, 10 - tiempo_transcurrido)
    st.progress(tiempo_restante / 10)

    if tiempo_restante == 0:
        st.warning("⏳ ¡Tiempo agotado! Pasamos a la siguiente pregunta.")
        st.session_state.indice_pregunta += 1
        st.session_state.tiempo_inicio = time.time()
        st.experimental_rerun()

    # Botón de responder
    if st.button("Responder"):
        if respuesta_usuario is not None:
            if pregunta_actual["opciones"].index(respuesta_usuario) == pregunta_actual["respuesta"]:
                st.success("✅ ¡Correcto!")
                st.session_state.puntaje += 1
            else:
                st.error(f"❌ Incorrecto. La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}")
            
            # Siguiente pregunta
            st.session_state.indice_pregunta += 1
            st.session_state.tiempo_inicio = time.time()
            st.experimental_rerun()

# Mostrar resultado final
elif st.session_state.indice_pregunta >= len(preguntas):
    st.subheader(f"🎉 ¡Juego terminado! Tu puntaje final es {st.session_state.puntaje}/{len(preguntas)}")
    
    # Guardar puntaje en archivo CSV
    historial_file = "historial_puntajes.csv"
    nuevo_puntaje = pd.DataFrame([[st.session_state.nombre_jugador, st.session_state.puntaje]], columns=["Jugador", "Puntaje"])
    
    try:
        historial = pd.read_csv(historial_file)
        historial = pd.concat([historial, nuevo_puntaje], ignore_index=True)
    except FileNotFoundError:
        historial = nuevo_puntaje

    historial.to_csv(historial_file, index=False)

    # Mostrar ranking
    st.subheader("🏆 Ranking de jugadores")
    historial = historial.sort_values(by="Puntaje", ascending=False).head(5)
    st.dataframe(historial)

    # Botón para reiniciar el quiz
    if st.button("🔄 Volver a jugar"):
        st.session_state.puntaje = 0
        st.session_state.indice_pregunta = 0
        st.session_state.tiempo_inicio = time.time()
        st.experimental_rerun()
