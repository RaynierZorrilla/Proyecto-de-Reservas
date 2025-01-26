from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

app.secret_key = 'supersecretkey'  # Necesario para usar sesiones y flash messages


@app.route('/')
def index():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
        return redirect(url_for('login'))

    return render_template('index.html', username=session['username'])


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

# Ruta para eliminar una reserva
@app.route('/reserva_reserva/<int:id>', methods=['GET', 'POST'])
def eliminar_reserva(id):
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()

    # Eliminar la reserva con el ID proporcionado
    cursor.execute('DELETE FROM reservas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('reservas'))

#Ruta para registrar un nuevo usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            error = 'Las contraseñas no coinciden.'
            return render_template('register.html', error=error)

        # Verificar si el usuario ya existe
        conn = sqlite3.connect('reservas.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            error = 'El nombre de usuario ya existe. Por favor, elige otro.'
            return render_template('register.html', error=error)

        # Si el usuario no existe, registrarlo
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        success = 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.'
        return render_template('register.html', success=success)

    return render_template('register.html')


# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('reservas.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
