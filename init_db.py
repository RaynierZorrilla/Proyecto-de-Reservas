import sqlite3

def init_db():
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()

    # Crear tabla reservas si no existe
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
    conn.commit()
    conn.close()

# Ejecutar el script para inicializar la base de datos
if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada correctamente.")
