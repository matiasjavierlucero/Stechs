from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,Response,json
import requests
app = Flask(__name__)
app.secret_key = 'FlaskLaUtilizaParaRetornarMensajesFlash'

@app.route ('/')
def index ():
    return render_template('index.html')

@app.route ('/listar_no_habilitados',methods=['POST'])
def listar_no_habilitados ():
    if request.method=='POST':
        vendor=request.form['vendor']
        data = {'vendor':vendor}
        resp = requests.post('http://localhost:4500/search_available', data=data)
        Modelos=resp.json()['Modelos no habilitados']
        Vendor=resp.json()['Vendor']
        if len(Modelos)<1:
            flash('No se ha encontrado ningun resultado para su busqueda','danger')
            resp = requests.get('http://localhost:4500/search_vendor')
            Frabricantes=resp.json()['Fabricantes']
            return render_template('agregartags.html',vendor=Vendor,Fabricantes=Frabricantes)
        else:
    
            return render_template('nohabilitados.html',listado=Modelos,vendor=Vendor)



if __name__ == "__main__":
    app.run(host='127.0.0.1',port='5000',debug=True)