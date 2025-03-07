import streamlit as st
import random
import csv
import os
import pandas as pd

# Configurar la página con un diseño llamativo
st.set_page_config(page_title="Geolimpiadas - ACGGP", page_icon="🌍", layout="centered")

# Archivo CSV para almacenar los puntajes
CSV_FILE = "puntajes.csv"

# Crear archivo si no existe
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Puntaje"])

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

# Registro del jugador
nombre = st.text_input("✍️ Ingresa tu nombre:")

if nombre:
    if st.button("Registrarse"):
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([nombre, 0])
        st.success(f"Jugador {nombre} registrado. Elige una categoría para comenzar el quiz.")

    # Seleccionar categoría
    st.subheader("📌 Elige una categoría para comenzar:")
    col1, col2, col3 = st.columns(3)

    categoria_seleccionada = None
    if col1.button("🌍 General"):
        categoria_seleccionada = "General"
    if col2.button("🏗️ Estructural"):
        categoria_seleccionada = "Estructural"
    if col3.button("⛏️ Sedimentología"):
        categoria_seleccionada = "Sedimentología"

    # Iniciar quiz
    if categoria_seleccionada:
        preguntas = random.sample(preguntas_por_categoria[categoria_seleccionada], min(10, len(preguntas_por_categoria[categoria_seleccionada])))
        puntaje = 0
        indice_pregunta = 0

        while indice_pregunta < len(preguntas):
            pregunta_actual = preguntas[indice_pregunta]
            st.subheader(f"❓ Pregunta {indice_pregunta + 1} de {len(preguntas)}")
            st.write(pregunta_actual["pregunta"])
            respuesta_usuario = st.radio("Selecciona una opción:", pregunta_actual["opciones"], index=None)

            if st.button("Responder"):
                if respuesta_usuario is not None:
                    if pregunta_actual["opciones"].index(respuesta_usuario) == pregunta_actual["respuesta"]:
                        st.success("✅ ¡Correcto!")
                        puntaje += 1
                    else:
                        st.error(f"❌ Incorrecto. La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}")

                if st.button("Siguiente pregunta ➡️"):
                    indice_pregunta += 1

        # Guardar puntaje en CSV
        with open(CSV_FILE, mode="r", newline="") as file:
            reader = list(csv.reader(file))
            for row in reader:
                if row[0] == nombre:
                    row[1] = str(puntaje)
                    break
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(reader)

        st.subheader(f"🎉 Has terminado el quiz, {nombre}!")
        st.write(f"Tu puntaje final: {puntaje}")

# Mostrar clasificación
st.subheader("🏆 Clasificación Total")
with open(CSV_FILE, mode="r", newline="") as file:
    reader = csv.reader(file)
    datos = list(reader)
st.table(datos)
