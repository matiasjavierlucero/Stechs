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
with open('nuevojson.json') as file:
    data = json.load(file)
    for models  in data['models']:
        if models not in modems_habilitados:
            modems_habilitados.append(models)
            
@app.route('/search_available', methods=['POST'])
def search():
        vendor=str(request.form['vendor'])
        #ARMO MI LISTA DE MODELOS HABILITADOS DADO EL VENDOR
        modelos_del_vendor=[]
        for modelos in modems_habilitados:
            if modelos['vendor']==vendor:
                modelos_del_vendor.append({'name':modelos['name'],'version':modelos['soft']})
            else:
                for tag in modelos['tags']:
                    if tag==vendor:
                        vendor=modelos['vendor']
                        modelos_del_vendor.append({'name':modelos['name'],'version':modelos['soft']})
        print("Modelos del vendor",modelos_del_vendor)
        #BUSCO TODOS LOS REGISTROS EN LA TABLA QUE EXISTEN BAJO EL MISMO VENDOR
        cur.execute(f"SELECT modem_macaddr,ipaddr,vsi_model,version FROM docsis_update WHERE vsi_vendor like '{vendor}%'")
        resultado=cur.fetchall()

        #COMPARO EL RESULTADO CON MI LISTA DE MODEMS DEL VENDOR PARA SOLO TOMAR LOS QUE NO EXISTEN EN EL JSON
        nohabilidatos=[]
        for result in resultado:
            for modelos in modelos_del_vendor:
                if result[2]!=modelos['name'] and result[3]!=modelos['version']: #Comparo vsi_model
                    if result not in nohabilidatos:
                        nohabilidatos.append(result)
        
        return jsonify({'Modelos no habilitados':nohabilidatos,'Vendor':vendor})

@app.route('/search_vendor', methods=['GET'])
def get_vendor():
    cur.execute("SELECT vsi_vendor FROM docsis_update WHERE vsi_vendor!='' GROUP BY vsi_vendor")
    fabricantes=cur.fetchall()
    return jsonify({'Fabricantes':fabricantes})

app.run(host='127.0.0.1',port='4500',debug=True)