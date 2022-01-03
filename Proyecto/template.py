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
from datetime import date, datetime
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
    
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
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

    plt.savefig("static/Reportes/rep1.png")

    plt.close()

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.95):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
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
    
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%Y%m%d"))
    #print("estoy en fechita")
    #print(fechita)

    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())


    #predi = datetime.date(str(predi)).toordinal()
    
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
    
    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.95):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
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
    contenido_archivo = pd.read_csv("Archivos/" + nombre_archivito)
    ejex=request.args.get('ejex',None)
    ejey=request.args.get('ejey',None)
    df=pd.DataFrame(contenido_archivo)
    
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    #fechita = int(fecha_dt.strftime("%d%m%Y"))
    #print(fechita)
    try:
        df['date_ordinal'] = pd.to_datetime(df[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
    

    #predi = datetime.date(str(predi)).toordinal()
    
    x=np.asarray(df['date_ordinal']).reshape(-1,1)
    y=df[ejey]

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
    
    if(pend > 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 >= 0.95):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion positivo de " + str(pend)
    elif(pend < 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 >= 0.95):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion negativo de " + str(pend)
        





    
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
    
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%d%m%Y"))
    #print(fechita)

    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    #predi = datetime.date(str(predi)).toordinal()
    
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

    plt.savefig("static/Reportes/rep4.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    
    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
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
    
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%d%m%Y"))
    #print(fechita)
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    #predi = datetime.date(str(predi)).toordinal()
    
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

    plt.savefig("static/Reportes/rep5.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    
    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
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
    
    #diapredi = int(predi)
    ##print(diapredi)
    #diapredi2 = ord(diapredi)
    #print(diapredi2)

    #fecha_dt = datetime.strptime(predi, '%d/%m/%Y')
    #fecha_reci = fecha_dt.toordinal()
    #fechita = int(fecha_dt.strftime("%d%m%Y"))
    #print(fechita)
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    #predi = datetime.date(str(predi)).toordinal()
    
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
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep6.png")
    
    #print(y_new[np.size(y_new)-1])
    plt.close()
    
    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1."
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1."
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1."
    elif(r2 >= 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1."
    
    
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
    
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

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

    plt.savefig("static/Reportes/rep7.png")

    plt.close()

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.95):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
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
    
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
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

    plt.savefig("static/Reportes/rep9.png")

    plt.close()

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.95):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis9.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado9/<descripcion>")
def Mandarmensaje9(descripcion):
    return render_template('IEEErep9.html', descripcion = descripcion)

#______________________________________________Reporte 10______________________________________________________
#----------------------------------Tendencia de la vacunación de en un País-----------------------------------
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
    
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

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
    plt.title("Ánalisis Comparativo de Vacunaciópn entre 2 paises para " + seleccion_rep1 + "\n" + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep10.png")

    plt.close()

    seleccion_rep2=request.args.get('seleccion_rep2',None)
    print("Estoy en seleccion")
    print(seleccion_rep2)
    df=pd.DataFrame(contenido_archivo)
    
    df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep2][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    x=np.asarray(df[df[pais]==seleccion_rep2]['date_ordinal']).reshape(-1,1)
    y=df[df[pais]==seleccion_rep2][ejey]
    

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


    descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " " + seleccion_rep2 +" se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media, por lo cual nos podemos dar cuenta que los indices de vacunacion van subiendo ya que las personas estan tomando conciencia que se deben de vacunar, aunque aun falta bastante genente a la cual llegar con la vacuna"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis10.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado10/<descripcion>")
def Mandarmensaje10(descripcion):
    return render_template('IEEErep10.html', descripcion = descripcion)

#______________________________________________Reporte 14______________________________________________________
#----------------------------------Muertes según regiones de un país - Covid 19.-----------------------------------
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
    
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
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
    plt.title("Muertes según regiones de un país - Covid 19\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Muertes')

    plt.savefig("static/Reportes/rep14.png")

    plt.close()

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.95):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
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
    
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

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
    plt.title("Tendencia de casos confirmados de Coronavirus en un departamento de un País.\n " + title, fontsize=10)
    plt.xlabel('Fecha')
    plt.ylabel('Infectados')

    plt.savefig("static/Reportes/rep15.png")

    plt.close()

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1"
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1"
    elif(r2 >= 0.95):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis15.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado15/<descripcion>")
def Mandarmensaje15(descripcion):
    return render_template('IEEErep15.html', descripcion = descripcion)


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
    
    x=np.asarray(df[df[pais]==seleccion_rep1][ejex]).reshape(-1,1)
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

    if(pend > 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion positivo de " + str(pend)
        elif(r2 >= 0.95):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion positivo de " + str(pend)
    elif(pend < 0):
        if(r2 < 0.25):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 < 0.5):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 < 0.75):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con un indice de progresion negativo de " + str(pend)
        elif(r2 >= 0.95):
            descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + "los paises " + " se ve afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con un indice de progresion negativo de " + str(pend)
        
    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
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

    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())


    #predi = datetime.date(str(predi)).toordinal()
    
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
    
    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    elif(r2 >= 0.95):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1." + "Con una prediccion de infectados de " + str(round(pred,2))
    
    
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
    
    try:
        df['date_ordinal'] = pd.to_datetime(df[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    x=np.asarray(df['date_ordinal']).reshape(-1,1)
    y=df[ejey]
    
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
    
    df['date_ordinal'] = pd.to_datetime(df[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    x=np.asarray(df['date_ordinal']).reshape(-1,1)
    y=df[ejey2]

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


    descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media, por lo cual nos podemos dar cuenta que los indices de infeccion y mortalidad solo se van a lograr reducir si todos nos cuidamos y seguimos las medidas precautorias"
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
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

    try:
        df['date_ordinal'] = pd.to_datetime(df[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())

    x=np.asarray(df['date_ordinal']).reshape(-1,1)
    y=df[ejey]
    
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

    df['date_ordinal'] = pd.to_datetime(df[ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    x=np.asarray(df['date_ordinal']).reshape(-1,1)
    y=df[ejey2]

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


    descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que se ven afectados de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media, por lo cual nos podemos dar cuenta que los indices de infeccion y mortalidad solo se van a lograr reducir si todos nos cuidamos y seguimos las medidas precautorias, con lo anterior descrito se sabe que la prediccion de infectados es de: " + str(round(pred,2)) + "y la prediccion de muertes es de: " + str(round(pred2,2))
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
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
    
    try:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%d/%m/%Y').apply(lambda date: date.toordinal())
    except:
        df['date_ordinal'] = pd.to_datetime(df[df[pais]==seleccion_rep1][ejex],format='%Y/%m/%d').apply(lambda date: date.toordinal())
    
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

    if(r2 < 0.25):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso no se encuentran correlacionados ya que estan muy alejados de 1" + "Con lo cual se tiene una tasa de mortalidad de: " + str(pend)
    elif(r2 < 0.5):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo no explica ninguna porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso casi no se encuentran correlacionados ya que estan muy alejados de 1" + "Con lo cual se tiene una tasa de mortalidad de: " + str(pend)
    elif(r2 < 0.75):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo medio explica la porción de la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran un poco correlacionados ya que no estan muy alejados de 1" + "Con lo cual se tiene una tasa de mortalidad de: " + str(pend)
    elif(r2 >= 0.95):
        descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que el valor del coeficiente de determinación " + str(round(r2,2)) + " indica que el modelo indica que el modelo explica toda la variabilidad de los datos de respuesta en torno a su media es decir que los datos en este caso se encuentran correlacionados ya que estan muy cercanos a 1" + "Con lo cual se tiene una tasa de mortalidad de: " + str(pend)
    

    #descripcion = "Actualmente se esta viviendo una situacion a nivel mundial con la enfermedad de Covid-19, en lo cual todos los paises nos hemos vuelto muy suceptibles, por lo cual gracias a las herramientas actuales se puede decir que " + seleccion_rep1 + " se ve afectado de manera directa. Por lo cual realizando un analisis de regresion polinomial de grado 3, nos podemos dar cuenta que se tiene un error cuadrático medio de " + str(round(rmse,2)) + " este error medio nos indica la cantidad de de error que tenemos entre los conjuntos de datos " + " de fechas e infecciones que se estan dando en el pais este datos nos ayuda para poder evaluar la tendencia entre dos valores, ahora bien nos podemos dar cuenta que "
    
    return render_template("analisis22.html", Encabezados = recorrertitulosExcel(), descripcion = descripcion)

@app.route("/mensajeenviado22/<descripcion>")
def Mandarmensaje22(descripcion):
    return render_template('IEEErep22.html', descripcion = descripcion)


































































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

