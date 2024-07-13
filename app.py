from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'turismo'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM lugares')
    lugares = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', lugares=lugares)

@app.route('/add', methods=['POST'])
def add():
    nombre = request.form['nombre']
    zona_turistica = request.form['zona_turistica']
    provincia = request.form['provincia']
    descripcion = request.form['descripcion']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO lugares (nombre, zona_turistica, provincia, descripcion) VALUES (%s, %s, %s, %s)',
                   (nombre, zona_turistica, provincia, descripcion))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        zona_turistica = request.form['zona_turistica']
        provincia = request.form['provincia']
        descripcion = request.form['descripcion']
        
        cursor.execute('UPDATE lugares SET nombre = %s, zona_turistica = %s, provincia = %s, descripcion = %s WHERE id = %s',
                       (nombre, zona_turistica, provincia, descripcion, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    
    cursor.execute('SELECT * FROM lugares WHERE id = %s', (id,))
    lugar = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', lugar=lugar)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lugares WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
