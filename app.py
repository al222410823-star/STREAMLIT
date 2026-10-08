import os
import json
import streamlit as st
import ollama
from pymongo import MongoClient
from dotenv import load_dotenv

# 1. Cargar las variables de entorno (.env)
load_dotenv()

# 2. Leer las variables del .env
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
DB_NAME = os.getenv("MONGO_DB", "MARYCRUZ73")
COLECCION_NOMBRE = os.getenv("MONGO_COLECCION", "LogiSmartM73")

# 3. Construir la URI de MongoDB Atlas
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"

MODELO = "llama3.2"

PROMPT_SISTEMA = """
Eres LogiBot, un Asistente Técnico y Manual Operativo de Patio en Cedis.
Responde de forma clara, directa y estructurada utilizando viñetas o listas.
"""

st.set_page_config(
    page_title="LogiSmart - Sistema de Control de Patio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILOS CSS PERSONALIZADOS (DISEÑO MODERNO)
# ============================================================

st.markdown("""
<style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: # !important;
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Barra lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1f2937;
    }

    /* Tarjetas de Métricas */
    [data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.875rem !important;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 1.75rem !important;
        font-weight: 700;
    }

    /* Encabezados y textos */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    p, span, label {
        color: #cbd5e1 !important;
    }

    /* Pestañas (Tabs) personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #1f2937;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 8px;
        color: #94a3b8;
        padding: 10px 18px;
        font-weight: 600;
        border: 1px solid #334155;
        transition: all 0.2s ease-in-out;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #334155;
        color: #f8fafc;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border-color: #0ea5e9 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }

    /* Gráficas */
    [data-testid="stVegaLiteChart"] {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #334155;
    }

    /* Botones */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        border: none;
    }

    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONEXIÓN A MONGODB ATLAS
# ============================================================

@st.cache_resource
def init_connection():
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=4000
        )

        client.admin.command("ping")

        return client[DB_NAME]

    except Exception as e:
        st.error(f" Error de conexión a MongoDB: {e}")
        return None


db = init_connection()


# ============================================================
# HISTORIAL DE CONVERSACIÓN
# ============================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "system",
            "content": PROMPT_SISTEMA
        }
    ]


# ============================================================
# BARRA LATERAL
# ============================================================

with st.sidebar:

    st.header(" Opciones del Sistema")

    if st.button(
        " Generar Resumen del Historial",
        type="primary",
        use_container_width=True
    ):

        mensajes_usuario = [
            m for m in st.session_state.mensajes
            if m["role"] != "system"
        ]

        if not mensajes_usuario:

            st.warning(
                "Aún no hay mensajes en la conversación."
            )

        else:

            with st.spinner(
                "Generando resumen ejecutivo..."
            ):

                prompt_resumen = (
                    st.session_state.mensajes
                    + [
                        {
                            "role": "user",
                            "content":
                                "Por favor, resume brevemente "
                                "los puntos clave de la consulta realizada."
                        }
                    ]
                )

                try:

                    res = ollama.chat(
                        model=MODELO,
                        messages=prompt_resumen
                    )

                    st.subheader(
                        " Resumen Ejecutivo"
                    )

                    st.write(
                        res["message"]["content"]
                    )

                except Exception as e:

                    st.error(
                        f"Error al conectar con Ollama: {e}"
                    )

    if st.button(
        " Limpiar Historial de Chat",
        use_container_width=True
    ):

        st.session_state.mensajes = [
            {
                "role": "system",
                "content": PROMPT_SISTEMA
            }
        ]

        st.rerun()


# ============================================================
# TÍTULO PRINCIPAL
# ============================================================

st.title(
    " LogiSmart: Plataforma de Gestión de Patio"
)


# ============================================================
# PESTAÑAS PRINCIPALES
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Panel de Control",
    " Control de Acceso",
    " Simulador Lógico",
    "Incidentes",
    " Riesgos Éticos",
    " Asistente RAG",
])


# ============================================================
# PESTAÑA 1: PANEL DE CONTROL
# ============================================================

with tab1:

    st.header("Indicadores Clave de Patio")

    col1, col2, col3 = st.columns(3)

    if db is not None:

        coleccion = db[COLECCION_NOMBRE]

        total_registros = coleccion.count_documents({})

        total_incidentes = coleccion.count_documents({
            "categoria": {
                "$exists": True
            }
        })

        total_camiones = coleccion.count_documents({
            "placa": {
                "$exists": True
            }
        })

        col1.metric(
            "Camiones / Registros",
            total_camiones
            if total_camiones > 0
            else total_registros
        )

        col2.metric(
            "Incidentes Totales",
            total_incidentes
        )

        col3.metric(
            "Registros Totales en DB",
            total_registros
        )

        st.subheader(
            "Incidentes por Categoría"
        )

        pipeline = [

            {
                "$match": {
                    "categoria": {
                        "$exists": True
                    }
                }
            },

            {
                "$group": {
                    "_id": "$categoria",
                    "total": {
                        "$sum": 1
                    }
                }
            },

            {
                "$sort": {
                    "total": -1
                }
            }
        ]

        resultados = list(
            coleccion.aggregate(pipeline)
        )

        if resultados:

            datos_grafica = {
                item["_id"]: item["total"]
                for item in resultados
                if item["_id"] is not None
            }

            st.bar_chart(
                datos_grafica
            )

        else:

            st.info(
                "Sin datos de 'categoria' "
                "en la colección para proyectar gráficas."
            )

    else:

        col1.metric(
            "Camiones Registrados",
            0
        )

        col2.metric(
            "Incidentes Totales",
            0
        )

        col3.metric(
            "Registros Totales",
            0
        )


# ============================================================
# PESTAÑA 2: CONTROL DE ACCESO
# ============================================================

with tab2:

    st.header(
        " Evaluación Lógica de Ingreso"
    )

    col_sw1, col_sw2 = st.columns(2)

    with col_sw1:

        P = st.toggle(
            "P: Documentación en regla",
            value=True
        )

        Q = st.toggle(
            "Q: Placa con reporte de robo / sobrepeso",
            value=False
        )

    with col_sw2:

        R = st.toggle(
            "R: Carga Peligrosa / Hazmat",
            value=False
        )

        S = st.toggle(
            "S: Inspección de Seguridad aprobada",
            value=True
        )

    A = P and S and (not Q)

    E = P and (R or Q)

    R3 = R and (not S)

    R4 = Q and R

    st.subheader(
        "Resultado de Evaluación:"
    )

    if R4:

        st.error(
            "BLOQUEO TOTAL "
            "(Regla 4: Placa Reportada + Hazmat)"
        )

    elif R3:

        st.error(
            "INGRESO DENEGADO - "
            "Hazmat Crítico sin Inspección "
            "(Regla 3)"
        )

    elif A:

        st.success(
            " ACCESO PERMITIDO "
            "(Regla 1: P ∧ S ∧ ¬Q)"
        )

    elif E:

        st.warning(
            "⚠️ INSPECCIÓN ESPECIAL REQUERIDA "
            "(Regla 2: P ∧ (R ∨ Q))"
        )

    else:

        st.error(
            "INGRESO RECHAZADO: "
            "No cumple premisas básicas"
        )


# ============================================================
# PESTAÑA 3: TABLA DE VERDAD
# ============================================================

with tab3:

    st.header(
        " Tabla de Verdad de Reglas Operativas"
    )

    filas = []

    for p in [True, False]:

        for q in [True, False]:

            for r in [True, False]:

                for s in [True, False]:

                    filas.append({

                        "P": p,

                        "Q": q,

                        "R": r,

                        "S": s,

                        "Acceso (A)":
                            p and s and (not q),

                        "Especial (E)":
                            p and (r or q),

                        "Hazmat Crítico (R3)":
                            r and (not s),

                        "Bloqueo (R4)":
                            q and r
                    })

    st.table(filas)


# ============================================================
# PESTAÑA 4: BANDEJA DE INCIDENTES
# ============================================================

with tab4:

    st.header(
        " Clasificación de Incidentes"
    )

    correo_texto = st.text_area(
        "Pegar texto del correo/incidente:",
        height=100,
        value=(
            "El camión con placa XYZ-123 "
            "presentó fuga de líquido en patio 2."
        )
    )

    if st.button(
        " Clasificar y Guardar Incidente",
        type="primary"
    ):

        prompt_clasificar = f"""
        Clasifica el siguiente reporte de incidente en JSON
        con las llaves:

        "placa"
        (si existe en el texto, ej: XYZ-123),

        "categoria"
        (Seguridad, Mantenimiento, Operativo, Fuga),

        "severidad"
        (ALTA, MEDIA, BAJA),

        "requiere_revision_humana"
        (true/false).

        Texto: {correo_texto}

        Devuelve SOLO el objeto JSON.
        """

        try:

            res = ollama.chat(
                model=MODELO,
                messages=[
                    {
                        "role": "user",
                        "content": prompt_clasificar
                    }
                ],
                format="json"
            )

            st.subheader(
                "Respuesta del Clasificador:"
            )

            st.code(
                res["message"]["content"],
                language="json"
            )

            # GUARDAR EN MONGODB

            if db is not None:

                datos = json.loads(
                    res["message"]["content"]
                )

                datos["descripcion"] = correo_texto

                db[
                    COLECCION_NOMBRE
                ].insert_one(datos)

                st.success(
                    "¡Incidente registrado con éxito "
                    "en MongoDB!"
                )

                st.rerun()

        except Exception as e:

            st.error(
                f"Error procesando incidente: {e}"
            )

    st.subheader(
        " Registros Guardados en MongoDB"
    )

    if db is not None:

        docs = list(
            db[
                COLECCION_NOMBRE
            ].find(
                {},
                {
                    "_id": 0
                }
            )
        )

        st.json(docs)


# ============================================================
# PESTAÑA 5: RIESGOS ÉTICOS
# ============================================================

with tab5:

    st.header(
        "⚖️ Riesgos Éticos e IA Residual"
    )

    if db is not None:

        riesgos_data = list(
            db[
                COLECCION_NOMBRE
            ].find(
                {
                    "tipo": "riesgo_etico"
                },
                {
                    "_id": 0
                }
            )
        )

        st.json(
            riesgos_data
            if riesgos_data
            else {
                "info":
                    "Sin registros de riesgos éticos específicos."
            }
        )


# ============================================================
# PESTAÑA 6: ASISTENTE RAG
# ============================================================

with tab6:

    st.header(
        " Asistente RAG & Consultas Directas"
    )

    for msg in st.session_state.mensajes:

        if msg["role"] != "system":

            avatar = (
                ""
                if msg["role"] == "user"
                else ""
            )

            with st.chat_message(
                msg["role"],
                avatar=avatar
            ):

                st.markdown(
                    msg["content"]
                )

    if pregunta := st.chat_input(
        "Escribe tu consulta o pregunta por una placa (ej. XYZ-123)..."
    ):

        pregunta_limpia = (
            pregunta
            .strip()
            .strip("\"'")
        )

        with st.chat_message(
            "user",
            avatar=""
        ):

            st.markdown(
                pregunta_limpia
            )

        st.session_state.mensajes.append({
            "role": "user",
            "content": pregunta_limpia
        })

        # ----------------------------------------------------
        # BÚSQUEDA RAG EN MONGODB
        # ----------------------------------------------------

        contexto_db = ""

        if db is not None:

            doc = db[
                COLECCION_NOMBRE
            ].find_one({

                "$or": [

                    {
                        "placa": {
                            "$regex":
                                pregunta_limpia,
                            "$options": "i"
                        }
                    },

                    {
                        "descripcion": {
                            "$regex":
                                pregunta_limpia,
                            "$options": "i"
                        }
                    }
                ]
            })

            if doc:

                contexto_db = (
                    f"\n[DATOS EN DB]: "
                    f"{json.dumps(doc, default=str)}"
                )

        mensajes_para_ollama = list(
            st.session_state.mensajes
        )

        if contexto_db:

            mensajes_para_ollama[-1] = {

                "role": "user",

                "content": (
                    f"{pregunta_limpia}\n\n"
                    f"[CONTEXTO BASE DE DATOS]:"
                    f"{contexto_db}"
                )
            }

        with st.chat_message(
            "assistant",
            avatar=""
        ):

            with st.spinner(
                "LogiBot está respondiendo..."
            ):

                try:

                    res = ollama.chat(
                        model=MODELO,
                        messages=mensajes_para_ollama
                    )

                    respuesta_llm = (
                        res["message"]["content"]
                    )

                    st.markdown(
                        respuesta_llm
                    )

                    st.session_state.mensajes.append({
                        "role": "assistant",
                        "content": respuesta_llm
                    })

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Error al obtener respuesta "
                        f"de Ollama: {e}"
                    )


