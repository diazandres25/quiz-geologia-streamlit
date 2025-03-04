import streamlit as st
import random
import time
import pandas as pd

# Configurar la página con un diseño más profesional
st.set_page_config(page_title="Quiz de Geología Estructural - ACGGP", page_icon="⛏️", layout="centered")

# Base de datos de preguntas
preguntas = [
    {"pregunta": "¿Qué es una falla en geología estructural?",
     "opciones": [
         "Una capa de roca que se desplaza.",
         "Un plano de discontinuidad en el que ocurre un desplazamiento.",
         "Una estructura que mantiene su forma original.",
         "Un perfil de estrato que se encuentra horizontalmente."
     ], "respuesta": 1},

    {"pregunta": "¿Qué valor representa el desplazamiento neto (A) en una falla?",
     "opciones": [
         "La medida vertical entre la corriente de agua y la falla.",
         "El movimiento lateral de dos bloques rocosos.",
         "La suma total del desplazamiento en todas las direcciones.",
         "La diferencia entre el desplazamiento vertical y horizontal de la falla."
     ], "respuesta": 2},

    {"pregunta": "En el contexto de un corte geológico, ¿qué se construye a partir de un mapa geológico?",
     "opciones": [
         "Un modelo tridimensional de las capas.",
         "La proyección de un perfil de la geología subyacente.",
         "Un esquema de elucubración de las rocas.",
         "Un corte general que ignora las capas específicas."
     ], "respuesta": 1}
]

# Barajar preguntas al iniciar
random.shuffle(preguntas)

# Inicializar estado de respuestas
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "indice_pregunta" not in st.session_state:
    st.session_state.indice_pregunta = 0
if "nombre_jugador" not in st.session_state:
    st.session_state.nombre_jugador = ""
if "respuesta_mostrada" not in st.session_state:
    st.session_state.respuesta_mostrada = False
if "tiempo_inicio" not in st.session_state:
    st.session_state.tiempo_inicio = None

# Preguntar nombre del jugador al inicio
st.title("📡 Quiz de Geología Estructural - ACGGP")
st.write("Pon a prueba tus conocimientos sobre geología estructural y la ACGGP.")

if st.session_state.nombre_jugador == "":
    st.session_state.nombre_jugador = st.text_input("✍️ Ingresa tu nombre para comenzar:")

if st.session_state.nombre_jugador and st.session_state.indice_pregunta < len(preguntas):
    # Obtener la pregunta actual
    indice = st.session_state.indice_pregunta
    pregunta_actual = preguntas[indice]

    # Iniciar temporizador
    if st.session_state.tiempo_inicio is None:
        st.session_state.tiempo_inicio = time.time()
    tiempo_restante = max(0, 10 - (time.time() - st.session_state.tiempo_inicio))
    st.progress(tiempo_restante / 10)

    if tiempo_restante == 0:
        st.warning("⏳ ¡Tiempo agotado! Pasamos a la siguiente pregunta.")
        st.session_state.indice_pregunta += 1
        st.session_state.tiempo_inicio = None
        st.rerun()

    # Mostrar pregunta y opciones
    st.subheader(f"🔹 Pregunta {indice + 1} de {len(preguntas)}")
    st.write(f"❓ {pregunta_actual['pregunta']}")

    respuesta_usuario = st.radio("Selecciona una opción:", pregunta_actual["opciones"], index=None)

    # Botón de responder
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
        st.session_state.tiempo_inicio = None
        st.rerun()

# Mostrar resultado final
elif st.session_state.indice_pregunta >= len(preguntas):
    st.subheader(f"🎉 ¡Juego terminado, {st.session_state.nombre_jugador}! Tu puntaje final es {st.session_state.puntaje}/{len(preguntas)}")
    
    # Guardar puntaje en archivo CSV
    historial_file = "historial_puntajes.csv"
    nuevo_puntaje = pd.DataFrame([[st.session_state.nombre_jugador, st.session_state.puntaje]], columns=["Jugador", "Puntaje"])
    
    try:
        historial = pd.read_csv(historial_file)
        historial = pd.concat([historial, nuevo_puntaje], ignore_index=True)
    except FileNotFoundError:
        historial = nuevo_puntaje

    historial.to_csv(historial_file, index=False, encoding='utf-8')

    # Mostrar ranking
    st.subheader("🏆 Ranking de jugadores")
    historial = historial.sort_values(by="Puntaje", ascending=False).head(5)
    st.dataframe(historial)

    # Botón para reiniciar el quiz
    if st.button("🔄 Volver a jugar"):
        st.session_state.puntaje = 0
        st.session_state.indice_pregunta = 0
        st.session_state.respuesta_mostrada = False
        st.session_state.tiempo_inicio = None
        st.rerun()
