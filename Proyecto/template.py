import os
from flask import Flask
from flask import request
from flask import render_template
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from flask_wtf import FlaskForm 
from wtforms import SelectField


nombre_archivito = ""


app = Flask(__name__)
app. config['UPLOAD_FOLDER'] = "./Archivos"
@app.route('/')
def index():
    return render_template('index.html')


#______________________________________________Reporte 1______________________________________________________
#--------------------------Tendencia de la infección por Covid-19 en un País----------------------------------
@app.route('/iniciorep1')
def pagina():
    return render_template('iniciorep1.html')

@app.route('/iniciorep1/regresionlineal')
def pagina2():
    return render_template('analisis1.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep1/regresionlineal/reporte1')
def pagina3():
    return render_template('IEEErep1.html')










@app.route('/iniciorep2')
def pagina4():
    return render_template('iniciorep2.html')



    

@app.route("/", methods = ['POST'])
def uploader():
    if request.method == "POST":
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global nombre_archivito
        nombre_archivito = filename
        #recorrertitulosExcel(filename)
        #Refresionlineal_prediccion(filename)

        return render_template('index.html')

@app.route("/rep2")
def Refresionlineal_prediccion2():
    ejex = request.args.get("ejex", None)
    ejey = request.args.get("ejey", None)

    global nombre_archivito
    df = pd.read_csv("Archivos/" + nombre_archivito)

    #print(df)
    x = np.asanyarray(df[ejex]).reshape(-1,1)
    y = df[ejey]

    regr = linear_model.LinearRegression()
    regr.fit(x,y)
    y_pred = regr.predict(x)

    plt.scatter(x, y, color = 'black')
    plt.plot(x, y_pred, color = 'blue', linewidth=3)

    rmse = np.sqrt(mean_squared_error(y, y_pred))
    r2 = r2_score(y, y_pred)
    print('RMSE: ', rmse)
    print('R2: ', r2)

    plt.ylim(56000,68000)
    plt.savefig("static/Reportes/rep2.png")

    print(regr.predict([[50]])) 
    #return "Si lo hizo"
    return render_template('analisis1.html', Encabezados = recorrertitulosExcel())

def recorrertitulosExcel():
    global nombre_archivito
    df = pd.read_csv("Archivos/" + nombre_archivito)
    encabezados =[]
    for titulo in pd.DataFrame(df):
        encabezados.append(titulo)
    #print(encabezados)
    return encabezados

if __name__ == '__main__':
    app.run(debug= True, port= 8000)

########################################################################

