# ============================================================
# FASE 5 - CLASIFICADOR HÍBRIDO DE INCIDENTES
# ============================================================

import json
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
DB_NAME = os.getenv("MONGO_DB", "MARYCRUZ73")

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"


def clasificar_incidente_hibrido(placa, tipo, descripcion, nivel, guardar_db=True):
    """
    Clasifica un incidente determinando su prioridad y, opcionalmente,
    lo registra en la base de datos de MongoDB Atlas.
    """

    # --------------------------------------------------------
    # Determinación de Prioridad por Nivel
    # --------------------------------------------------------
    if nivel >= 8:
        prioridad = "CRITICA"
    elif nivel >= 5:
        prioridad = "ALTA"
    elif nivel >= 3:
        prioridad = "MEDIA"
    else:
        prioridad = "BAJA"

    # Estructura del documento
    doc_incidente = {
        "placa": placa,
        "tipo": tipo,
        "descripcion": descripcion,
        "nivel": nivel,
        "prioridad": prioridad,
        "fecha": datetime.now().isoformat()
    }

    # --------------------------------------------------------
    # Persistencia en MongoDB Atlas
    # --------------------------------------------------------
    if guardar_db:
        try:
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            resultado = db.incidentes.insert_one(doc_incidente)
            
            # Convertimos el ObjectId de MongoDB a cadena de texto para evitar el error de serialización JSON
            doc_incidente["_id"] = str(resultado.inserted_id)
            print(f"✅ Incidente guardado en MongoDB con ID: {doc_incidente['_id']}")
        except Exception as e:
            print(f"⚠️ Error al guardar incidente en MongoDB: {e}")

    # Retornar en formato JSON estandarizado
    return json.dumps({"incidente": doc_incidente}, indent=4, ensure_ascii=False)


def enviar_correo_soporte(destinatario, asunto, mensaje):
    """Simulación del envío de correo."""
    print("\n========== CORREO DE SOPORTE ==========")
    print("Destinatario:", destinatario)
    print("Asunto:", asunto)
    print("Mensaje:", mensaje)
    print("========================================")


if __name__ == "__main__":
    print("\n========== PRUEBA FASE 5: CLASIFICADOR HÍBRIDO ==========")

    json_res = clasificar_incidente_hibrido(
        placa="XYZ-789",
        tipo="Control de Acceso",
        descripcion="Exceso de peso detectado en báscula principal",
        nivel=8,
        guardar_db=True
    )

    print("\nJSON generado:")
    print(json_res)