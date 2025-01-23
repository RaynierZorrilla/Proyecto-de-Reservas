from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

app.secret_key = 'supersecretkey'  # Necesario para usar sesiones y flash messages


@app.route('/')
def index():
    return render_template('index.html')

# Ruta para crear una nueva reserva
@app.route('/reserva', methods=['GET', 'POST'])
def reservar():
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        hora = request.form['hora']
        telefono = request.form['telefono']
        email = request.form['email']
        detalles = request.form['detalles']

        # Validación de los campos
        if not nombre or not apellido or not fecha or not hora:
            # Si algún campo obligatorio está vacío
            return "Todos los campos son obligatorios", 400
        
        if not telefono.isdigit():
            # Validar que el teléfono contenga solo números
            return "El teléfono debe contener solo números", 400
        
        if not email or "@" not in email:
            # Validar formato de email
            return "El correo electrónico no es válido", 400



        # Conectar a la base de datos y guardar la reserva
        conn = sqlite3.connect('reservas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reservas (nombre, apellido, fecha, hora, telefono, email, detalles)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, fecha, hora, telefono, email, detalles))
        conn.commit()
        conn.close()

        # Redirigir a la misma página después de guardar
        return redirect(url_for('reservar'))
    
    # Renderizar formulario para crear reserva
    return render_template('reservar.html')

# Ruta para listar todas las reservas
@app.route('/reservas')
def reservas():
    # Conectar a la base de datos y obtener las reservas
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reservas')
    reservas = cursor.fetchall()
    conn.close()

    # Renderizar la lista de reservas
    return render_template('reservas.html', reservas=reservas)


if __name__ == '__main__':
    app.run(debug=True)
