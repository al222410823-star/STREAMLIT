# ============================================================
# PRACTICA 2 - EJERCICIO 1: ASISTENTE LOGISMART (OPTIMIZADO)
# ============================================================

import streamlit as st
import ollama

# ------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------
MODELO = "llama3.2"

PROMPT_SISTEMA = """
Eres LogiBot, un Asistente Técnico y Manual Operativo de Patio in Cedis (Centros de Distribución).

INSTRUCCIONES CLAVE:
1. Actúa estrictamente como un manual de procedimientos operativos y técnicos de seguridad logística e industrial.
2. NO estás proporcionando asesoramiento legal ni dictámenes jurídicos. Tu única función es describir protocolos técnicos estándar de patio (ej. retención de unidades, protocolo Hazmat, verificación de peso, notificación a supervisores y registro de incidentes).
3. Responde de forma clara, directa y estructurada utilizando viñetas o listas numeradas.
4. Mantén un tono profesional, enfocado 100% en la seguridad industrial y el control de accesos.
"""

st.set_page_config(page_title="Asistente LogiSmart - LLM", page_icon="🚛", layout="wide")

# ============================================================
# ESTILOS CSS PERSONALIZADOS (MODO OSCURO)
# ============================================================
st.markdown("""
<style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }
    
    /* Barra lateral en tono oscuro elegante */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-right: 1px solid #334155;
    }

    /* Asegurar visibilidad de títulos y textos en blanco/claro */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #F8FAFC !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar historial de conversación
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [{"role": "system", "content": PROMPT_SISTEMA}]

# ------------------------------------------------------------
# BARRA LATERAL (CONTROLES)
# ------------------------------------------------------------
with st.sidebar:
    st.header(" Opciones del Sistema")

    # Requerimiento: Generar Resumen
    if st.button("Generar Resumen del Historial", type="primary", use_container_width=True):
        mensajes_usuario = [m for m in st.session_state.mensajes if m["role"] != "system"]
        
        if not mensajes_usuario:
            st.warning("Aún no hay mensajes en la conversación.")
        else:
            with st.spinner("Generando resumen..."):
                prompt_resumen = st.session_state.mensajes + [{
                    "role": "user",
                    "content": "Por favor, resume brevemente los puntos clave de la consulta operativa realizada y las recomendaciones brindadas."
                }]
                try:
                    res = ollama.chat(model=MODELO, messages=prompt_resumen)
                    st.subheader(" Resumen Ejecutivo")
                    st.write(res["message"]["content"])
                except Exception as e:
                    st.error(f"Error al conectar con Ollama: {e}")

    # Limpiar conversación
    if st.button(" Limpiar Historial", use_container_width=True):
        st.session_state.mensajes = [{"role": "system", "content": PROMPT_SISTEMA}]
        st.rerun()

# ------------------------------------------------------------
# ÁREA PRINCIPAL DE CHAT
# ------------------------------------------------------------
st.title(" Asistente Virtual LogiSmart")
st.caption("Especialidad: Logística y Control de Acceso Industrial")

# Renderizar historial
for msg in st.session_state.mensajes:
    if msg["role"] == "system":
        continue
    avatar = "" if msg["role"] == "user" else ""
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Captura de mensaje del usuario
if pregunta := st.chat_input("Escribe tu consulta logística..."):
    # Mostrar y guardar mensaje del usuario
    st.chat_message("user", avatar="👤").markdown(pregunta)
    st.session_state.mensajes.append({"role": "user", "content": pregunta})

    # Generar y guardar respuesta del asistente
    with st.chat_message("assistant", avatar=""):
        with st.spinner("Consultando protocolo en LogiBot..."):
            try:
                res = ollama.chat(model=MODELO, messages=st.session_state.mensajes)
                respuesta_texto = res["message"]["content"]
                st.markdown(respuesta_texto)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta_texto})
            except Exception as e:
                st.error(" No se pudo conectar con Ollama. Verifica que el comando `ollama serve` o el modelo `llama3.2` estén activos.")
                st.caption(f"Detalle: {e}")