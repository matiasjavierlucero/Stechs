from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,Response,json
import requests
app = Flask(__name__)
app.secret_key = 'FlaskLaUtilizaParaRetornarMensajesFlash'

@app.route ('/')
def index ():
    resp = requests.get('http://localhost:4500/list_vendor')
    listadofabricantes=resp.json()['Listado']
    return render_template('index.html',Listado=listadofabricantes)

@app.route ('/listar_no_habilitados',methods=['POST'])
def listar_no_habilitados ():
    if request.method=='POST':
        vendor=request.form['vendor']
        data = {'vendor':vendor}
        resp = requests.post('http://localhost:4500/search_enable', data=data)
        Modelos=resp.json()['Modelos no habilitados']
        Vendor=resp.json()['Vendor']
        if len(Modelos)<1:
            flash('No se ha encontrado ningun resultado para su busqueda','danger')
            resp = requests.get('http://localhost:4500/search_vendor')
            Frabricantes=resp.json()['Fabricantes']
            return render_template('agregartags.html',vendor=Vendor,Fabricantes=Frabricantes)
        else:
    
            return render_template('nohabilitados.html',listado=Modelos,vendor=Vendor)

@app.route('/guardartag',methods=['POST'])
def Guardartag():
    if request.method=='POST':
        tag=request.form['nuevotag']
        vendortag=request.form['tagvendor']
        data = {'vendortag':vendortag,'tag':tag}
        resp = requests.post('http://localhost:4500/newtag', data=data)
        resp=resp.status_code
        flash(f"Se guardo un nuevo Tag ({tag}) para {vendortag}","success")
        return render_template('index.html')

@app.route('/habilitarmodem/<macaddress>')
def habilitarmodem(macaddress):
    data = {'macaddress':macaddress}
    resp = requests.post('http://localhost:4500/modem_enable', data=data)
    status=resp.status_code
    if status==200:
        Modem=resp.json()['Modem']
        resp = requests.get('http://localhost:4500/search_vendor')
        Frabricantes=resp.json()['Fabricantes']
        flash("Modem habilitado","success")
        return render_template('habilitarmodem.html',Modem=Modem,Fabricantes=Frabricantes)

@app.route('/guardarmodems',methods=['POST'])
def guardarmodem():
    print("ENTRA")
    modelo=request.form['Modelo']
    version=request.form['Version']
    fabricante=request.form['Fabricante']
    tags=str(request.form['Tags'])
    data = {
        "modelo":modelo,
        "version":version,
        "fabricante":fabricante,
        "tags":tags
        }
    resp = requests.post('http://localhost:4500/enable_confirm', data=data)
    status=resp.status_code
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1',port='5000',debug=True)