import sqlite3
from pathlib import Path

# Ruta de la base de datos
RUTA_DB = Path(__file__).parent / "memoria.db"


def conectar():
    return sqlite3.connect(RUTA_DB)


def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recuerdos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT NOT NULL,
            categoria TEXT NOT NULL,
            informacion TEXT NOT NULL,
            origen TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracion (
            usuario_id TEXT PRIMARY KEY,
            memoria_automatica INTEGER DEFAULT 0
        )
    """)

    conexion.commit()
    conexion.close()
