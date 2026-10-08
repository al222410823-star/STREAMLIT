import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 1. Cargar las variables de entorno (.env)
load_dotenv()

# 2. Leer las variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
DB_NAME = os.getenv("MONGO_DB", "MARYCRUZ73")
COLECCION_NOMBRE = os.getenv("MONGO_COLECCION", "LogiSmartM73")

# 3. Construir la URI de conexión
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"

def insertar_semillas():
    try:
        # Conectar a MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=4000)
        client.admin.command("ping")
        db = client[DB_NAME]
        coleccion = db[COLECCION_NOMBRE]

        # Lista de documentos semilla proporcionados
        semillas = [
            {
                "placa": "XYZ-123",
                "categoria": "Seguridad",
                "descripcion": "Fuga de aceite patio 2"
            },
            {
                "placa": "ABC-789",
                "categoria": "Mantenimiento",
                "descripcion": "Falla de luces"
            },
            {
                "placa": "XYZ-123",
                "categoria": "Fuga",
                "severidad": "ALTA",
                "requiere_revision_humana": True,
                "descripcion": "El camión con placa XYZ-123 presentó fuga de líquido en patio 2."
            }
        ]

        # Insertar los documentos en la colección
        resultado = coleccion.insert_many(semillas)
        print(f"¡Se insertaron {len(resultado.inserted_ids)} documentos semilla con éxito en la base de datos '{DB_NAME}'!")

    except Exception as e:
        print(f"Error al conectar o insertar en MongoDB: {e}")

if __name__ == "__main__":
    insertar_semillas()