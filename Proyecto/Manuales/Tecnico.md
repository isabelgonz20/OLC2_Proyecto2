### 
![Image text](https://i.pinimg.com/originals/e7/94/6c/e7946c7073fc9df995f6047d17125afe.png)
# **Coronavirus Data Analysis With Machine Learning**

Escuela de Ciencias y Sistemas

Organización de Lenguajes y Compiladores 1

Vacaciones Diciembre de 2021

## Indice
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Collaboration](#collaboration)
5. [FAQs](#faqs)

## Objetivos
***
Aplicar inteligencia artificial para lograr entrenar un modelo, el cual nos ayude a realizar predicciones a un futuro o sobre la tendencia del coronavirus:
* Realizar un analisis de tendencias sobre las graficas.
* Realizar un analisis de regresion sobre las graficas que nos indiquen.

## Funcionalidad
***
* Interpretar resultados que se pueden obtener sobre las graficas
* Se requiere la implementación de una Aplicación Web que permita el ánalisis de la información, y con esta poder terminar diferentes parametros de medición y configuración para desplegar gráficas y resultados de forma agradable y de fácil entendimiento para el usuario.

## Flujo de la aplicación
***
![image](IMAGENES/A14.png)

# Descripcion del sistema
Durante la emergencia sanitaria provocada por el COVID-19, se ha observado un notable incremento en la aplicación de nuevas tecnologías al campo de la salud y la investigación. Desde la creación de todo tipo de dispositivos inteligentes destinados a detectar el más mínimo síntoma indicativo de contagio, hasta el diseño de nuevos patrones de investigación en la cura del nuevo coronavirus.

Mediante el procesamiento y análisis de noticias de todos los países del mundo, junto con información relacionada con rutas de vuelos comerciales y brotes de enfermedades, pudieron predecir, no solo la existencia de una enfermedad potencialmente pandémica, sino también el epicentro de la enfermedad. Así mismo, como su trayectoria más inmediata.

# Requerimientos minimos
> 1. Tener instalado un navegador web.
![image](https://res.cloudinary.com/pym/image/upload/c_scale,f_auto,q_auto,w_800/v1/articles/2021/js-ecmascript/navegadores-web)

> 2. Tener acceso a internet 
![image](https://www.bankinter.com/file_source/blog/Contents/Noticias/images-static/wifi.png)


# Especificación de Tecnologías utilizadas

## HTML 5

HTML 5 (HyperText Markup Language, versión 5) es la quinta revisión importante del lenguaje básico de la World Wide Web, HTML. HTML5 específica dos variantes de sintaxis para HTML: una «clásica», HTML (text/html), conocida como HTML5, y una variante XHTML conocida como sintaxis XHTML 5 que deberá servirse con sintaxis XML (application/xhtml+xml).1​2​ Esta es la primera vez que HTML y XHTML se han desarrollado en paralelo. La versión definitiva de la quinta revisión del estándar se publicó en octubre de 2014.3​

Al no ser reconocido en viejas versiones de navegadores por sus nuevas etiquetas, se recomienda al usuario común actualizar su navegador a la versión más nueva, para poder disfrutar de todo el potencial que provee HTML 5.

![image](https://user-images.githubusercontent.com/24401039/122161353-cf7faa80-ce2e-11eb-9c90-37d3abf6bb3b.png)

## CSS 3

CSS es un lenguaje de diseño gráfico que permite definir y crear la presentación de un documento estructurado escrito en un lenguaje de marcado. Es muy usado para establecer el diseño visual de los documentos web e interfaces de usuario escritas en HTML.

En la propia definición de CSS vemos que está muy ligado desde su nacimiento a HTML. Desde que nació, el objetivo de CSS fue poner un poco de orden a la hora de aplicar los estilos a las páginas web.



## Javascript

JavaScript es un lenguaje de programación o de secuencias de comandos que te permite implementar funciones complejas en páginas web, cada vez que una página web hace algo más que sentarse allí y mostrar información estática para que la veas, muestra oportunas actualizaciones de contenido, mapas interactivos, animación de Gráficos 2D/3D, desplazamiento de máquinas reproductoras de vídeo, etc., puedes apostar que probablemente JavaScript está involucrado. Es la tercera capa del pastel de las tecnologías web estándar

![image](https://user-images.githubusercontent.com/24401039/122161390-ddcdc680-ce2e-11eb-9e7e-41d5fb64dbad.png)

## Codemirror

CodeMirror es un componente de JavaScript que proporciona un editor de código en el navegador. Tiene una API de programación rica y un enfoque en la extensibilidad.

La primera versión del editor fue escrita a principios de 2007, para la consola del sitio web de Eloquent JavaScript. El código fue empaquetado por primera vez y publicado bajo el nombre de CodeMirror en mayo de 2007. Esta versión se basaba en la función contentEditable de los navegadores.1​

A finales de 2010, el proyecto Ace, otro editor de código basado en JavaScript, fue pionero en nuevas técnicas de implementación y demostró que es posible, incluso en JavaScript, manejar documentos con miles de líneas sin un rendimiento degradado. Esto provocó una reescritura de CodeMirror2​ según los mismos principios. El resultado fue la versión 2, que ya no dependía de contentEditable y mejoró significativamente el rendimiento.

![image](https://user-images.githubusercontent.com/24401039/122161428-ee7e3c80-ce2e-11eb-93ce-af56f75dfe6e.png)

## Flask

En la actualidad existen muchas opciones para crear páginas web y muchos lenguajes (PHP, JAVA), y en este caso Flask nos permite crear de una manera muy sencilla aplicaciones web con Python.

Flask es un “micro” Framework escrito en Python y concebido para facilitar el desarrollo de Aplicaciones Web bajo el patrón MVC.

![image](https://blog.tiraquelibras.com/wp-content/uploads/2019/08/Flask.png)

# Comandos de Compilación

Instalacion scikit-learn
```
pip install -U scikit-learn
```
Para instalar la libreria que nos ayudara a realizar las graficas de las predicciones de nuestros informes. 

```
pip install matplotlib
```
Lenguaje de programacion que nos ayudara a programar nuestra aplicacion

```
pip install python
```

Instalacion browserify

```
npm install -g browserify
```
Instalacion de flask
```
pip install Flask
```

# Gramaticas realizadas

Inicio de la gramática, se inicia con la producción inicial ini, la gramática es LALR.
```
ini
    : instrucciones EOF
    |EOF
```

***
La producción instrucciones deriva en instrucciones con instrucción o solo instrucción.

```
instrucciones
    : instrucciones instruccion
    |instruccion
```
***
Esta produccion toma las distintas instrucciones que se pueden generar de instrucciones.
```
instruccion
    : tipodato IDENTIFICADOR asignacionesprima fin 	
    | tipodato IDENTIFICADOR COMA IDENTIFICADOR declaracionmultiple fin
    | IDENTIFICADOR IGUAL asignaciones fin
    | tipodato listaDim IDENTIFICADOR IGUAL asignaciones fin
    | tipodato listaDim IDENTIFICADOR fin
    | IDENTIFICADOR lista_expresiones IGUAL asignaciones fin
    | RVOID RMAIN PARA PARC LLAVEA dentro LLAVEC
    | RVOID IDENTIFICADOR PARA parametros  PARC LLAVEA dentro LLAVEC
    | tipodato listaDim IDENTIFICADOR PARA parametros PARC LLAVEA dentro LLAVEC
    | tipodato IDENTIFICADOR PARA parametros PARC LLAVEA dentro LLAVEC
    | RSTRUCT IDENTIFICADOR LLAVEA parametros LLAVEC fin
    | IDENTIFICADOR asignacionesMento fin
```

***
La producccion nos sirve para los tipos de declaracion multiple.
```
declaracionmultiple
    : COMA IDENTIFICADOR declaracionmultiple
    |
```

***
La producción instrucción es la encargada de tener todas las funciones que nuestro programa acepta.
```
instrucciondentro
    : tipodato IDENTIFICADOR asignacionesprima fin
    | tipodato IDENTIFICADOR COMA IDENTIFICADOR declaracionmultiple fin
    | IDENTIFICADOR IGUAL asignaciones fin
    | RPRINT PARA asignaciones PARC fin
    | RPRINT PARA asignaciones COMA asignaciones printtipodos PARC fin
    | RPRINTLN PARA asignaciones PARC fin 
    | RPRINTLN PARA asignaciones COMA asignaciones printtipodos PARC fin
    | RIF PARA asignaciones PARC LLAVEA dentro LLAVEC elseInstruccion
    | RIF PARA asignaciones PARC instrucciondentro
    | tipodato listaDim IDENTIFICADOR IGUAL asignaciones fin
    | IDENTIFICADOR lista_expresiones IGUAL asignaciones fin
    | RWHILE PARA asignaciones PARC LLAVEA dentro LLAVEC
    | RDO LLAVEA dentro LLAVEC	RWHILE PARA asignaciones PARC
    | RSWITCH PARA asignaciones PARC LLAVEA caseslist finalswitch
    | RFOR PARA asigdeclafor PTCOMA asignaciones PTCOMA asignacionfor PARC LLAVEA dentro LLAVEC
    | RFOR IDENTIFICADOR RIN asignaciones LLAVEA dentro LLAVEC
    | IDENTIFICADOR PARA parametrosllamada PARC fin
    | RBREAK fin
    | RRETURN returnasignaciones fin
    | RCONTINUE fin
    | IDENTIFICADOR asignacionesMento fin
    | IDENTIFICADOR PUNTO valorstruct IGUAL asignaciones fin
    | IDENTIFICADOR PUNTO RPUSH PARA asignaciones PARC fin
    | IDENTIFICADOR PUNTO RPOP PARA PARC fin
    | error
```
***
Produccion que ayuda a imprimir otro tipo de println o print
```
printtipodos
    :COMA asignaciones printtipodos
    |
```
***
Produccion que ayuda a declarar los parametros de las funciones.
```
parametros
    : tipodato listaDim2 IDENTIFICADOR parametrosPrima
    |
```
***
Produccion que ayuda a declarar los parametros de las funciones.
```
parametrosPrima
    : COMA tipodato listaDim2 IDENTIFICADOR parametrosPrima
    |
```
***
Produccion que ayuda a declarar los parametros de las llamadas.
```
parametrosllamada
    : asignaciones parametrosllamadaprima
    |
```
***
Produccion que ayuda a declarar los parametros de las llamadas.
```
parametrosllamadaprima
    : COMA asignaciones parametrosllamadaprima
    |
```
***
Produccion que decide si es un arreglo o no.
```
listaDim2
    listaDim
    |
```
***
Pruduccion que asigna y declara en un for
```
asigdeclafor
    : tipodato IDENTIFICADOR IGUAL asignaciones
    | IDENTIFICADOR asignacionesMento
```
***
Produccion que signa dentro de un for.
```
asignacionfor
    : IDENTIFICADOR asignacionesMento
```
***
Prudcciones que nos ayudan a saber si hay que incrementar, decrementar o son iguales. 
```
asignacionesMento
    : IGUAL asignaciones
    | INCREMENTO
    | DECREMENTO
```
***
Prudiccion que nos retorna una asignacion. 
```
returnasignaciones
    : asignaciones
    | 
```
***
Esta producción nos ayuda a lograr implementar la lista de cases dentro de un switch, con sus diferentes factores.
```
caseslist
    : caseslist cases
    | cases
```
***
Esta producción nos ayuda a lograr implementar el case dentro de un switch, con sus diferentes factores.
```
cases
    :RCASE asignaciones DOSPUNTOS dentro
    | 
```
***
Esta producción nos ayuda a lograr implementar cuando se termina el switch.
```
finalswitch
    : casesdefault LLAVEC
    | LLAVEC
```
***
Esta producción nos ayuda a lograr implementar el case defalult dentro de un switch, con sus diferentes factores.
```
casesdefault
    :RDEFAULT DOSPUNTOS dentro
    | 
```
***
Pruduccion que nos obtiene una lista de expresiones para asignar.
```
lista_expresiones
    : lista_expresiones CORA asignaciones CORC
    | CORA asignaciones CORC
```
***
Pruduccion que nos obtiene una lista de expresiones para los arreglos.
```
listaDim
    : listaDim CORA CORC
    | CORA CORC
```
***
Produccion que sirve para verificar si existe una instruccion dentro de otra isntruccion.
```
dentro
    : dentro instrucciondentro
    | instrucciondentro
```
***
Instruccion que sirve para el ELSE del IF.
```
elseInstruccion
    : RELSE relseifInstruccion
    | 
```
***
Produccion que sirve para verificar el ELSEIF.
```
relseifInstruccion
    : RIF PARA asignaciones PARC LLAVEA dentro LLAVEC elseInstruccion
    | RIF PARA asignaciones PARC instrucciondentro
    | LLAVEA dentro LLAVEC
    | instrucciondentro		
```
***
Produccion que sirve para realizar asignaciones.
```
asignacionesprima
    : IGUAL asignaciones
    | 	
```
***
Esta producción nos sirve para poder realizar los diferentes tipos de asignación de variables.

```
asignaciones
    : asignaciones MAS asignaciones	
    | asignaciones MENOS asignaciones
    | asignaciones ASTERISCO asignaciones
    | asignaciones DIAGONAL asignaciones
    | asignaciones MODULO asignaciones
    | asignaciones CONCATENACION asignaciones
    | asignaciones REPETICION asignaciones
    | RPOW PARA asignaciones COMA asignaciones PARC
    | RSQRT PARA asignaciones PARC 		
    | RSIN PARA asignaciones PARC 
    | RCOS PARA asignaciones PARC
    | RTAN PARA asignaciones PARC 
    | MENOS asignaciones
    | asignaciones IGUALACION asignaciones operacionternaria
    | asignaciones DIFERENCIACION asignaciones 		
    | asignaciones MENORQUE asignaciones 	
    | asignaciones MAYORQUE asignaciones
    | asignaciones MENORIGUAL asignaciones 	 
    | asignaciones MAYORIGUAL asignaciones 	
    | asignaciones AND asignaciones 	
    | asignaciones OR asignaciones	
    | NOT asignaciones
    | PARA asignaciones PARC
    | IDENTIFICADOR lista_expresiones 
    | IDENTIFICADOR CORA expresionarreglo DOSPUNTOS expresionarreglo CORC 
    | NUMERAL IDENTIFICADOR lista_expresione
    | NUMERAL IDENTIFICADOR	
    | variables
    | RSTRING PARA asignaciones PARC
    | RTOINT PARA asignaciones PARC
    | RTODOUBLE PARA asignaciones PARC		
    | tipodato PUNTO RPARSE PARA asignaciones PARC	
    | IDENTIFICADOR PUNTO RTOLOWERCASE PARA PARC
    | IDENTIFICADOR PUNTO RTOUPPERCASE PARA PARC
    | IDENTIFICADOR PUNTO RLENGTH PARA PARC
    | IDENTIFICADOR PUNTO RCARACTEROFPOSITION PARA asignaciones PARC
    | IDENTIFICADOR PUNTO RSUBSTRING PARA asignaciones COMA asignaciones PARC
    | RTYPEOF PARA asignaciones PARC
    | error

```
***
Produccion que contiene las expresiones que pueden venir en un arreglo.
```
expresionarreglo
    : RBEGIN
    | REND
    | asignaciones	
```
***
Produccion que nos ayuda para crear el operador ternario.
```
operacionternaria
    : TERNARIO asignaciones DOSPUNTOS asignaciones
    | 	
```
***
Pruduccion que nos desglosa los diferentes tipos de variables con su respectica funcion. 
```
variables
    : IDENTIFICADOR llamadas
    | IDENTIFICADOR PARA parametrosllamada PARC	
    | IDENTIFICADOR PUNTO valorstruct
    | primitivo
```
***
Produccion que nos da el identificador del struct.
```
valorstruct
    : IDENTIFICADOR valorstructprima
    | IDENTIFICADOR lista_expresiones valorstructprima

```
***
Produccion que nos da el identificador del struct.
```
valorstructprima
    : PUNTO IDENTIFICADOR valorstructprima
    | PUNTO IDENTIFICADOR lista_expresiones valorstructprima
    |
```
***
Pruduccion que nos sirve para hacer el incremento y decremento.
```
llamadas
    : INCREMENTO
    | DECREMENTO
    |
```
***
Produccion fin esta producción es la encargada de finalizar una instrucción, ya que puede finalizar con punto y coma o con
ninguno. 
```
fin
    : PTCOMA
    |
```
***
La producción tipo, deriva en todos los posibles tipos de datos que se pueden utilizar en el programa
```
tipodato
    : RSTRING
    | RINT
    | RCHAR
    | RBOOLEAN
    | RDOUBLE
    | IDENTIFICADOR
```
***
Produccion que contiene los distintos tipos de datos que acepta nuestro programa. 
```
primitivo
    : ENTERO
    | DECIMAL
    | CADENA
    | CARACTER
    | RTRUE
    | RNULL
    | arregloprimitivo
```
***
Produccion que nos permite mandejar arreglos de tipo de dato primitivo.
```
arregloprimitivo
    : CORA primitivoarreglo CORC
```
***
Produccion que nos perimite manejar una asignacion de arreglos
```
primitivoarreglo
    : asignaciones primitivoarregloprima
```
***
Produccion que nos permite mandejar arreglos de tipo de dato primitivo.
```
primitivoarregloprima
    : COMA asignaciones primitivoarregloprima
    | 		
```
# Palabras reservadas
```
int                 RINT
double		        RDOUBLE
char		        RCHAR
string		        RSTRING2
String 		        RSTRING
boolean			    RBOOLEAN
true			    RTRUE
false			    RFALSE
null			    RNULL
if				    RIF
else			    RELSE
switch			    RSWITCH
case			    RCASE
default			    RDEFAULT
break			    RBREAK
while			    RWHILE
do				    RDO
for				    RFOR
println			    RPRINTLN
print			    RPRINT
return			    RRETURN
struct			    RSTRUCT
pow				    RPOW
sqrt			    RSQRT
sin				    RSIN
cos				    RCOS
tan				    RTAN
caracterOfPosition 	RCARACTEROFPOSITION
subString			RSUBSTRING
length				RLENGTH
toUppercase			RTOUPPERCASE
toLowercase			RTOLOWERCASE
parse				RPARSE
toInt				RTOINT
toDouble			RTODOUBLE
typeof				RTYPEOF
function			RFUNCTION
continue			RCONTINUE
push				RPUSH
pop					RPOP
void				RVOID
main				RMAIN
begin				RBEGIN
end					REND
in					RIN
graficar_ts			RGRAFICARTS
```
# Simbolos del lenguaje
```
%			MODULO 
:			DOSPUNTOS 
;			PTCOMA 
{			LLAVEA 
}			LLAVEC 
(			PARA 
)			PARC 
[			CORA 
]			CORC 
++			INCREMENTO 
+			MAS 
--			DECREMENTO 
-			MENOS 
*			ASTERISCO 
/			DIAGONAL 
&&			AND 
||			OR 
<=		    MENORIGUAL 
>=			MAYORIGUAL 
==			IGUALACION 
!=			DIFERENCIACION 
<			MENORQUE 
>			MAYORQUE 
=			IGUAL 
!			NOT 
&			CONCATENACION 
^			REPETICION 
?			TERNARIO 
,			COMA 
#			NUMERAL 
.			PUNTO 
```
# Expresiones regulares
```
"//".*										Comentario simple línea
[/][*][^*]*[*]+([^/*][^*]*[*]+)*[/]			Comentario multiple líneas
\"(\\[n]|\\\\|\\[t]|\\\'|\\\"|[^\\\"])*?\"  Cadena
\'(\\[n]|\\\\|\\[t]|\\\'|\\\"|[^\\\'])?\'	Caracter
[0-9]+\.[0-9]+\b  	                        Decimal
[0-9]+\b				                    Entero
([a-zA-Z_])[a-zA-Z0-9_]*	                Identificador
```

# Archivos principales
> index.html

> analisis.html

> IEEE.html

> iniciorep.html

> template.py

> Cargararchivo.py

> Subirarchivo.py

# Librerias
>import os

>from re import X

>from flask import Flask

>from flask import request

>from flask import render_template

>from werkzeug.utils import secure_filename

>from werkzeug.datastructures import  FileStorage

>import matplotlib.pyplot as plt

>import numpy as np

>import pandas as pd

>from sklearn import linear_model

>from sklearn.metrics import mean_squared_error, r2_score

>from flask_wtf import FlaskForm 

>from wtforms import SelectField

>from datetime import date, datetime

>import seaborn as sns

>from sklearn.linear_model import LinearRegression  

>from sklearn.preprocessing import PolynomialFeatures 

>from sklearn import preprocessing

# Metodos principales
* Uploader: Metodo que se encarga de obtener la ruta del archivo. 
![image](IMAGENES/A15.png)

* Recorrer CSV: Metodo que se encarga de recorrer todos los titulos de nuestro csv
![image](IMAGENES/A16.png)

* App: Metodo principal que ejecuta toda la aplicacion 
![image](IMAGENES/A17.png)


# Interfaz
1. Se cuenta con una pantalla de inicio la cual muestra el nombre del programa Coronavirus Data Analysis With Machine Learning

![image](IMAGENES/A1.png)

2. Se cuenta con un area de carga de documentos tipo csv, que nos ayudaran a realizar el analisis correspondiente.

![image](IMAGENES/A2.png)

3. Opciones de analisis: Nos muestra un listado con todas las opciones de informe con las que contamos.
* ![image](IMAGENES/A3.png)
* ![image](IMAGENES/A4.png)
* ![image](IMAGENES/A5.png)
* ![image](IMAGENES/A6.png)
* ![image](IMAGENES/A7.png)
* ![image](IMAGENES/A8.png)

4. Manuales: Ventana que nos muestra un boton del manual de usuario y tecnico.
* ![image](IMAGENES/A9.png)

5. Ventana que nos muestra el titulo y la opcion de ingresar o regresar al inform
* ![image](IMAGENES/A10.png)

6. Ventana que nos pedira los datos requeridos para realizar el analisis correspondiente
* ![image](IMAGENES/A11.png)

7. Ventana que nos muestra los botones que nos permitiran realizar el analisis o enviarnos a descargar nuestro reporte del analisis correctapondiente.
* ![image](IMAGENES/A12.png)

8. Ventana que nos muestra el reporte en formato IEEE del analisis que hemos realizo, el cual se podra descargar en formato .pdf.
* ![image](IMAGENES/A13.png)

9. Ventana que nos muestra los botones que nos redirigen a los distintos manuales que se tienen.
* ![image](IMAGENES/A9.png)
* [Manual tecnico](https://github.com/isabelgonz20/OLC2_Proyecto2/blob/master/Proyecto/Manuales/Tecnico.md): Manual tecnico
* [Manual Usuario](https://github.com/isabelgonz20/OLC2_Proyecto2/blob/master/Proyecto/Manuales/Usuario.md): Manual Usuario

# Link pagina
***
* [Pagina web](http://34.125.68.190:8000/): Coronavirus Data Analysis With Machine Learning