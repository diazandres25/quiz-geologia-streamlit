import streamlit as st
import random
import pandas as pd
import os

# Configurar la página con un diseño llamativo
st.set_page_config(page_title="Geolimpiadas - ACGGP", page_icon="🌍", layout="centered")

# Archivo CSV para almacenar los puntajes de cada jugador
CSV_FILE = "puntajes.csv"
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Nombre", "Puntaje"]).to_csv(CSV_FILE, index=False)

# Estilos mejorados
st.markdown(
    """
    <style>
        .title { text-align: center; font-size: 50px; font-weight: bold; color: #2c3e50; }
        .subtext { text-align: center; font-size: 20px; color: #34495e; }
        .category-button { width: 100%; height: 100px; font-size: 24px; margin: 10px 0; }
        .question-box { text-align: center; font-size: 24px; margin-top: 20px; }
        .answer-box { text-align: left; font-size: 18px; margin-bottom: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='title'>🌍 Geolimpiadas - ACGGP</div>", unsafe_allow_html=True)

# Base de datos de preguntas
preguntas_por_categoria = {
    "General": [
        {"pregunta": "¿Qué es la geología?", "opciones": ["Estudio de los animales", "Estudio de la Tierra", "Estudio del clima", "Estudio del agua"], "respuesta": 1},
        {"pregunta": "¿Cuál es la capa más externa de la Tierra?", "opciones": ["Núcleo", "Manto", "Corteza", "Litosfera"], "respuesta": 2},
        {"pregunta": "¿Qué tipo de roca es el granito?", "opciones": ["Ígnea", "Metamórfica", "Sedimentaria", "Volcánica"], "respuesta": 0},
        {"pregunta": "¿Cuál es el mineral más abundante en la corteza terrestre?", "opciones": ["Feldespato", "Cuarzo", "Mica", "Olivino"], "respuesta": 0},
        {"pregunta": "¿Cómo se llama la escala que mide la dureza de los minerales?", "opciones": ["Richter", "Mohs", "Beaufort", "Mercalli"], "respuesta": 1},
        {"pregunta": "¿Cuál es el proceso de transformación de rocas por calor y presión?", "opciones": ["Erosión", "Compactación", "Metamorfismo", "Fusión"], "respuesta": 2},
        {"pregunta": "¿Qué gas es el más abundante en la atmósfera terrestre?", "opciones": ["Oxígeno", "Nitrógeno", "Dióxido de carbono", "Argón"], "respuesta": 1},
        {"pregunta": "¿Qué tipo de roca se forma por el enfriamiento del magma?", "opciones": ["Ígnea", "Sedimentaria", "Metamórfica", "Carbonatada"], "respuesta": 0},
        {"pregunta": "¿Cuál es el agente principal de la erosión?", "opciones": ["Agua", "Viento", "Glaciares", "Seres vivos"], "respuesta": 0},
        {"pregunta": "¿Cómo se llama la capa más interna de la Tierra?", "opciones": ["Núcleo", "Manto", "Corteza", "Litosfera"], "respuesta": 0}
    ],
    "Estructural": [
        {"pregunta": "¿Qué es una falla geológica?", "opciones": ["Un volcán", "Un pliegue de roca", "Un plano de fractura con desplazamiento", "Un depósito de minerales"], "respuesta": 2},
        {"pregunta": "¿Qué tipo de esfuerzo produce fallas inversas?", "opciones": ["Compresión", "Tensión", "Cizalla", "Flexión"], "respuesta": 0},
        {"pregunta": "¿Cómo se llama la fuerza que actúa en direcciones opuestas en un plano de falla?", "opciones": ["Esfuerzo compresivo", "Esfuerzo tensional", "Esfuerzo cortante", "Esfuerzo elástico"], "respuesta": 2},
        {"pregunta": "¿Qué estructura geológica forma un pliegue anticlinorio?", "opciones": ["Las capas más jóvenes en el centro", "Las capas más antiguas en el centro", "Rocas intrusivas", "Zonas de subducción"], "respuesta": 1},
        {"pregunta": "¿Qué instrumento se usa para medir la dirección de una falla?", "opciones": ["Brújula geológica", "Sismógrafo", "GPS", "Dinamómetro"], "respuesta": 0},
        {"pregunta": "¿Cómo se llama el punto de inicio de un terremoto?", "opciones": ["Epicentro", "Hipocentro", "Foco sísmico", "Placa tectónica"], "respuesta": 1},
        {"pregunta": "¿Qué es una discordancia angular?", "opciones": ["Un pliegue abierto", "Un límite entre rocas de diferentes edades con inclinaciones distintas", "Una falla de tipo normal", "Un depósito de sedimentos en el océano"], "respuesta": 1},
        {"pregunta": "¿Qué tipo de pliegue tiene un eje inclinado?", "opciones": ["Anticlinal", "Sinclinal", "Inclinados", "Recumbentes"], "respuesta": 2},
        {"pregunta": "¿Qué tipo de falla produce un desplazamiento horizontal?", "opciones": ["Inversa", "Normal", "De desgarre", "Plana"], "respuesta": 2},
        {"pregunta": "¿Qué ocurre en una zona de subducción?", "opciones": ["Una placa oceánica se hunde bajo otra", "Dos placas chocan y forman montañas", "Las placas se deslizan lateralmente", "Se forma una nueva corteza oceánica"], "respuesta": 0}
    ],
    "Sedimentología": [
        {"pregunta": "¿Qué es una roca sedimentaria?", "opciones": ["Roca formada por enfriamiento de magma", "Roca formada por acumulación de sedimentos", "Roca metamórfica", "Roca con estructura cristalina"], "respuesta": 1},
        {"pregunta": "¿Cuál es un ejemplo de roca sedimentaria?", "opciones": ["Granito", "Caliza", "Basalto", "Cuarzo"], "respuesta": 1},
        {"pregunta": "¿Qué proceso transforma sedimentos en roca sedimentaria?", "opciones": ["Erosión", "Compactación y cementación", "Fusión", "Metamorfismo"], "respuesta": 1},
        {"pregunta": "¿Qué tipo de roca sedimentaria se forma por precipitación química?", "opciones": ["Caliza", "Arenisca", "Conglomerado", "Pizarra"], "respuesta": 0},
        {"pregunta": "¿Qué agente transporta sedimentos en ríos?", "opciones": ["Gravedad", "Viento", "Hielo", "Agua"], "respuesta": 3},
        {"pregunta": "¿Cuál es la principal característica de los estratos sedimentarios?", "opciones": ["Color", "Fósiles", "Capas horizontales", "Tamaño de grano"], "respuesta": 2},
        {"pregunta": "¿Qué es una turbidita?", "opciones": ["Depósito de origen volcánico", "Sedimentos transportados por corrientes de turbidez", "Roca ígnea", "Fósil marino"], "respuesta": 1},
        {"pregunta": "¿Qué determina el tamaño del grano en una roca sedimentaria?", "opciones": ["Tipo de mineral", "Energía del medio de transporte", "Presión tectónica", "Profundidad de formación"], "respuesta": 1},
        {"pregunta": "¿Qué roca sedimentaria es rica en carbono?", "opciones": ["Arenisca", "Lutita", "Carbón", "Pizarra"], "respuesta": 2},
        {"pregunta": "¿Cuál es el principal agente formador de dunas?", "opciones": ["Agua", "Hielo", "Viento", "Gravedad"], "respuesta": 2}
    ]
}


# Estado de la aplicación
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

# Registro del jugador
if st.session_state.nombre == "":
    st.session_state.nombre = st.text_input("✍️ Ingresa tu nombre para comenzar:")
    if st.session_state.nombre:
        st.rerun()

# Selección de categoría
elif st.session_state.categoria == "":
    st.subheader("📌 Selecciona una categoría:")
    for categoria in preguntas_por_categoria.keys():
        if st.button(categoria, key=categoria, help=f"Iniciar preguntas sobre {categoria}"):
            st.session_state.categoria = categoria
            st.session_state.preguntas = random.sample(preguntas_por_categoria[categoria], min(10, len(preguntas_por_categoria[categoria])))
            st.session_state.indice_pregunta = 0
            st.session_state.puntaje = 0
            st.session_state.respuesta_mostrada = False
            st.rerun()

# Mostrar preguntas
elif st.session_state.indice_pregunta < 5:
    pregunta_actual = st.session_state.preguntas[st.session_state.indice_pregunta]
    st.subheader(f"❓ Pregunta {st.session_state.indice_pregunta + 1} de 5")
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

# Mostrar resultado final
else:
    st.subheader(f"🎉 ¡Juego terminado, {st.session_state.nombre}!")
    st.write(f"Tu puntaje final: {st.session_state.puntaje}/5")
    
    # Guardar puntaje en CSV
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([[st.session_state.nombre, st.session_state.puntaje]], columns=["Nombre", "Puntaje"])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    
    # Botón para reiniciar
    if st.button("🔄 Volver a jugar"):
        for key in ["nombre", "categoria", "preguntas", "indice_pregunta", "puntaje", "respuesta_mostrada"]:
            st.session_state[key] = "" if key in ["nombre", "categoria"] else 0
        st.rerun()
