import streamlit as st
import random
import time
import pandas as pd

# Configurar la página
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
     ], "respuesta": 1},

    {"pregunta": "¿Cómo se mide el buzamiento de una capa?",
     "opciones": [
         "A través de la distancia lateral que recorre.",
         "Mediante el ángulo entre la horizontal y la capa.",
         "A través de la proyección sobre un plano vertical.",
         "Mediante el desplazamiento neto de los bloques adyacentes."
     ], "respuesta": 1},

    {"pregunta": "¿Cuál de los siguientes materiales se necesita para trabajar con fallas?",
     "opciones": [
         "Calculadora y colores.",
         "Papel pulido y pluma de gel.",
         "Regla en milímetros y compás.",
         "Hojas de papel fotográfico y tinta especial."
     ], "respuesta": 2}
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
    st.session_state.nombre_jugador = st.text_input("Ingresa tu nombre para comenzar:")

if st.session_state.nombre_jugador and st.session_state.indice_pregunta < len(preguntas):
    # Obtener la pregunta actual
    indice = st.session_state.indice_pregunta
    pregunta_actual = preguntas[indice]

    # Mostrar pregunta y opciones
    st.subheader(f"🔹 Pregunta {indice + 1}")
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
        st.rerun()

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
            st.rerun()

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

    historial.to_csv(historial_file, index=False, encoding='utf-8')

    # Mostrar ranking
    st.subheader("🏆 Ranking de jugadores")
    historial = historial.sort_values(by="Puntaje", ascending=False).head(5)
    st.dataframe(historial)

    # Botón para reiniciar el quiz
    if st.button("🔄 Volver a jugar"):
        st.session_state.puntaje = 0
        st.session_state.indice_pregunta = 0
        st.session_state.tiempo_inicio = time.time()
        st.rerun()
