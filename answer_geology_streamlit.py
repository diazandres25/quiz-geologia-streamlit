import streamlit as st
import random
import pandas as pd
import os

st.set_page_config(page_title="Geolimpiadas - ACGGP", page_icon="🌍", layout="centered")

CSV_FILE = "puntajes.csv"
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Nombre", "Puntaje"]).to_csv(CSV_FILE, index=False)

imagenes_por_categoria = {
    "General": "imagenes/general.jpg",
    "Estructural": "imagenes/estructural.jpg",
    "Sedimentología": "imagenes/sedimentologia.jpg"
}

preguntas_por_categoria = {
    "General": [
        {"pregunta": "¿Qué es la geología?", "opciones": ["Estudio de los animales", "Estudio de la Tierra", "Estudio del clima", "Estudio del agua"], "respuesta": 1, "imagen": "imagenes/geologia.jpg"},
        {"pregunta": "¿Cuál es la capa más externa de la Tierra?", "opciones": ["Núcleo", "Manto", "Corteza", "Litosfera"], "respuesta": 2, "imagen": "imagenes/corteza.jpg"}
    ],
    "Estructural": [
        {"pregunta": "¿Qué es una falla geológica?", "opciones": ["Un volcán", "Un pliegue de roca", "Un plano de fractura con desplazamiento", "Un depósito de minerales"], "respuesta": 2, "imagen": "imagenes/falla.jpg"}
    ]
}

st.markdown("<div class='title'>🌍 Geolimpiadas - ACGGP</div>", unsafe_allow_html=True)

if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "categoria" not in st.session_state:
    st.session_state.categoria = ""
if "preguntas" not in st.session_state:
    st.session_state.preguntas = []
if "indice_pregunta" not in st.session_state:
    st.session_state.indice_pregunta = 0
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "respuesta_mostrada" not in st.session_state:
    st.session_state.respuesta_mostrada = False

if st.session_state.nombre == "":
    st.session_state.nombre = st.text_input("✍️ Ingresa tu nombre para comenzar:")
    if st.session_state.nombre:
        st.rerun()

elif st.session_state.categoria == "":
    st.subheader("📌 Selecciona una categoría:")
    for categoria in preguntas_por_categoria.keys():
        if st.button(categoria, key=categoria):
            st.session_state.categoria = categoria
            st.session_state.preguntas = random.sample(preguntas_por_categoria[categoria], min(10, len(preguntas_por_categoria[categoria])))
            st.session_state.indice_pregunta = 0
            st.session_state.puntaje = 0
            st.session_state.respuesta_mostrada = False
            st.rerun()

elif st.session_state.indice_pregunta < len(st.session_state.preguntas):
    pregunta_actual = st.session_state.preguntas[st.session_state.indice_pregunta]
    st.subheader(f"❓ Pregunta {st.session_state.indice_pregunta + 1}")
    
    if "imagen" in pregunta_actual:
        st.image(pregunta_actual["imagen"], use_column_width=True)

    st.write(pregunta_actual["pregunta"])
    respuesta_usuario = st.radio("Selecciona una opción:", pregunta_actual["opciones"], index=None, key=f"pregunta_{st.session_state.indice_pregunta}")
    
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
    st.subheader(f"🎉 ¡Juego terminado, {st.session_state.nombre}!")
    st.write(f"Tu puntaje final: {st.session_state.puntaje}/5")

    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([[st.session_state.nombre, st.session_state.puntaje]], columns=["Nombre", "Puntaje"])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    
    if st.button("🔄 Volver a jugar"):
        for key in ["nombre", "categoria", "preguntas", "indice_pregunta", "puntaje", "respuesta_mostrada"]:
            st.session_state[key] = "" if key in ["nombre", "categoria"] else 0
        st.rerun()
