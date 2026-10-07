
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
DB_NAME = os.getenv("MONGO_DB", "MARYCRUZ73")
COLECCION_NOMBRE = os.getenv("MONGO_COLECCION", "LogiSmartM73")

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"

print("🔄 Conectando a MongoDB Atlas...")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ ¡Conexión exitosa a MongoDB Atlas!")

    db = client[DB_NAME]
    coleccion = db[COLECCION_NOMBRE]

    datos_ejemplo = [
        {
            "placa": "XYZ-123",
            "chofer": "Juan Pérez",
            "categoria": "Seguridad",
            "severidad": "ALTA",
            "descripcion": "Fuga de aceite en patio 2.",
            "requiere_revision": True
        },
        {
            "placa": "ABC-789",
            "chofer": "María Gómez",
            "categoria": "Mantenimiento",
            "severidad": "MEDIA",
            "descripcion": "Falla en luces traseras al ingresar.",
            "requiere_revision": False
        },
        {
            "placa": "DEF-456",
            "chofer": "Carlos López",
            "categoria": "Operativo",
            "severidad": "BAJA",
            "descripcion": "Retraso en entrega de documentación.",
            "requiere_revision": False
        }
    ]

    resultado = coleccion.insert_many(datos_ejemplo)
    print(f" Se insertaron {len(resultado.inserted_ids)} registros de prueba en '{COLECCION_NOMBRE}'.")

    total = coleccion.count_documents({})
    print(f" Total de registros en '{COLECCION_NOMBRE}': {total}")

except Exception as e:
    print(f"❌ Error de conexión o inserción: {e}")
