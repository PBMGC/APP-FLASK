from flask import Flask,render_template,request,url_for,redirect,flash
from flask_mysqldb import MySQL

app=Flask(__name__)

#aqui se le configura toda la conexion a mysql
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="123"
app.config["MYSQL_DB"]="flaskcontacts"

#trabajar con mysql por medio de xampm
#asi iniciar conexion mysql
mysql=MySQL(app)

#la session del servidor siempre necesita una key
#por esta vez se guardar en memoria de app
app.secret_key='123'

@app.route('/')
def index():
    #consulta a la db
    cur=mysql.connection.cursor()
    cur.execute("SELECT * from contacts")
    #por medio del fecthall se reciebira toda la data que le pide
    data=cur.fetchall()
    return render_template("index.html",datos=data)

@app.route("/add_contact",methods=['POST'])
def add_contact():
    #guardara datos del formulario si se envian por
    #metodo post
    if request.method=="POST":
        #va a a solicitar del form 
        Nombre=request.form['nombre']
        Telefono=request.form['telefono']
        Email=request.form['email']

        cur=mysql.connection.cursor()
        cur.execute("SELECT * from contacts where telefono={0}".format(Telefono))
        data=cur.fetchall()

        if data:
            flash("Registro Existente")
            return redirect(url_for("index"))
        else:

            #por medio del cursor obtendras la ubicacion donde esta mysql
            cursor=mysql.connection.cursor()
            #cursor permitira ejecutar los comandos mysql
            #por medio de %s le indico que le pasare valores , en este caso por medio de una tupla
            cursor.execute('insert into contacts (Nombre,telefono,email) values (%s,%s,%s)',(Nombre,Telefono,Email))
            mysql.connection.commit()

            #mensaje flash
            flash("Registro Exitoso")
            #redirect redireccion url indica donde
            return redirect(url_for("index"))

#no es necesario indicar el tipo de dato en el app route
@app.route("/editar/<id>")
def editar(id):
    cursor=mysql.connection.cursor()
    cursor.execute('select * from contacts where idcontacts=%s',(id))
    dato=cursor.fetchall()
    #solo le pasara la tupla 0
    return render_template("editar.html",dato=dato[0])

#le indico que trabajara con un parametro 
@app.route("/eliminar/<string:id>")
def eliminar(id):
    cursor=mysql.connection.cursor()
    #por medio del format le indico que el primer valor del format que es id
    #es el que reemplazara al 0 
    cursor.execute('delete from contacts where idcontacts={0}'.format(id))
    mysql.connection.commit()
    flash("Registro Eliminado")
    return redirect(url_for("index"))

@app.route("/actualizar/<string:id>",methods=['POST'])
def actualizar(id):
    if request.method=='POST':
        Nombre=request.form['nombre']
        Telefono=request.form['telefono']
        Email=request.form['email']

        cursor=mysql.connection.cursor()
        cursor.execute(""" 
            update contacts
            set Nombre=%s,
                telefono=%s,
                email=%s
            where idcontacts = %s
        """,(Nombre,Telefono,Email,id))
        mysql.connection.commit()
        flash("actualizacion exitosa")
        return redirect(url_for("index"))


if __name__ == '__main__':

    app.run(debug=True)