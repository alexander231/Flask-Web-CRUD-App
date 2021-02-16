from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = "Vreau10laPIBD"
# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profesori')
def profesori():
    conn = mysql.connection
    cur = conn.cursor()
    resultValue = cur.execute("SELECT * FROM profesori")
    
    profesoriDetails = cur.fetchall()
        

    return render_template('profesori.html', profesoriDetails=profesoriDetails)



    

@app.route('/add_contact', methods=['POST'])
def add_profesori():
    conn = mysql.connection
    cur = conn.cursor()
    if request.method == 'POST':
        nume = request.form['nume']
        prenume = request.form['prenume']
        data_nastere = request.form['data_nastere']
        salariu = request.form['salariu']
        cur.execute("INSERT INTO profesori (nume, prenume, data_nastere, salariu) VALUES (%s,%s,%s,%s)", (nume, prenume, data_nastere, salariu))
        conn.commit()
        flash('Profesor adaugat cu succes')
        return redirect(url_for('profesori'))

        
@app.route('/edit_profesori/<id>', methods = ['POST', 'GET'])
def get_profesori(id):
    conn = mysql.connection
    cur = conn.cursor()

    cur.execute('SELECT * FROM profesori WHERE idprofesor = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_profesori.html', profesoriDetails = data[0])

@app.route('/update_profesori/<id>', methods=['POST'])
def update_profesori(id):
    if request.method == 'POST':
        nume = request.form['nume']
        prenume = request.form['prenume']
        data_nastere = request.form['data_nastere']
        salariu = request.form['salariu']
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("""
            UPDATE profesori
            SET nume = %s,
                prenume = %s,
                data_nastere = %s,
                salariu = %s
            WHERE idprofesor = %s
        """, (nume, prenume, data_nastere, salariu, id))
        flash('Profesor updatat cu succes')
        conn.commit()
        return redirect(url_for('profesori'))

@app.route('/delete_profesori/<string:id>', methods = ['POST','GET'])
def delete_profesori(id):
    conn = mysql.connection
    cur = conn.cursor()
  
    cur.execute('DELETE FROM profesori WHERE idprofesor = {0}'.format(id))
    conn.commit()
    flash('Profesor sters cu succes')
    return redirect(url_for('profesori'))

@app.route('/departamente')
def departamente():
    conn = mysql.connection
    cur = conn.cursor()
    resultValue = cur.execute("SELECT * FROM departamente")
    
    departamenteDetails = cur.fetchall()
        

    return render_template('departamente.html', departamenteDetails = departamenteDetails)
    

@app.route('/add_contactd', methods=['POST'])
def add_departamente():
    conn = mysql.connection
    cur = conn.cursor()
    if request.method == 'POST':
        nume = request.form['nume']
        nr_angajati = request.form['nr_angajati']
        buget = request.form['buget']
        
        cur.execute("INSERT INTO departamente (nume, nr_angajati, buget) VALUES (%s,%s,%s)", (nume, nr_angajati, buget))
        conn.commit()
        flash('Departament adaugat cu succes')
        return redirect(url_for('departamente'))
@app.route('/edit_departamente/<id>', methods = ['POST', 'GET'])
def get_departamente(id):
    conn = mysql.connection
    cur = conn.cursor()

    cur.execute('SELECT * FROM departamente WHERE iddepartament = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_departamente.html', departamenteDetails = data[0])

@app.route('/update_departamente/<id>', methods=['POST'])
def update_departamente(id):
    if request.method == 'POST':
        nume = request.form['nume']
        nr_angajati = request.form['nr_angajati']
        buget = request.form['buget']
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("""
            UPDATE departamente
            SET nume = %s,
                nr_angajati = %s,
                buget = %s
            WHERE iddepartament = %s
        """, (nume, nr_angajati, buget, id))
        flash('Departament updatat cu succes')
        conn.commit()
        return redirect(url_for('departamente'))

