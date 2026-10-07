# ============================================================
# FASE 3 - POBLACIÓN INICIAL DE BASE DE DATOS LOGISMART (ATLAS)
# ============================================================

import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
DB_NAME = os.getenv("MONGO_DB", "MARYCRUZ73")

# Construir la URI para MongoDB Atlas
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"

def poblar_base_datos():
    try:
        print(" Conectando a MongoDB Atlas...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Prueba de conexión rápida
        client.admin.command('ping')
        print(f" Conexión exitosa a la base de datos de Atlas: '{DB_NAME}'")

        # 1. Colección: camiones
        db.camiones.drop()
        db.camiones.insert_many([
            {"placa": "ABC-123", "conductor": "Juan Pérez", "capacidad_ton": 20.0, "tipo_carga": "General", "estado": "Activo"},
            {"placa": "XYZ-789", "conductor": "Carlos López", "capacidad_ton": 15.0, "tipo_carga": "Peligrosa", "estado": "Activo"},
            {"placa": "MNO-456", "conductor": "Ana Gómez", "capacidad_ton": 30.0, "tipo_carga": "Refrigerada", "estado": "Mantenimiento"}
        ])
        print(" Colección 'camiones' poblada.")

        # 2. Colección: accesos
        db.accesos.drop()
        db.accesos.insert_many([
            {"placa": "ABC-123", "fecha_ingreso": datetime.now(), "peso_registrado_ton": 18.5, "autorizado": True, "puerta": "Norte"},
            {"placa": "XYZ-789", "fecha_ingreso": datetime.now(), "peso_registrado_ton": 17.2, "autorizado": False, "puerta": "Sur"}
        ])
        print(" Colección 'accesos' poblada.")

        # 3. Colección: incidentes
        db.incidentes.drop()
        db.incidentes.insert_many([
            {"placa": "XYZ-789", "fecha": datetime.now().isoformat(), "tipo": "Control de acceso", "prioridad": "CRITICA", "descripcion": "Vehículo detectado con peso excedido", "nivel": 8},
            {"placa": "MNO-456", "fecha": datetime.now().isoformat(), "tipo": "Documentación", "prioridad": "MEDIA", "descripcion": "Falta manifiesto de carga refrigerada", "nivel": 4}
        ])
        print("Colección 'incidentes' poblada.")

        # 4. Colección: riesgos_eticos
        db.riesgos_eticos.drop()
        db.riesgos_eticos.insert_many([
            {"modulo": "Cámara de detección", "riesgo": "Sesgo en condiciones nocturnas", "categoria": "Sesgo", "impacto": "Alto", "probabilidad": "Media", "mitigacion": "Pruebas con diferentes condiciones de iluminación"},
            {"modulo": "Sistema de vigilancia", "riesgo": "Uso inadecuado de información personal", "categoria": "Privacidad", "impacto": "Alto", "probabilidad": "Media", "mitigacion": "Aplicar controles de acceso y políticas de retención"}
        ])
        print(" Colección 'riesgos_eticos' poblada.")

        # 5. Colección: evaluaciones_llm
        db.evaluaciones_llm.drop()
        db.evaluaciones_llm.insert_many([
            {"modelo": "llama3.2", "fecha_prueba": datetime.now(), "exactitud": 0.93, "latencia_promedio_ms": 450, "total_evaluados": 30}
        ])
        print(" Colección 'evaluaciones_llm' poblada.")

        print(f"\n ¡Población de las 5 colecciones completada con éxito en Atlas ('{DB_NAME}')!")

    except Exception as e:
        print(f"❌ Error al conectar o poblar MongoDB Atlas: {e}")

if __name__ == "__main__":
    poblar_base_datos()