### 
![Image text](https://i.pinimg.com/originals/e7/94/6c/e7946c7073fc9df995f6047d17125afe.png)
# **Quetzal OCL2: Manual Técnico**

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
Aplicar la fase de sintesis del compilador para lograr realizar un traductor e interprete utilizando herramientas para su analisis:
* Realizar un analisis lexico y sintactico para construir un traductor.
* Implementar la ejecucion de dicha traduccion utilizando traduccion dirigida por la sintaxis haciendo uso de atributos heredados y sintetizados.

## Funcionalidad
***
* Interpreta: Esta opción nos va a permitir interpretar una entrada. El programa recibe un archivo de entrada de código de alto nivel y ejecuta las instrucciones.
* Traducir: Esta opción nos va a permitir traducir una entrada. El programa recibe un archivo de entrada de código de alto nivel y traduce a código intermedio en la sintaxis de tres direcciones.
* Reportes: Esta opción nos va a permitir visualizar los reportes generados después de traducir una entrada.

## Flujo de la aplicación
***
![image](https://raw.githubusercontent.com/harias25/olc2-diciembre-2021/main/Proyecto%201/flujo_quetzal.png)

# Descripcion del sistema
Quetzal es un lenguaje de programación inspirado en C, su característica principal es la inclusión de tipos implícitos. El sistema de tipos de Quetzal realiza una formalización de los tipos de C y Java. Esto permite a los desarrolladores definir variables y funciones tipadas sin perder la esencia. Otra inclusión importante de Quetzal es la simplificación de los lenguajes C y Java para poder realizar diferentes instrucciones en menos pasos.

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

## Jison

Jison es, en escencia, un clone del generador grammatical Bison y Yacc, pero en javascript. Incluye su propio analizador lexico modelado en base a Flex (analizador lexico para JAVA). Fue creado originalmente por Zach Carter para ayudar el estudio de un curso de compiladores.

![image](https://user-images.githubusercontent.com/24401039/122161438-f2aa5a00-ce2e-11eb-8d97-3a5044b5aa8f.png)

# Comandos de Compilación

Instalacion Jison
```
npm install jison -g
```
Para instalar el compilador de typescript, la librería jison y el paquete copyfiles, que sirve para poder copiar, pegar y eliminar archivos en carpetas.

```
npm run build
```
Para compilar el codigo de la clase Analizador_Lexico_Sintactico.jison

```
jison Analizador_Lexico_Sintactico.jison
```

Instalacion browserify

```
npm install -g browserify
```
Ejecucion de browserify para union de js.
```
browserify .\PROYECTO1\ANALIZADOR\Ejecutar.js --standalone load > bundle.js
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

# Clases
> NodoAST.js

> Operacion.js

> Funciones.js

> GraficarTs.js

> Llamadas.js

> Main.js

> Parametros.js

> Print.js

> caracterOfPosition.js

> Length.js

> subString.js

> ToLower.js

> ToUpper.js

> TypeOf.js

> Aritmetica.js

> Arreglo.js

> Asignacion.js

> AsignacionArreglo.js

> AsignacionStruct.js

> Casteo.js

> Declaracion.js

> DeclaracionArreglos.js

> Identificador.js

> IncrementoDecremento.js

> Logica.js

> OperadorTernario.js

> Primitivo.js

> Relacional.js

> Struct.js

> For.js

> While.js

> Case.js

> If.js

> Switch.js

> Break.js

> Continue.js

> Return.js

> Arbol.js

> Error.js

> Simbolo.js

> TablaSimbolos.js

> Tipo.js

> Analizador_Lexico_Sintactico.jison

> Ejecut.js

> Ejecutar.js

> bundlle.js

> index.js

# Metodos principales
* Clase NodoAST: Es la encargada de crear los nodos del arbol abstracto. 
![image](IMAGENES/M1.png)

* Clase GraficarTS: Es la encargada de graficar la Tabla de simbolos que se genere hasta el momento que se pida.
![image](IMAGENES/M2.png)

* Clase Funcion: Es la encargada de manejar todas las funciones. 
![image](IMAGENES/M3.png)

* Clase Main: Es el encargado de ejecutar de manera correcta el programa.
![image](IMAGENES/M4.png)

* Clase Parametro: Es la encargada de de manejar los parametros que se le envian a las funciones.
![image](IMAGENES/M5.png)

* Clase Print: Es la encargada del print y el println, asi manejando los diferentes tipos de prints que se tienen.
![image](IMAGENES/M6.png)

* Clase CaracterOfPosition: Es la clase encargada que devolvera el caracter correspondiente a esa posición indicada.
![image](IMAGENES/M7.png)

* Clase Length: Es la clase encargada de la obtención del número de elementos de una cadena
![image](IMAGENES/M8.png)

* Clase ToLower: Es la clase encargada de convertir en minusculas.
![image](IMAGENES/M9.png)

* Clase Aritmetica

![image](IMAGENES/M10.png)

Entre las operaciones aritmeticas disponibles vamos a encontrar las siguientes:

    - **Suma:** La suma de dos expresiones se define por el símbolo `+` 
    - **Resta:** La resta de dos expresiones y la negación de una expresión aritmetica se define por el símbolo `-` 
    - **Multiplicación:** La multiplicación de dos expresiones se define por el símbolo `*` 
    - **División:** La división de dos expresiones se define por el símbolo `/`
    - **Modulo:** El modulo entre dos expresiones se define por el símbolo `%` 
    - **Nativas:** Quetzal posee 6 funciones nativas para la resolución de expresiones, entre ellas se encuentran:
    - **pow:** Recibe como primer parametro la base y como segundo parametro la potencia a elevar.  Ejemplo: `pow(2,4)`
    - **sqrt:**  Cálcula la raíz cuadrara de un número Ejemplo: `sqrt(4)`
    - **sin:** Resuelve la función seno del número que se ingrese
    - **cos:** Resuelve la función coseno del numero que se ingrese
    - **tan:** Resuelve la función tangente del numero que se ingrese

* Clase IncrementoDecremento: Es la clase encargada de incrementar y decrementar variables.
![image](IMAGENES/M11.png)

* Clase Primitivo: 

    ![image](IMAGENES/M12.png)

* Clase For: Es la encargada de repetir una o más instrucciones un determinado número de veces. 
![image](IMAGENES/M13.png)

* Clase Switch: Es la encargada de control de selección utilizado para permitir que el valor de una variable o expresión cambie el flujo de control de la ejecución del programa mediante búsqueda y mapa.

    ![image](IMAGENES/M14.png)

* Clase Continue: Es la encargada de detener la iteración actual y volver al principio del bucle para realizar otra iteración, si corresponde.
![image](IMAGENES/M15.png)

* Clase index: Es la clase que tiene todo el codigo html, que es utilizado para mostrar la pagina con sus funcionalidades.
![image](IMAGENES/M16.png)

# Interfaz
1. Se cuenta con una pantalla de inicio la cual muestra el nombre del programa QUETZAL OCL2.

![image](IMAGENES/A1.png)

2. Se muestran dos consolas donde se podra cargar un archivo para su analisis y en la siguiente consola se muestra el resultado de salida.

![image](IMAGENES/A2.png)

* Consola entrada
![image](IMAGENES/A3.png)

* Consola salida
![image](IMAGENES/A4.png)

* Boton cargar archivo: nos sirve para cargar un archivo que tengamos en nuestro sistema.
![image](IMAGENES/A6.png)

* Boton interpretar: nos sirve para realizar el analisis lexico, sintactico y semantico.
![image](IMAGENES/A5.png)

* Boton traducir: nos sirve para traducir nuestro codigo a 3D
![image](IMAGENES/A7.png)

3. Menu de navegacion: nos ayuda a desplazarnos por las diferentes ventanas de la aplicacion.
* ![image](IMAGENES/A9.png)
* ![image](IMAGENES/A8.png)

4. Ventana que nos muestra el reporte de errores en una tabla.
* ![image](IMAGENES/A10.png)

5. Ventana que nos muestra el reporte de tabla de simbolos.
* ![image](IMAGENES/A11.png)

6. Ventana que nos muestra el reporte de AST.
* ![image](IMAGENES/A12.png)

7. Ventana que nos muestra los botones que nos redirigen a los distintos manuales que se tienen.
* ![image](IMAGENES/A13.png)
* [Reporte Gramatical](https://github.com/Jony198/COMPI2_DICIEMBRE_2021/blob/master/PROYECTO1/Manuales/Gramatica.md): Reporte Gramatical
* [Definicion dirigida por la sintaxis](https://github.com/Jony198/COMPI2_DICIEMBRE_2021/blob/master/PROYECTO1/Manuales/DirigidaSintaxis.md): Definicion dirigida por la sintaxis
* [Manual tecnico](https://github.com/Jony198/COMPI2_DICIEMBRE_2021/blob/master/PROYECTO1/Manuales/MTecnico.md): Manual tecnico
* [Manual Usuario](https://github.com/Jony198/COMPI2_DICIEMBRE_2021/blob/master/PROYECTO1/Manuales/MUsuario.md): Manual Usuario

# Link pagina
***
* [Pagina web](https://jony198.github.io/COMPI2_DICIEMBRE_2021/): QUETZAL OLC2 2021