@app.route('/delete_departamente/<string:id>', methods = ['POST','GET'])
def delete_departamente(id):
    conn = mysql.connection
    cur = conn.cursor()
  
    cur.execute('DELETE FROM departamente WHERE iddepartament = {0}'.format(id))
    conn.commit()
    flash('Departament sters cu succes')
    return redirect(url_for('departamente'))

@app.route('/cursuri')
def cursuri():
    conn = mysql.connection
    cur = conn.cursor()
    
    resultValue = cur.execute('SELECT c.idcurs, c.idprofesor idprofesor_curs, a.nume nume_profesor, a.prenume prenume_profesor, a.data_nastere, a.salariu, c.iddepartament iddepartament_curs, b.nume nume_departament, b.nr_angajati, b.buget, c.nume nume_curs, c.credite, c.ore_pe_semestru from profesori a, departamente b, cursuri c WHERE a.idprofesor = c.idprofesor AND b.iddepartament = c.iddepartament;')
    
    cursuriDetails = cur.fetchall()
    res2 = cur.execute("SELECT * FROM departamente")
    departamenteDetails = cur.fetchall()
    res1 = cur.execute("SELECT * FROM profesori")
    profesoriDetails = cur.fetchall()

    return render_template('cursuri.html', cursuriDetails=cursuriDetails, profesoriDetails = profesoriDetails, departamenteDetails = departamenteDetails)

@app.route('/add_contactc', methods=['POST'])
def add_cursuri():
    conn = mysql.connection
    cur = conn.cursor()
    if request.method == 'POST':
        idprofesor = request.form['idprofesor']
        iddepartament = request.form['iddepartament']
        nume = request.form['nume']
        credite = request.form['credite']
        ore_pe_semestru = request.form['ore_pe_semestru']
        
        cur.execute('INSERT INTO cursuri (idprofesor, iddepartament, nume, credite, ore_pe_semestru) VALUES (%s,%s,%s,%s,%s)', (idprofesor, iddepartament, nume, credite, ore_pe_semestru))
        conn.commit()
        flash('Curs adaugat cu succes')
        return redirect(url_for('cursuri'))
@app.route('/edit_cursuri/<id>', methods = ['POST', 'GET'])
def get_cursuri(id):
    conn = mysql.connection
    cur = conn.cursor()

    cur.execute('SELECT * FROM cursuri WHERE idcurs = %s', [id])
    data = cur.fetchall()
    res2 = cur.execute("SELECT * FROM departamente")
    departamenteDetails = cur.fetchall()
    res1 = cur.execute("SELECT * FROM profesori")
    profesoriDetails = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_cursuri.html', cursuriDetails = data[0], profesoriDetails = profesoriDetails, departamenteDetails = departamenteDetails)

@app.route('/update_cursuri/<id>', methods=['POST'])
def update_cursuri(id):
    if request.method == 'POST':
        idprofesor = request.form['idprofesor']
        iddepartament = request.form['iddepartament']
        nume = request.form['nume']
        credite = request.form['credite']
        ore_pe_semestru = request.form['ore_pe_semestru']
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("""
            UPDATE cursuri
            SET idprofesor = %s,
                iddepartament = %s,
                nume = %s,
                credite = %s,
                ore_pe_semestru = %s
            WHERE idcurs = %s
        """, (idprofesor, iddepartament, nume, credite, ore_pe_semestru, id))
        flash('Curs updatat cu succes')
        conn.commit()
        return redirect(url_for('cursuri'))

@app.route('/delete_cursuri/<string:id>', methods = ['POST','GET'])
def delete_cursuri(id):
    conn = mysql.connection
    cur = conn.cursor()
  
    cur.execute('DELETE FROM cursuri WHERE idcurs = {0}'.format(id))
    conn.commit()
    flash('Curs sters cu succes')
    return redirect(url_for('cursuri'))
if __name__ == '__main__':
    app.run(debug = True)