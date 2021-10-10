from flask import Flask
from flask import render_template,request,redirect,url_for,flash
from flaskext.mysql import MySQL

app= Flask(__name__)
app.secret_key="Develoteca"

""" ------------------------------------------------------------------------------------------------------------ """
""" CONFIGURACION DE DIRECCION DE CONEXION, USUARIO, CONTRASEÑA Y NOMBRE DE LA BASE DE DATOS"""
""" ------------------------------------------------------------------------------------------------------------ """

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='rodolfodb'
mysql.init_app(app)



""" ------------------------------------------------------------------------------------------------------------ """
""" FUNCION PARA ACCIONAR HTML "INDEX" CREADO EN CARPETA TEMPLATES """
""" ------------------------------------------------------------------------------------------------------------ """

@app.route('/index')
def index():
    
    """
    ------------------------------------------------------------------------------------------------------------
    PRUEBA PARA CONEXIÓN A BASE DE DATOS CON CONSULTA DE PRUEBA INCLUIDA
    ------------------------------------------------------------------------------------------------------------
    
    sql = "INSERT INTO `productos` (`id`, `referencia`, `marca`, `cantidadtotal`, `preciound`, `indiciva`, `cantiva`, `precioundiva`) VALUES ('DOVE-M-32', 'M-32', 'DOVE', '24', '5000', '0', '0', '0');"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    """

    sql = "SELECT * FROM `productos`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    """ 
    ----------------------------------------------------------------------------
    FRAGMENTO PARA SELECCIONAR TODOS LOS REGISTROS
    ----------------------------------------------------------------------------
    """
    productos=cursor.fetchall()

    conn.commit()
      
    return render_template('productos/index.html', productos=productos)

""" ------------------------------------------------------------------------------------------------------------ """
""" FUNCION PARA ACCIONAR HTML "LOGIN" CREADO EN CARPETA TEMPLATES """
""" ------------------------------------------------------------------------------------------------------------ """

@app.route('/')
def login():
    return render_template('productos/ejemplo.html')

""" ------------------------------------------------------------------------------------------------------------ """
""" FUNCION PARA VALIDAR INICIOS DE SESIÓN """
""" ------------------------------------------------------------------------------------------------------------ """

@app.route('/validation', methods=['POST'])
def validation():

    _usuario="rsuarez11"
    _contrasena="timberious15"
    _username=request.form['txtUsuario']
    _pssw=request.form['txtContraseña']

    
   
    if _pssw=="" or _pssw != _contrasena:
        flash('Usuario y/o contraseña incorrectos, intente nuevamente')
        return redirect(url_for('login'))
    elif _username=="" or _username != _usuario:
        flash('Usuario y/o contraseña incorrectos, intente nuevamente')
        return redirect(url_for('login'))
    elif _username=="" and _pssw=="":
        flash('Usuario y/o contraseña incorrectos, intente nuevamente')
        return redirect(url_for('login'))
    elif _username == _usuario and _pssw == _contrasena:
        return redirect(url_for('index'))
    
    
    

    return redirect('/')

""" ------------------------------------------------------------------------------------------------------------ """
""" FUNCION PARA ACCIONAR HTML "CREATE" CREADO EN CARPETA TEMPLATES """
""" ------------------------------------------------------------------------------------------------------------ """

@app.route('/create')
def create():
    
    return render_template('productos/create.html')

""" ------------------------------------------------------------------------------------------------------------ """
""" FUNCION PARA ACCIONAR EL 'STORE' DENTRO DEL HTML "CREATE" CREADO EN CARPETA TEMPLATES """
""" ------------------------------------------------------------------------------------------------------------ """

@app.route('/store', methods=['POST'])
def storage():
    
    _referencia=request.form['txtReferencia']
    _marca=request.form['txtMarca']
    _cantTotal=request.form['txtCantidadTotal']
    _precioUnd=request.form['txtPrecioUnd']
    _indicIVA=request.form['txtIndicIVA']
    _cantIVA=request.form['txtCantIVA']
    _precioIVA=request.form['txtPrecioIVA']
    _id=_marca + "-" + _referencia

    if _referencia=="" or _marca=="" or _cantTotal=="" or _precioUnd=="" or _indicIVA=="" or _cantIVA=="" or _precioIVA=="":
        flash('Recuerda llenar los datos de los campos "Referencia", "marca", "cantidad total", "precio unitario", "indicador de IVA", "Unidades Disp. con IVA" y "precio con IVA"')
        return redirect(url_for('create'))
   
    sql = "INSERT INTO `productos` (`id`, `referencia`, `marca`, `cantidadtotal`, `preciound`, `indiciva`, `cantiva`, `precioundiva`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    datos=(_id,_referencia,_marca,_cantTotal,_precioUnd,_indicIVA,_cantIVA,_precioIVA)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('index')

@app.route('/destroy/<id>')
def destroy(id):
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s",(id))
    conn.commit()

    return redirect('/index')

@app.route('/edit/<id>')
def edit(id):
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id=%s",(id))
    productos=cursor.fetchall()
    conn.commit()

    return render_template('productos/edit.html',productos=productos)

@app.route('/update', methods=['POST'])
def update():

    _referencia=request.form['txtReferencia']
    _marca=request.form['txtMarca']
    _cantTotal=request.form['txtCantidadTotal']
    _precioUnd=request.form['txtPrecioUnd']
    _indicIVA=request.form['txtIndicIVA']
    _cantIVA=request.form['txtCantIVA']
    _precioIVA=request.form['txtPrecioIVA']
    _id=_marca + "-" + _referencia

    sql = "UPDATE productos SET referencia=%s, marca=%s, cantidadtotal=%s, preciound=%s, indiciva=%s, cantiva=%s, precioundiva=%s WHERE id=%s;"
    datos=(_referencia,_marca,_cantTotal,_precioUnd,_indicIVA,_cantIVA,_precioIVA,_id)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    """_nuevoID=_marca + "-" + _referencia

    sql = "UPDATE `productos` SET id=%s WHERE id=%s;"
    datos=(_nuevoID,_id)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()"""

    return redirect('/index')

""" PRUEBA DE CARGUE A GITHUB CON SABIDURIA CREO"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)