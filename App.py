from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask import request

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bankaccounts'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
def consultaCliente():
    cur = mysql.connection.cursor()
    squery="select nrocuenta,saldo,fecha from usuario xu, cuenta xc WHERE xu.id=xc.idusuario and xu.id ="+str(id)
    cur.execute(squery)
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    return data

@app.route('/')
def Index():
    
    return render_template('signin.html')
    

@app.route('/signin', methods=['POST'])
def add_contact():
    print('hola')
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("select contrasenia,username,rol,id from usuario")
        mysql.connection.commit()
        data = cur.fetchall()
        cur.close()
        print(data[0])
        flag = False
        name = ""
        id = 0
        for tup in data:
            if tup[1] == user and tup[0] == passw:
                flag = True
                id = tup[3]
                name = tup[2]
        print(name)
        if(flag):
            if name == "cliente":
                ide = int(id)
                print(type(id), id)
                cur = mysql.connection.cursor()
                squery="select nrocuenta,saldo,fecha, xu.id, xc.idcuenta from usuario xu, cuenta xc WHERE xu.id=xc.idusuario and xu.id ="+str(id)
                cur.execute(squery)
                mysql.connection.commit()
                data = cur.fetchall()
                cur.close()
                return render_template('index-client.html', accounts=data)
            elif name == "administrador":
                cur = mysql.connection.cursor()
                cur.execute("select * from usuario")
                mysql.connection.commit()
                data = cur.fetchall()
                cur.close()
                return render_template('index-admin.html', users=data)
        else:
            #flash('Contact Added successfully')
            return render_template('signin.html')


@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        ci = request.form['ci']
        nombre = request.form['nombre']
        app = request.form['ape_pat']
        apm = request.form['ape_mat']
        user = request.form['username']
        contr = request.form['contrasenia']
        cur = mysql.connection.cursor()
        cur.execute("INSERT into usuario(ci,nombre,apellidoP,apellidoM,username,contrasenia,rol)VALUES(%s,%s,%s,%s,%s,%s,'cliente')",
                    (ci, nombre, app, apm, user, contr))
        mysql.connection.commit()
        data = cur.fetchall()
        cur.close()
        flash('Contact Added successfully')
        return render_template('index-admin.html', users=data)


@app.route('/retiro', methods=['POST'])
def retiro():
    if request.method == 'POST':
        nroc = request.form['nrocuenta']
        #nroc=request.args.get('nrocuenta','no contiene')
        #monto=request.args.get('monto','no contiene')
        cur = mysql.connection.cursor()
        cur.execute("SELECT xu.nombre,xu.apellidoP,xu.apellidoM,xc.saldo,xc.idcuenta FROM usuario xu, cuenta xc WHERE xu.id=xc.idusuario and xc.nrocuenta=%s", (nroc))
        mysql.connection.commit()
        data = cur.fetchall()
        cur.close()
        saldo=data[0][3]
        idcuenta=data[0][4]
        if(monto<saldo):
            flash('Retiro exitoso¡¡')
            actual=saldo -monto
            cur = mysql.connection.cursor()
            cur.execute("UPDATE cuenta set saldo=50000 WHERE idcuenta=%s", (idcuenta))
            mysql.connection.commit()
            data = cur.fetchall()
            cur.close()
        else:
            flash('No cuenta con saldo suficiente¡¡')
        data=consultaCliente()
        return render_template('index-cliente.html',users=data)


@app.route('/saldo', methods=['POST'])
def saldo():
    if request.method == 'POST':
        #ide=request.args.get('id','no contiene')
        #nroc=request.args.get('brocuenta','no contiene')
        nroc = request.form['nrocuenta']
        cur = mysql.connection.cursor()
        cur.execute("SELECT xu.nombre,xu.apellidoP,xu.apellidoM,xc.saldo FROM usuario xu, cuenta xc WHERE  xu.id=xc.idusuario and xc.nrocuenta=%s", (nroc))
        mysql.connection.commit()
        data = cur.fetchall()
        cur.close()
        saldo=data[0][3]
        flash('Saldo actual: '+str(saldo))
        data=consultaCliente()
        return render_template('index-cliente.html',users=data)



@app.route('/transferencia', methods=['POST'])
def transferencia():
    if request.method == 'POST':
        org = request.form['origen']
        dest = request.form['destino']
        monto = request.form['monto']
        cur = mysql.connection.cursor()
        cur.execute("SELECT saldo,nrocuenta from cuenta")
        mysql.connection.commit()
        data = cur.fetchall()
        cur.close()
        flag=False
        for tup in data:
            if tup[1]==dest:
                flag=True
        if flag:
            cur = mysql.connection.cursor()
            cur.execute("SELECT saldo,nrocuenta from cuenta")
            mysql.connection.commit()
            data = cur.fetchall()
            flash('Saldo actual: '+str(saldo))
            cur.close()
        else:
            flash('Saldo actual: '+str(saldo))

                
        
        data=consultaCliente()
        return render_template('index-cliente.html',users=data)
    pass


@app.route('/deposito', methods=['POST'])
def deposito():
    pass


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuario WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
