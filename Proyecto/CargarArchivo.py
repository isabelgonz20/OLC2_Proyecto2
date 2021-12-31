import os
from flask import Flask
from flask import request
from flask import render_template
from werkzeug import secure_filename

app = Flask(__name__)
app. config['UPLOAD_FOLDER'] = "./Archivos"
@app.route('/')
def index():
    return 'Cambios'

if __name__ == '__main__':
    app.run(debug= True, port= 8000)

@app.route("/uploader", methods = ['POST'])
def uploader():
    if request.method == "POST":
        f = request.files['archivo']
        filename = secure_filename(f.filename) 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "Archivo subido exitosamente"