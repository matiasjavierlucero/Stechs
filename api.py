from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, jsonify, g, jsonify, Response,json
from flaskext.mysql import MySQL
import os


app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'stechs'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql = MySQL()
mysql.init_app(app)
cur = mysql.connect().cursor()

#Al revisar el JSON note que existen registros repetidos, por lo que purgue el JSON
#pasandolo a lista y quitando de la misma los repetidos

modems_habilitados=[]
vendor_habilitados=[]

def array_modelos():
    with open('nuevojson.json') as file:
        data = json.load(file)
        for models  in data['models']:
            if models not in modems_habilitados:
                modems_habilitados.append(models)

def array_vendor():
    with open('nuevojson.json') as file:
        data = json.load(file)
        for models  in data['models']:
            if models['vendor'] not in vendor_habilitados:
                vendor_habilitados.append(models['vendor'])

array_modelos()
array_vendor()
            

@app.route('/search_enable', methods=['POST'])
def search():
    array_modelos()
    array_vendor()
    vendor=str(request.form['vendor'])
    #ARMO MI LISTA DE MODELOS HABILITADOS DADO EL VENDOR
    modelos_del_vendor=[]
    for modelos in modems_habilitados:
        print(modelos)
        if modelos['vendor']==vendor:
            modelos_del_vendor.append({'name':modelos['name'],'version':modelos['soft']})
        else:
            print("Entro aca")
            for tag in modelos['tags']:
                if tag==vendor:
                    vendor=modelos['vendor']
                    modelos_del_vendor.append({'name':modelos['name'],'version':modelos['soft']})
                else:
                    pass

    #BUSCO TODOS LOS REGISTROS EN LA TABLA QUE EXISTEN BAJO EL MISMO VENDOR
    cur.execute(f"SELECT modem_macaddr,ipaddr,vsi_model,version FROM docsis_update WHERE vsi_vendor like '{vendor}%'")
    resultado=cur.fetchall()

    #COMPARO EL RESULTADO CON MI LISTA DE MODEMS DEL VENDOR PARA SOLO TOMAR LOS QUE NO EXISTEN EN EL JSON
    nohabilidatos=[]
    for result in resultado:
        item={'name':result[2],'version':result[3]}
        if item not in modelos_del_vendor:       
            nohabilidatos.append(result)

    return jsonify({'Modelos no habilitados':nohabilidatos,'Vendor':vendor})

@app.route('/search_vendor', methods=['GET'])
def get_vendor():
    array_modelos()
    array_vendor()
    fabricantes=vendor_habilitados
    return jsonify({'Fabricantes':fabricantes})

@app.route('/newtag', methods=['POST'])
def newtag():
    vendortag=str(request.form['vendortag'])
    tag=str(request.form['tag'])
    with open('nuevojson.json', 'r') as f:
        json_data = json.load(f)
        for models in json_data['models']:
            if models['vendor']==vendortag:
                models['tags'].append(tag)

    with open('nuevojson.json', 'w') as f:
        f.write(json.dumps(json_data))
    array_modelos()
    array_vendor()
    return jsonify({'Ok':'Ok'}),200

@app.route('/modem_enable',methods=['POST'])
def modem_enable():
    array_modelos()
    array_vendor()
    macaddress=str(request.form['macaddress'])
    cur.execute("SELECT vsi_vendor,vsi_model,version FROM docsis_update WHERE modem_macaddr=%s",(macaddress))
    modem=cur.fetchall()
   
    return jsonify ({'Modem':modem}),200

@app.route('/enable_confirm',methods=['POST'])
def enable_confirm():
    modelo=request.form['modelo']
    version=request.form['version']
    fabricante=request.form['fabricante']
    tags=request.form['tags']
    tags=tags.split(',')
    
    
    #Esto almacena el modelo
    with open('nuevojson.json', 'r') as f:
        json_data = json.load(f)
        nuevomodelo={
        "vendor":fabricante,
        "name":modelo,
        "soft":version,
        "tags":[]
        }
        if nuevomodelo not in json_data['models']:
            for model in json_data['models']:
                if model['vendor']==fabricante:
                    if model['tags'] not in nuevomodelo['tags']:
                        nuevomodelo['tags']=model['tags']
            json_data['models'].append(nuevomodelo)

    with open('nuevojson.json', 'w') as f:
        f.write(json.dumps(json_data))

    #Ahora debo agregar los tag a cada uno de los modelos del vendor
    with open('nuevojson.json', 'r') as f:
        json_data = json.load(f)
        for model in json_data['models']:
            if model['vendor']==fabricante:
                for tag in tags:
                    model['tags'].append(tag)

    with open('nuevojson.json', 'w') as f:
        f.write(json.dumps(json_data))

    array_modelos()
    array_vendor()
    return jsonify({'Ok':'Ok'}),200

@app.route('/list_vendor',methods=['GET'])
def list_vendor():
    cur.execute("Select vsi_vendor FROM docsis_update GROUP BY vsi_vendor")
    listado=cur.fetchall()
    return jsonify({'Listado':listado})

app.run(host='127.0.0.1',port='4500',debug=True)