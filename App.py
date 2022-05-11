from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'banco'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes


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
        name=""
        id=0
        for tup in data:
            if tup[1] == user and tup[0] == passw:
                flag = True
                id=tup[3]
                name=tup[2]
        print(name)
        if(flag):
            if name=="cliente":
                ide=int(id)
                print(type(id),id)
                cur = mysql.connection.cursor()
                squery="select nrocuenta,saldo,fecha from usuario xu, cuenta xc WHERE xu.id=xc.idusuario and xu.id ="+str(id)
                cur.execute(squery)
                mysql.connection.commit()
                data = cur.fetchall()
                cur.close()
                return render_template('index-client.html',accounts=data)
            elif name=="administrador":
                cur = mysql.connection.cursor()
                cur.execute("select * from usuario")
                mysql.connection.commit()
                data = cur.fetchall()
                cur.close()
                return render_template('index-admin.html',users=data)
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
        cur.execute("INSERT into usuario(ci,nombre,apellidoP,apellidoM,username,contrasenia,rol)VALUES(%s,%s,%s,%s,%s,%s,'cliente')", (ci, nombre, app,apm,user,contr))
        mysql.connection.commit()
        data = cur.fetchall()
        cur.close()
        flash('Contact Added successfully')
        return render_template('index-admin.html',users=data)
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
