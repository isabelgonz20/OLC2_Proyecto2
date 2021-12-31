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



app = Flask(__name__)
app. config['UPLOAD_FOLDER'] = "./Archivos"
@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/opcionesrep2')
#def inirep2():
#    return render_template('iniciorep2.html')

@app.route('/iniciorep2')
def pagina2():
    return render_template('iniciorep2.html')

@app.route('/iniciorep2/regresionlineal')
def pagina3():
    return render_template('prediccion_lineal.html')

@app.route("/", methods = ['POST'])
def uploader():
    if request.method == "POST":
        f = request.files['archivo']
        filename = secure_filename(f.filename) 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Refresionlineal_prediccion(filename)
        print(filename)

        return render_template('index.html')


def Refresionlineal_prediccion(filename):
    df = pd.read_csv("Archivos/" + filename)

    print(df)
    x = np.asanyarray(df['Anio']).reshape(-1,1)
    y = df['Republica']

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
    plt.show()

    print(regr.predict([[50]])) 


if __name__ == '__main__':
    app.run(debug= True, port= 8000)

########################################################################

