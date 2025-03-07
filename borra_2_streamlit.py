import streamlit as st
import random
import time
import pandas as pd
import os

# Configurar la página con un diseño más profesional
st.set_page_config(page_title="Geolimpiadas - ACGGP", page_icon="⛏️", layout="centered")

# Archivo CSV para almacenar los puntajes
CSV_FILE = "puntajes.csv"

# Crear archivo si no existe
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = pd.DataFrame(columns=["Nombre", "Puntaje"])
        writer.to_csv(CSV_FILE, index=False)

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

# Registro del jugador
st.title("🌍 Geolimpiadas - ACGGP")
nombre = st.text_input("✍️ Ingresa tu nombre para comenzar:")

if nombre:
    categoria = st.selectbox("📌 Selecciona una categoría:", list(preguntas_por_categoria.keys()))
    if categoria:
        preguntas = random.sample(preguntas_por_categoria[categoria], len(preguntas_por_categoria[categoria]))
        puntaje = 0
        for i, pregunta in enumerate(preguntas):
            st.subheader(f"❓ Pregunta {i + 1}")
            st.write(pregunta["pregunta"])
            respuesta_usuario = st.radio("Selecciona una opción:", pregunta["opciones"], index=None, key=f"q{i}")
            if st.button("Responder", key=f"resp_{i}"):
                if respuesta_usuario is not None:
                    if pregunta["opciones"].index(respuesta_usuario) == pregunta["respuesta"]:
                        st.success("✅ ¡Correcto!")
                        puntaje += 1
                    else:
                        st.error(f"❌ Incorrecto. La respuesta correcta era: {pregunta['opciones'][pregunta['respuesta']]}")
                if i < len(preguntas) - 1:
                    st.button("Siguiente pregunta", key=f"next_{i}")
                else:
                    st.subheader(f"🎉 Has terminado el quiz, {nombre}!")
                    st.write(f"Tu puntaje final: {puntaje}")

                    # Guardar puntaje en CSV
                    df = pd.read_csv(CSV_FILE)
                    df = pd.concat([df, pd.DataFrame([[nombre, puntaje]], columns=["Nombre", "Puntaje"])], ignore_index=True)
                    df.to_csv(CSV_FILE, index=False)



