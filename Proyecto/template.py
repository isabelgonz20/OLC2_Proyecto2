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
from datetime import date
import seaborn as sns
from sklearn.linear_model import LinearRegression  
from sklearn.preprocessing import PolynomialFeatures 

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

@app.route("/rep1")
def Reporte1():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    if ejex==None or ejey==None:
        return "no se selecciono ningun eje"
    if seleccion_rep1==None:
        return "no se ingreso ningun pais"
    if pais==None:
        return "No se selecciono ninguna etiqueta para el pais"
    
    df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    x=np.asarray(df[df[pais]==seleccion_rep1]['date_ordinal']).reshape(-1,1)
    y=df[df[pais]==seleccion_rep1][ejey]

    plt.scatter(x,y)

    # regression transform
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # fit the model
    model = LinearRegression().fit(x_transform, y)
    y_new = model.predict(x_transform)

    # calculate rmse and r2
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)
    #print('RMSE: ', rmse)
    #print('R2: ', r2)


    # prediction
    x_new_min = 0.0
    x_new_max = 50.0

    x_new = np.linspace(x_new_min, x_new_max, 50)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plt.title("Tendencia de la infección por Covid-19 en un País\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    #
    

    plt.savefig("static/Reportes/rep1.png")

    plt.close()
    return render_template("analisis1.html", Encabezados = recorrertitulosExcel())







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

