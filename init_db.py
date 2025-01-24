import sqlite3

conn = sqlite3.connect('reservas.db')
cursor = conn.cursor()

# Crear tabla de reservas (ya existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    telefono TEXT,
    email TEXT,
    detalles TEXT
)
''')

# Crear tabla de usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()
