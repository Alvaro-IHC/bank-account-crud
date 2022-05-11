from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

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


@app.route('/')
def Index():
    return render_template('signin.html')


@app.route('/signin', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("select password,username from usuario")
        mysql.connection.commit()
        data = cur.fetchall()
        cur.close()
        print(data[0])
        flag = False
        for tup in data:
            if tup[1] == user and tup[0] == passw:
                flag = True
        if(flag):
            return render_template('index.html')
        else:
            flash('Data invalid')
            return render_template('signin.html')


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
