from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, jsonify, g, jsonify, Response,json
import requests
app = Flask(__name__)


@app.route ('/')
def index ():
    return render_template('index.html')

@app.route ('/listar_no_habilitados',methods=['POST'])
def listar_no_habilitados ():
    if request.method=='POST':
        vendor=request.form['vendor']
        print(vendor)
        return render_template('nohabilitados.html')



if __name__ == "__main__":
    app.run(host='127.0.0.1',port='5000',debug=True)