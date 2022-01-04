#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os
from re import X
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
from datetime import date, datetime
import seaborn as sns
from sklearn.linear_model import LinearRegression  
from sklearn.preprocessing import PolynomialFeatures 
from sklearn import preprocessing

nombre_archivito = ""


app = Flask(__name__, template_folder='Templates')
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
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])
    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})



    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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

    plt.savefig("static/Reportes/rep1.png")

    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis1.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado1/<descripcion>")
def Mandarmensaje1(descripcion):
    return render_template('IEEErep1.html', descripcion = descripcion)

#______________________________________________Reporte 2______________________________________________________
#----------------------------------Predicción de Infertados en un País-----------------------------------------
@app.route('/iniciorep2')
def pagina4():
    return render_template('iniciorep2.html')

@app.route('/iniciorep2/regresionlineal2')
def pagina5():
    return render_template('analisis2.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep2/regresionlineal2/reporte2')
def pagina6():
    return render_template('IEEErep2.html')

@app.route("/rep2")
def Reporte2():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    predi=request.args.get('predi',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)
    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%Y%m%d"))
    #print("estoy en fechita")
    #print(fechita)

    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())


    #predi = datetime.date(str(predi)).toordinal()
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    x_new_max = fecha_reci #175

    x_new = np.linspace(x_new_min, x_new_max, fecha_reci)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    #
    pred = y_new[np.size(y_new)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Prediccion = {}'.format(poly_degree, round(rmse,2), round(r2,2), round(pred,2))
    plt.title("Predicción de Infectados en un País\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep2.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
    #descripcion = "esta es la descripcicon del rep 2"
    return render_template("analisis2.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado/<descripcion>")
def Mandarmensaje(descripcion):
    return render_template('IEEErep2.html', descripcion = descripcion)


#______________________________________________Reporte 3______________________________________________________
#----------------------------------Indice de Progresión de la pandemia-----------------------------------------
@app.route('/iniciorep3')
def pagina7():
    return render_template('iniciorep3.html')

@app.route('/iniciorep3/regresionlineal3')
def pagina8():
    return render_template('analisis3.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep3/regresionlineal3/reporte3')
def pagina9():
    return render_template('IEEErep3.html')

@app.route("/rep3")
def Reporte3():
    global nombre_archivito
    print("estoy antes de la 253")
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    print("antes de la 255")
    df=pd.DataFrame(contenido_archivo)
    df =df.dropna(subset=[ejey])
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])
    df3=df.groupby([ejex], as_index=False).agg({ejey: "sum"})
    print(ejey)
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    #fechita = int(fecha_dt.strftime("%d%m%Y"))
    #print(fechita)
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    

    #predi = datetime.date(str(predi)).toordinal()
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

    print(y)

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
    x_new_max = 50 #175

    x_new = np.linspace(x_new_min, x_new_max, 50)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    #
    pred = y_new[np.size(y_new)-1]
    pend = model.coef_[np.size(model.coef_)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Pendiente = {}'.format(poly_degree, round(rmse,2), round(r2,2), pend)
    plt.title("Indice de Progresión de la pandemia\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep3.png")
    #print("estoy en la pendiente")
    #print(pend)
    #print(y_new[np.size(y_new)-1])
    plt.close()
    descripcion = ""

    if(pend > 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion positivo de " + str(pend)
    elif(pend <= 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion negativo de " + str(pend)
        
    #descripcion = "esta es la descripcicon del rep 2"
    return render_template("analisis3.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado3/<descripcion>")
def Mandarmensaje3(descripcion):
    return render_template('IEEErep3.html', descripcion = descripcion)

#______________________________________________Reporte 4______________________________________________________
#--------------------------Predicción de mortalidad por COVID en un Departamento------------------------------
@app.route('/iniciorep4')
def pagina10():
    return render_template('iniciorep4.html')

@app.route('/iniciorep4/regresionlineal4')
def pagina11():
    return render_template('analisis4.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep4/regresionlineal4/reporte4')
def pagina12():
    return render_template('IEEErep4.html')

@app.route("/rep4")
def Reporte4():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    predi=request.args.get('predi',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])
    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%d%m%Y"))
    #print(fechita)

    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    #predi = datetime.date(str(predi)).toordinal()
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    x_new_max = fecha_reci #175

    x_new = np.linspace(x_new_min, x_new_max, fecha_reci)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    #
    pred = y_new[np.size(y_new)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Prediccion = {}'.format(poly_degree, round(rmse,2), round(r2,2), round(pred,2))
    plt.title("Predicción de mortalidad por COVID en un Departamento.\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Mortalidad')

    plt.savefig("static/Reportes/rep4.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
    #descripcion = "esta es la descripcicon del rep 2"
    return render_template("analisis4.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado4/<descripcion>")
def Mandarmensaje4(descripcion):
    return render_template('IEEErep4.html', descripcion = descripcion)

#______________________________________________Reporte 5______________________________________________________
#--------------------------------Predicción de mortalidad por COVID en un País---------------------------------
@app.route('/iniciorep5')
def pagina13():
    return render_template('iniciorep5.html')

@app.route('/iniciorep5/regresionlineal5')
def pagina14():
    return render_template('analisis5.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep5/regresionlineal5/reporte5')
def pagina15():
    return render_template('IEEErep5.html')

@app.route("/rep5")
def Reporte5():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    predi=request.args.get('predi',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])
    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%d%m%Y"))
    #print(fechita)
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    #predi = datetime.date(str(predi)).toordinal()
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    x_new_max = fecha_reci #175

    x_new = np.linspace(x_new_min, x_new_max, fecha_reci)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    #
    pred = y_new[np.size(y_new)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Prediccion = {}'.format(poly_degree, round(rmse,2), round(r2,2), round(pred,2))
    plt.title("Predicción de mortalidad por COVID en un País\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Mortaliad')

    plt.savefig("static/Reportes/rep5.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
    #descripcion = "esta es la descripcicon del rep 2"
    return render_template("analisis5.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado5/<descripcion>")
def Mandarmensaje5(descripcion):
    return render_template('IEEErep5.html', descripcion = descripcion)

#______________________________________________Reporte 6______________________________________________________
#---------------------------Análisis del número de muertes por coronavirus en un País-------------------------
@app.route('/iniciorep6')
def pagina16():
    return render_template('iniciorep6.html')

@app.route('/iniciorep6/regresionlineal6')
def pagina17():
    return render_template('analisis6.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep6/regresionlineal6/reporte6')
def pagina18():
    return render_template('IEEErep6.html')

@app.route("/rep6")
def Reporte6():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    #predi=request.args.get('predi',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])
    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    #fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    #fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%d%m%Y"))
    #print(fechita)
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    #predi = datetime.date(str(predi)).toordinal()
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    x_new_max = 50 #175

    x_new = np.linspace(x_new_min, x_new_max, 50)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    #
    pred = y_new[np.size(y_new)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plt.title("Análisis del número de muertes por coronavirus en un País\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Muertes')

    plt.savefig("static/Reportes/rep6.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1."
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1."
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1."
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1."
    
    
    #descripcion = "esta es la descripcicon del rep 2"
    return render_template("analisis6.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado6/<descripcion>")
def Mandarmensaje6(descripcion):
    return render_template('IEEErep6.html', descripcion = descripcion)

#______________________________________________Reporte 7______________________________________________________
#--------------------------Tendencia del número de infectados por día de un País-------------------------------
@app.route('/iniciorep7')
def pagina19():
    return render_template('iniciorep7.html')

@app.route('/iniciorep7/regresionlineal7')
def pagina20():
    return render_template('analisis7.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep7/regresionlineal7/reporte7')
def pagina21():
    return render_template('IEEErep7.html')

@app.route("/rep7")
def Reporte7():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])
    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})

    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    plt.title("Tendencia del número de infectados por día de un País\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep7.png")

    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis7.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado7/<descripcion>")
def Mandarmensaje7(descripcion):
    return render_template('IEEErep7.html', descripcion = descripcion)


#______________________________________________Reporte 9______________________________________________________
#----------------------------------Tendencia de la vacunación de en un País-----------------------------------
@app.route('/iniciorep9')
def pagina25():
    return render_template('iniciorep9.html')

@app.route('/iniciorep9/regresionlineal9')
def pagina26():
    return render_template('analisis9.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep9/regresionlineal9/reporte9')
def pagina27():
    return render_template('IEEErep9.html')

@app.route("/rep9")
def Reporte9():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    plt.title("Tendencia de la vacunacion de en un Pais\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep9.png")

    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis9.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado9/<descripcion>")
def Mandarmensaje9(descripcion):
    return render_template('IEEErep9.html', descripcion = descripcion)

#______________________________________________Reporte 10______________________________________________________
#-------------------------------Ánalisis Comparativo de Vacunación entre 2 paises.----------------------------
@app.route('/iniciorep10')
def pagina28():
    return render_template('iniciorep10.html')

@app.route('/iniciorep10/regresionlineal10')
def pagina29():
    return render_template('analisis10.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep10/regresionlineal10/reporte10')
def pagina30():
    return render_template('IEEErep10.html')

@app.route("/rep10")
def Reporte10():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]
    
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
    plt.title("Ánalisis Comparativo de Vacunaciópn entre 2 paises para " + seleccion_rep1 + "\n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep10.png")

    plt.close()

    seleccion_rep2=request.args.get('seleccion_rep2',None)
    #print("Estoy en seleccion")
    #print(seleccion_rep2)
    #df=pd.DataFrame(contenido_archivo)
    
    df3=df[df[pais]==seleccion_rep2].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    plt.title("Ánalisis Comparativo de Vacunaciópn entre 2 paises " + seleccion_rep2 + "\n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep101.png")

    plt.close()

    descripcion = ""
    descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " " + seleccion_rep2 +" se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media, por lo cual nos podemos dar cuenta que los indices de vacunacion van subiendo ya que las personas estan tomando conciencia que se deben de vacunar, aunque aun falta bastante genente a la cual llegar con la vacuna"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis10.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado10/<descripcion>")
def Mandarmensaje10(descripcion):
    return render_template('IEEErep10.html', descripcion = descripcion)

#______________________________________________Reporte 11______________________________________________________
#---------------Porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo----------------																									------
@app.route('/iniciorep11')
def pagina61():
    return render_template('iniciorep11.html')

@app.route('/iniciorep11/regresionlineal11')
def pagina62():
    return render_template('analisis11.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep11/regresionlineal11/reporte11')
def pagina63():
    return render_template('IEEErep11.html')

@app.route("/rep11")
def Reporte11():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    x=np.asarray(df[df[pais]==seleccion_rep1][ejex]).reshape(-1,1)
    y=df[df[pais]==seleccion_rep1][ejey]

    plt.scatter(x,y)

    tamano_x = 0
    tamano_y = 0
    porcentaje = 0.0

    #print("esta es la suma de x")
    tamano_x = np.sum(x)
    #print(tamano_x)

    #print("esta es la suma de y")
    tamano_y = np.sum(y)
    #print(tamano_y)

    porcentaje = (tamano_y * 100)/tamano_x

    #print("El porcentajes es de: ")
    #print(porcentaje)

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

    pend = model.coef_[np.size(model.coef_)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Porcentaje = {}%'.format(poly_degree, round(rmse,2), round(r2,2), round(porcentaje,2))
    plt.title("Porcentaje de hombres infectados por covid-19 en un Pais desde el primer caso activo\n " + title, fontsize=10)
    plt.xlabel('Infectados')
    plt.ylabel('Hombres')

    plt.savefig("static/Reportes/rep11.png")

    plt.close()
    descripcion = ""

    if(pend > 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "por lo cual el porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo " + str(round(porcentaje,2))
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "por lo cual el porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo" + str(round(porcentaje,2))
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "por lo cual el porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo" + str(round(porcentaje,2))
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion positivo de " + str(pend) + "por lo cual el porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo " + str(round(porcentaje,2))
    elif(pend <= 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "por lo cual el porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo" + str(round(porcentaje,2))
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "por lo cual el porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo " + str(round(porcentaje,2))
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "por lo cual el porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo  " + str(round(porcentaje,2))
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion negativo de " + str(pend) + "por lo cual el porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo " + str(round(porcentaje,2))
        
    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis11.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado11/<descripcion>")
def Mandarmensaje11(descripcion):
    return render_template('IEEErep11.html', descripcion = descripcion)

#______________________________________________Reporte 12______________________________________________________
#--------------------------Ánalisis Comparativo entres 2 o más paises o continentes.--------------------------
@app.route('/iniciorep12')
def pagina70():
    return render_template('iniciorep12.html')

@app.route('/iniciorep12/regresionlineal12')
def pagina71():
    return render_template('analisis12.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep12/regresionlineal12/reporte12')
def pagina72():
    return render_template('IEEErep12.html')

@app.route("/rep12")
def Reporte12():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]
    
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
    plt.title("Ánalisis Comparativo de Vacunaciópn entre 2 o mas paises para " + seleccion_rep1 + "\n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep12.png")

    plt.close()

    seleccion_rep2=request.args.get('seleccion_rep2',None)
    #print("Estoy en seleccion")
    #print(seleccion_rep2)
    #df=pd.DataFrame(contenido_archivo)
    
    df3=df[df[pais]==seleccion_rep2].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    plt.title("Ánalisis Comparativo de Vacunaciópn entre 2 o mas paises " + seleccion_rep2 + "\n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep121.png")

   #plt.close()
    plt.close()

    seleccion_rep3=request.args.get('seleccion_rep3',None)
    #print("Estoy en seleccion")
    #print(seleccion_rep2)
    #df=pd.DataFrame(contenido_archivo)
    
    df3=df[df[pais]==seleccion_rep3].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    plt.title("Ánalisis Comparativo de Vacunaciópn entre 2 o mas paises " + seleccion_rep3 + "\n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep122.png")

    plt.close()


    descripcion = ""
    descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " " + seleccion_rep2 +" se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media, por lo cual nos podemos dar cuenta que los indices de vacunacion van subiendo ya que las personas estan tomando conciencia que se deben de vacunar, aunque aun falta bastante genente a la cual llegar con la vacuna"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis12.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado12/<descripcion>")
def Mandarmensaje12(descripcion):
    return render_template('IEEErep12.html', descripcion = descripcion)



#______________________________________________Reporte 13______________________________________________________
#----------------------Muertes promedio por casos confirmados y edad de covid 19 en un País--------------------																									------
@app.route('/iniciorep13')
def pagina64():
    return render_template('iniciorep13.html')

@app.route('/iniciorep13/regresionlineal13')
def pagina65():
    return render_template('analisis13.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep13/regresionlineal13/reporte13')
def pagina66():
    return render_template('IEEErep13.html')

@app.route("/rep13")
def Reporte13():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    edad=request.args.get('edad',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    seleccion_rep2=request.args.get('seleccion_rep2',None)
    
    df  = pd.DataFrame(contenido_archivo)
    df2 = df[df[pais]==int(seleccion_rep1)]
    df2 = df2.dropna(subset=[ejex])
    df2 = df2.dropna(subset=[ejey])

    df3=df2.groupby([ejex], as_index=False).agg({ejey: "sum"})
    
    
    x=np.asarray(df3[ejex]).reshape(-1,1)
    y=df3[ejey]

    plt.scatter(x,y)

    tamano_x = 0
    tamano_y = 0
    porcentaje = 0.0

    #print("este es el tamanio de x")
    tamano_x = np.size(x)
    #print(tamano_x)
    #print(x)
    #print("esta es la suma de x")
    tamano_y = np.sum(x)
    #print(tamano_y)

    porcentaje = tamano_y/tamano_x

    #print("El porcentajes es de: ")
    #print(porcentaje)

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

    pend = model.coef_[np.size(model.coef_)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Promedio = {}'.format(poly_degree, round(rmse,2), round(r2,2), round(porcentaje,2))
    plt.title("Muertes promedio por casos confirmados y edad de covid 19 en un Pais.\n " + title, fontsize=10)
    plt.xlabel('Muertes')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep13.png")

    plt.close()
    descripcion = ""

    if(pend > 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "Por lo cual se tiene un promedio de muertes por casos confirmados y edad de covid 19 en un País que es de " + str(round(porcentaje,2))
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "Por lo cual se tiene un promedio de muertes por casos confirmados y edad de covid 19 en un País que es de " + str(round(porcentaje,2))
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "Por lo cual se tiene un promedio de muertes por casos confirmados y edad de covid 19 en un País que es de " + str(round(porcentaje,2)) 
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion positivo de " + str(pend) + "Por lo cual se tiene un promedio de muertes por casos confirmados y edad de covid 19 en un País que es de" + str(round(porcentaje,2)) 
    elif(pend <= 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "Por lo cual se tiene un promedio de muertes por casos confirmados y edad de covid 19 en un País que es de " + str(round(porcentaje,2)) 
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "Por lo cual se tiene un promedio de muertes por casos confirmados y edad de covid 19 en un País que es de" + str(round(porcentaje,2)) 
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "Por lo cual se tiene un promedio de muertes por casos confirmados y edad de covid 19 en un País que es de " + str(round(porcentaje,2)) 
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion negativo de " + str(pend) + "Por lo cual se tiene un promedio de muertes por casos confirmados y edad de covid 19 en un País que es de " + str(round(porcentaje,2))
        
    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis13.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado13/<descripcion>")
def Mandarmensaje13(descripcion):
    return render_template('IEEErep13.html', descripcion = descripcion)


#______________________________________________Reporte 14______________________________________________________
#-------------------------------Muertes según regiones de un país - Covid 19.----------------------------------
@app.route('/iniciorep14')
def pagina31():
    return render_template('iniciorep14.html')

@app.route('/iniciorep14/regresionlineal14')
def pagina32():
    return render_template('analisis14.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep14/regresionlineal14/reporte14')
def pagina33():
    return render_template('IEEErep14.html')

@app.route("/rep14")
def Reporte14():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

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
    plt.title("Muertes según regiones de un país - Covid 19\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Muertes')

    plt.savefig("static/Reportes/rep14.png")

    plt.close()
    
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis14.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado14/<descripcion>")
def Mandarmensaje14(descripcion):
    return render_template('IEEErep14.html', descripcion = descripcion)


#______________________________________________Reporte 15______________________________________________________
#---------------Porcentaje de muertes frente al total de casos en un país, región o continente.----------------
@app.route('/iniciorep15')
def pagina34():
    return render_template('iniciorep15.html')

@app.route('/iniciorep15/regresionlineal15')
def pagina35():
    return render_template('analisis15.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep15/regresionlineal15/reporte15')
def pagina36():
    return render_template('IEEErep15.html')

@app.route("/rep15")
def Reporte15():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]


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
    plt.title("Tendencia de casos confirmados de Coronavirus en un departamento de un País.\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep15.png")

    plt.close()

    descripcion = ""
    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis15.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado15/<descripcion>")
def Mandarmensaje15(descripcion):
    return render_template('IEEErep15.html', descripcion = descripcion)

#______________________________________________Reporte 16______________________________________________________
#---------------Porcentaje de muertes frente al total de casos en un país, región o continente.----------------																									------
@app.route('/iniciorep16')
def pagina58():
    return render_template('iniciorep16.html')

@app.route('/iniciorep16/regresionlineal16')
def pagina59():
    return render_template('analisis16.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep16/regresionlineal16/reporte16')
def pagina60():
    return render_template('IEEErep16.html')

@app.route("/rep16")
def Reporte16():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})

    x=np.asarray(df3[ejex]).reshape(-1,1)
    y=df3[ejey]

    plt.scatter(x,y)

    tamano_x = 0
    tamano_y = 0
    porcentaje = 0.0

    #print("esta es la suma de x")
    tamano_x = np.sum(x)
    #print(tamano_x)

    #print("esta es la suma de y")
    tamano_y = np.sum(y)
    #print(tamano_y)

    porcentaje = (tamano_x * 100)/tamano_y

    #print("El porcentajes es de: ")
    #print(porcentaje)

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

    pend = model.coef_[np.size(model.coef_)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Porcentaje = {}%'.format(poly_degree, round(rmse,2), round(r2,2), round(porcentaje,2))
    plt.title("Porcentaje de muertes frente al total de casos en un pais, region o continente.\n " + title, fontsize=10)
    plt.xlabel('Muertes')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep16.png")

    plt.close()
    descripcion = ""

    if(pend > 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "Por lo cual se tiene un porcentaje de muertes frente al total de casos de " + str(round(porcentaje,2))
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "Por lo cual se tiene un porcentaje de muertes frente al total de casos de " + str(round(porcentaje,2))
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) + "Por lo cual se tiene un porcentaje de muertes frente al total de casos de " + str(round(porcentaje,2)) 
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion positivo de " + str(pend) + "Por lo cual se tiene un porcentaje de muertes frente al total de casos de " + str(round(porcentaje,2)) 
    elif(pend <= 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "Por lo cual se tiene un porcentaje de muertes frente al total de casos de " + str(round(porcentaje,2)) 
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "Por lo cual se tiene un porcentaje de muertes frente al total de casos de " + str(round(porcentaje,2)) 
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) + "Por lo cual se tiene un porcentaje de muertes frente al total de casos de " + str(round(porcentaje,2)) 
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion negativo de " + str(pend) + "Por lo cual se tiene un porcentaje de muertes frente al total de casos de " + str(round(porcentaje,2))
        
    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis16.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado16/<descripcion>")
def Mandarmensaje16(descripcion):
    return render_template('IEEErep16.html', descripcion = descripcion)

#______________________________________________Reporte 17______________________________________________________
#---------------Tasa de comportamiento de casos activos en relación al número de muertes en un continente------
@app.route('/iniciorep17')
def pagina37():
    return render_template('iniciorep17.html')

@app.route('/iniciorep17/regresionlineal17')
def pagina38():
    return render_template('analisis17.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep17/regresionlineal17/reporte17')
def pagina39():
    return render_template('IEEErep17.html')

@app.route("/rep17")
def Reporte17():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})

    x=np.asarray(df3[ejex]).reshape(-1,1)
    y=df3[ejey]

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

    pend = model.coef_[np.size(model.coef_)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Pendiente = {}'.format(poly_degree, round(rmse,2), round(r2,2), pend)
    plt.title("Tasa de comportamiento de casos activos en relación al número de muertes en un continente.\n " + title, fontsize=10)
    plt.xlabel('Muertes')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep17.png")

    plt.close()
    descripcion = ""

    if(pend > 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion positivo de " + str(pend)
    elif(pend <= 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion negativo de " + str(pend)
        
    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis17.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado17/<descripcion>")
def Mandarmensaje17(descripcion):
    return render_template('IEEErep17.html', descripcion = descripcion)


#______________________________________________Reporte 19______________________________________________________
#------------------Predicción de muertes en el último día del primer año de infecciones en un país.-------------
@app.route('/iniciorep19')
def pagina40():
    return render_template('iniciorep19.html')

@app.route('/iniciorep19/regresionlineal19')
def pagina41():
    return render_template('analisis19.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep19/regresionlineal19/reporte19')
def pagina42():
    return render_template('IEEErep19.html')

@app.route("/rep19")
def Reporte19():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    predi=request.args.get('predi',None)
    df=pd.DataFrame(contenido_archivo)
    
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%Y%m%d"))
    #print("estoy en fechita")
    #print(fechita)

    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]


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
    x_new_max = fecha_reci #175

    x_new = np.linspace(x_new_min, x_new_max, fecha_reci)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    #
    pred = y_new[np.size(y_new)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Prediccion = {}'.format(poly_degree, round(rmse,2), round(r2,2), round(pred,2))
    plt.title("Predicción de muertes en el último día del primer año de infecciones en un país.\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Muertes')

    plt.savefig("static/Reportes/rep19.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
    #descripcion = "esta es la descripcicon del rep 2"
    return render_template("analisis19.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado19/<descripcion>")
def Mandarmensaje19(descripcion):
    return render_template('IEEErep19.html', descripcion = descripcion)


#______________________________________________Reporte 20______________________________________________________
#-Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19---
@app.route('/iniciorep20')
def pagina43():
    return render_template('iniciorep20.html')

@app.route('/iniciorep20/regresionlineal20')
def pagina44():
    return render_template('analisis20.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep20/regresionlineal20/reporte20')
def pagina45():
    return render_template('IEEErep20.html')

@app.route("/rep20")
def Reporte20():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    #pais=request.args.get('pais',None)
    #seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df.groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

    
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
    plt.title("Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios \n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep20.png")

    plt.close()

    ejex=request.args.get('ejex',None)
    ejey2=request.args.get('ejey2',None)
    #print("Estoy en seleccion")
    #print(seleccion_rep2)
    df=pd.DataFrame(contenido_archivo)
    
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey2])

    df3=df.groupby([ejex], as_index=False).agg({ejey2: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey2]









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
    plt.title("Tasa de muerte por COVID-19 \n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Muerte')

    plt.savefig("static/Reportes/rep201.png")

    plt.close()


    descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media, por lo cual nos podemos dar cuenta que los indices de infeccion y mortalidad solo se van a lograr reducir si todos nos cuidamos y seguimos las medidas precautorias"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis20.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado20/<descripcion>")
def Mandarmensaje20(descripcion):
    return render_template('IEEErep20.html', descripcion = descripcion)

#______________________________________________Reporte 21______________________________________________________
#-------------------Predicciones de casos y muertes en todo el mundo - Neural Network MLPRegressor-------------
@app.route('/iniciorep21')
def pagina46():
    return render_template('iniciorep21.html')

@app.route('/iniciorep21/regresionlineal21')
def pagina47():
    return render_template('analisis21.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep21/regresionlineal21/reporte21')
def pagina48():
    return render_template('IEEErep21.html')

@app.route("/rep21")
def Reporte21():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    predi=request.args.get('predi',None)
    #pais=request.args.get('pais',None)
    #seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()

    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df.groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

    
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
    x_new_max = fecha_reci

    x_new = np.linspace(x_new_min, x_new_max, fecha_reci)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    pred = y_new[np.size(y_new)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Prediccion = {}'.format(poly_degree, round(rmse,2), round(r2,2), round(pred,2))
    plt.title("Predicciones de casos en todo el mundo \n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep21.png")

    plt.close()

    ejex=request.args.get('ejex',None)
    ejey2=request.args.get('ejey2',None)
    predi2=request.args.get('predi2',None)
    #print("Estoy en seleccion")
    #print(seleccion_rep2)
    df=pd.DataFrame(contenido_archivo)
    
    fecha_dt2 = datetime.strptime(predi2, '%d/%m/%Y')
    fecha_reci2 = fecha_dt2.toordinal()

    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey2])

    df3=df.groupby([ejex], as_index=False).agg({ejey2: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey2]


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
    x_new_max = fecha_reci2

    x_new = np.linspace(x_new_min, x_new_max, fecha_reci2)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    pred2 = y_new[np.size(y_new)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Prediccion = {}'.format(poly_degree, round(rmse,2), round(r2,2), round(pred2,2))
    plt.title("Predicciones muertes en todo el mundo \n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Muerte')

    plt.savefig("static/Reportes/rep211.png")

    plt.close()


    descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media, por lo cual nos podemos dar cuenta que los indices de infeccion y mortalidad solo se van a lograr reducir si todos nos cuidamos y seguimos las medidas precautorias, con lo anterior descrito se sabe que la prediccion de infectados es de: " + str(round(pred,2)) + "y la prediccion de muertes es de: " + str(round(pred2,2))
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis21.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado21/<descripcion>")
def Mandarmensaje21(descripcion):
    return render_template('IEEErep21.html', descripcion = descripcion)

#______________________________________________Reporte 22______________________________________________________
#--------------------------Tasa de mortalidad por coronavirus (COVID-19) en un país----------------------------
@app.route('/iniciorep22')
def pagina49():
    return render_template('iniciorep22.html')

@app.route('/iniciorep22/regresionlineal22')
def pagina50():
    return render_template('analisis22.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep22/regresionlineal22/reporte22')
def pagina51():
    return render_template('IEEErep22.html')

@app.route("/rep22")
def Reporte22():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]


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

    pend = model.coef_[np.size(model.coef_)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plt.title("Tasa de mortalidad por coronavirus (COVID-19) en un país.\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Mortalidad')

    plt.savefig("static/Reportes/rep22.png")

    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1" + "Con lo cual se tiene una tasa de mortalidad de: " + str(pend)
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1" + "Con lo cual se tiene una tasa de mortalidad de: " + str(pend)
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1" + "Con lo cual se tiene una tasa de mortalidad de: " + str(pend)
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1" + "Con lo cual se tiene una tasa de mortalidad de: " + str(pend)
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis22.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado22/<descripcion>")
def Mandarmensaje22(descripcion):
    return render_template('IEEErep22.html', descripcion = descripcion)

#______________________________________________Reporte 23______________________________________________________
#---------------------------------Factores de muerte por COVID-19 en un país.--------------------																									------
@app.route('/iniciorep23')
def pagina67():
    return render_template('iniciorep23.html')

@app.route('/iniciorep23/regresionlineal23')
def pagina68():
    return render_template('analisis23.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep23/regresionlineal23/reporte23')
def pagina69():
    return render_template('IEEErep23.html')

@app.route("/rep23")
def Reporte23():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    
    df  = pd.DataFrame(contenido_archivo)
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})

    x=np.asarray(df3[ejex]).reshape(-1,1)
    y=df3[ejey]

    #print("Probando que lleva outlook_encoded")
    #outlook_encoded=le.fit_transform(x)
    #outlook_encoded.array.reshape(-1, 1)
    #print(outlook_encoded)
    #nuevax = df3
    #print("Este es mi nueva x")
    #print(nuevax)
    #print("esta es una nueva x")
    #print("tIPO X")
    #print(type(y))

    plt.scatter(x,y)

    tamano_x = 0
    tamano_y = 0
    porcentaje = 0.0

    #print("este es el tamanio de x")
    #tamano_x = np.size(x)
    #print(tamano_x)
    #print(x)
    #print("esta es la suma de x")
    #tamano_y = np.sum(x)
    #print(tamano_y)

    #porcentaje = tamano_y/tamano_x

    #print("El porcentajes es de: ")
    #print(porcentaje)

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

    pend = model.coef_[np.size(model.coef_)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {};'.format(poly_degree, round(rmse,2), round(r2,2))
    plt.title("Factores de muerte por COVID-19 en un país.\n " + title, fontsize=10)
    plt.xlabel('Factores')
    plt.ylabel('Muertes')

    plt.savefig("static/Reportes/rep23.png")

    plt.close()
    descripcion = ""

    if(pend > 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) 
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) 
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend) 
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion positivo de " + str(pend) 
    elif(pend <= 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)  
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) 
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend) 
        elif(r2 >= 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion negativo de " + str(pend) 
        
    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis23.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado23/<descripcion>")
def Mandarmensaje23(descripcion):
    return render_template('IEEErep23.html', descripcion = descripcion)



#______________________________________________Reporte 24______________________________________________________
#--------------Comparación entre el número de casos detectados y el número de pruebas de un país.--------------
@app.route('/iniciorep24')
def pagina52():
    return render_template('iniciorep24.html')

@app.route('/iniciorep24/regresionlineal24')
def pagina53():
    return render_template('analisis24.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep24/regresionlineal24/reporte24')
def pagina54():
    return render_template('IEEErep24.html')

@app.route("/rep24")
def Reporte24():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    df=pd.DataFrame(contenido_archivo)
    
    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]

    
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
    plt.title("Casos detectados de un país. " + seleccion_rep1 + "\n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep24.png")

    plt.close()

    #seleccion_rep2=request.args.get('seleccion_rep2',None)
    ejey2=request.args.get('ejey2',None)
    df = df.dropna(subset=[ejey2])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey2: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey2]
    #print("Estoy en seleccion")
    #print(seleccion_rep2)
    #y=df[ejey2]
    

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
    plt.title("Número de pruebas de un país. " + seleccion_rep1 + "\n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Pruebas')

    plt.savefig("static/Reportes/rep241.png")

    plt.close()
    descripcion = ""

    descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media, por lo cual nos podemos dar cuenta que los indices de vacunacion van subiendo ya que las personas estan tomando conciencia que se deben de vacunar, aunque aun falta bastante genente a la cual llegar con la vacuna"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis24.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado24/<descripcion>")
def Mandarmensaje24(descripcion):
    return render_template('IEEErep24.html', descripcion = descripcion)


#______________________________________________Reporte 25______________________________________________________
#-----------------------------------Predicción de casos confirmados por día------------------------------------
@app.route('/iniciorep25')
def pagina55():
    return render_template('iniciorep25.html')

@app.route('/iniciorep25/regresionlineal25')
def pagina56():
    return render_template('analisis25.html', Encabezados = recorrertitulosExcel())

@app.route('/iniciorep25/regresionlineal25/reporte25')
def pagina57():
    return render_template('IEEErep25.html')

@app.route("/rep25")
def Reporte25():
    global nombre_archivito
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    pais=request.args.get('pais',None)
    seleccion_rep1=request.args.get('seleccion_rep1',None)
    predi=request.args.get('predi',None)
    df=pd.DataFrame(contenido_archivo)
    
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%Y%m%d"))
    #print("estoy en fechita")
    #print(fechita)

    df = df.dropna(subset=[ejex])
    df = df.dropna(subset=[ejey])

    df3=df[df[pais]==seleccion_rep1].groupby([ejex], as_index=False).agg({ejey: "sum"})
    try:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df3['date_ordinal'] = pd.to_datetime(df3[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    x=np.asarray(df3['date_ordinal']).reshape(-1,1)
    y=df3[ejey]


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
    x_new_max = fecha_reci #175

    x_new = np.linspace(x_new_min, x_new_max, fecha_reci)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    #
    pred = y_new[np.size(y_new)-1]
    # plot the prediction
    plt.plot(x, y, color='coral', linewidth=3)
    plt.grid()
    #plt.xlim(x_new_min,x_new_max)
    plt.ylim(np.min(y),np.max(y))
    title = 'Degree = {}; RMSE = {}; R2 = {}; Prediccion = {}'.format(poly_degree, round(rmse,2), round(r2,2), round(pred,2))
    plt.title("Predicción de casos confirmados por día\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep25.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    descripcion = ""

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadratico medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
    #descripcion = "esta es la descripcicon del rep 2"
    return render_template("analisis25.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado25/<descripcion>")
def Mandarmensaje25(descripcion):
    return render_template('IEEErep25.html', descripcion = descripcion)































































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
    app.run(debug= True, port= 8000, host='0.0.0.0')

########################################################################

