# Manual Tecnico Simple C

## Objetivos:
Crear un analizador lexico capaz de repotar si un codigo fuente pertenece o no a dicho lenguaje



## Datos que el analizador lexico debe ser capaz de reconocer
// comentario

/* 
   comentario de varias lineas
*/ 

### Tipos de datos
int  
Double  
String  
Char  
Boolean  

### Identificadores
[Letra o guion bajo][cero o mas letras, guiones bajos o numeros]
_
_2
__
A_
A2

### Operaciones
- Suma +
- Resta -
- Multiplicacion *
- Division /
- Resto %
- Igualacion ==
- Asignacion =
- Diferenciacion !=
- Mayor igual >=
- Mayor >
- Menor igual <=
- Menor <
- AND &&
- OR ||
- NOT !

### Otros
- Llaves {}
- Corchetes []
- Parentesis ()
- punto y coma ;

### Estructuras condicionales
- if {}
- if{} else {}
  
### Estructuras iterativas
- while {}
- do {} while  

### Funciones y metodos
- Metodo void [ID][parametros]{}
- Funcion [TipoDato][ID][parametros]{}
- (Paramentro,)*
  
## Listado de Tokens y patrones que usara el programa

| TOKEN                 | DESCRIPCION                 | PATRON       | 
| --------------------- | --------------------------- | ------------ |  
| tk_comentario_simple  | Comentario de una linea     | //           |
| tk_comentario_A       | comentario Abierto          | /*           |
| tk_comentario_C       | comentario Cerrado          | */           |
| tk_tipo_int           | tipo int                    | int          |
| tk_dato_int           | dato de tipo int            | [0-9]+       |
| tk_tipo_double        | tipo double                 | double       |
| tk_dato_double        | dato de tipo double         | [0-9]+.[0-9]{1,2} | 
| tk_tipo_string        | tipo string                 | string       |
| tk_dato_string        | dato de tipo string         | "[a-zA-Z|0-9|\s][a-zA-Z|0-9|\s]\*"|
| tk_tipo_char          | tipo char                   | char         |
| tk_dato_char          | dato de tipo char           | '[a-zA-Z0-9]'|
| tk_tipo_boolean       | tipo boolean                | boolean      |
| tk_dato_boolean       | dato de tipo Boolean        | (true|false) | 
| tk_identificador      | identificador               | [a-zA-Z_][a-zA-Z0-9_]* |
| tk_suma               | operador suma               | +            |
| tk_resta              | operador resta              | -            |
| tk_multiplicacion     | operador multiplicacion     | *            |
| tk_division           | operador division           | /            |
| tk_resto              | operador resto              | %            |
| tk_igualacion         | operador igualacion         | ==           |
| tk_diferenciacion     | operador diferencia         | !=           | 
| tk_asignacion         | operador asignacion         | =            |
| tk_mayor_igual        | operador mayor o igual      | >=           |
| tk_mayor              | operador mayor              | >            |
| tk_menor_igual        | operador menor igual        | <=           |
| tk_menor              | operdaor menor              | <            |
| tk_operador_and       | operador and                | &&           |
| tk_operdaor_or        | operador or                 | \|\|          |
| tk_operdaor_not       | operdaor not                | !            |
| tk_llaveA             | llave abierta               | {            |
| tk_llaveB             | llave cerrada               | }            |
| tk_corcheteA          | corchete abierto            | [            |
| tk_corcheteB          | corchete cerrado            | ]            |
| tk_parentesisA        | parentesis abierto          | (            |
| tk_parentesisC        | parentesis cerrado          | )            | 
| tk_punto_coma         | punto y coma                | ;            |
| tk_condicional_else   | condicional else         | else         |
| tk_condicional_if     | condicional if              | if           |
| tk_ciclo_while        | ciclo while                 | while        |
| tk_ciclo_do           | ciclo do while              | do           |


# AFD'S GENERADOS POR METODO DEL ARBOL
## Expresion regular Usada:
-Expresion : [0-9]+#

### Paso 1: Elaboracion del arbol, con las hojas de izquierda a derecha

![Ruta de AFD metodo del arbol](https://drive.google.com/file/d/1zNVW-rXLxc1Vf8xSI_ETsXJZiNBnfgiO/view?usp=sharing)