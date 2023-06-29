def escribirFinal():
    #Leo la seccion 1
    archivo = open("resultado.txt", "r")
    lineas = archivo.readlines()
    archivo.close()
    
    #Escribo en compilado la seccion 1 al reves
    compilado = open("compilado.ino", "a")
    for linea in reversed(lineas):
        compilado.write(linea)
    
    #Leo la seccion Setup y escribo en Compilado
    setup=open("auxiliarSetup.txt", "r")
    texto = setup.readlines()
    compilado.write("".join(["void setup(){\n"]+texto+["\n}"]))
    
    
    #Leo la seccion Loop y escribo en compilado al reves
    auxLoop = open("auxiliarLoop.txt","r")
    textoLoop=auxLoop.readlines()
    compilado.write("void loop(){\n")
    for linea in reversed(textoLoop):
        compilado.write("\t"+linea)
    compilado.write("}")
    
    #Cierro los archivos
    compilado.close()
    setup.close()
    
    #Blanqueo los auxiliares
    

def limpiarArchivos():
    auxLoop=open("auxiliarLoop.txt","w")
    auxLoop.close()
    auxSetup = open("auxiliarSetup.txt","w")
    auxSetup.close()
    file = open("resultado.txt", 'w')
    file.close()
    compilado = open("compilado.ino", "w")
    compilado.write("")
    compilado.close()

def traducir(p, callback):
    callback(p)


def cb_p_librerias(p):
    list_cast = list(p)
    if (p[1] != None):
        file = open("resultado.txt", 'a')
        resultado = "".join(["#include <"]+list_cast[3:4]+[".h>"]+["\n"])
        file.write(resultado)
        file.close()

def cb_p_declvar(p):
    list_cast = list(p)
    if (p[1] != None):
        file = open("resultado.txt", 'a')
        quees={"entero": "int",
                 "texto": "String",
                 "decimal": "float",
                 "logico":"bool"}
        tipoDato = quees.get(list_cast[4:5][0])
        resultado = "".join([tipoDato]+[" "]+list_cast[3:4]+[";\n"])
        file.write(resultado)
        file.close()
        
def cb_p_asignacion(p):
    list_cast = list(p)
    if (p[1] != None):
        file = open("resultado.txt", 'a')
        resultado = "".join(list_cast[1:2]+[":="]+list_cast[3:4]+[";\n"])
        file.write(resultado)
        file.close()

def cb_p_d(p):
    list_cast = list (p)
    if(p[1]!=None):
        file = open("resultado.txt", 'a')
        resultado = "".join(list_cast[1:2]+["="]+list_cast[3:4]+list_cast[4:5]+list_cast[5:6]+[";\n"])
        file.write(resultado)
        file.close()


def cb_p_defpi(p):

    list_cast = list (p)
    if(p[1]!=None):
        auxiliarSetup = open("auxiliarSetup.txt", "a")
        
        
        """ file = open("resultado.txt", 'a') """
        quees = {"PINOU": "OUTPUT",
                 "PININ": "INPUT"}
        td = quees.get(list_cast[3:4][0])
        pinNP= ["\tpinMode("]+list_cast[5:6]+[", "]+[td]+[");\n"]
        auxiliarSetup.write("".join(pinNP))
        auxiliarSetup.close()

def cb_p_si(p):
    list_cast = list (p)
    if(p[1]!=None):
        file = open("resultado.txt", 'a')
        resultado = "".join(["if ("]+list_cast[3:8]+[");\n"])
        file.write(resultado)
        file.close()

def cb_p_sino(p):
    list_cast = list (p)
    if(p[1]!=None):
        file = open("resultado.txt", 'a')
        resultado = "".join(["while("]+list_cast[3:8]+[");\n"])
        file.write(resultado)
        file.close()

def cb_p_durante(p):
    list_cast = list (p)
    if(p[1]!=None):
        file = open("resultado.txt", 'a')
        resultado = "".join(["while("]+list_cast[3:6]+[")"]+["{ }\n"])
        file.write(resultado)
        file.close()

def cb_p_mov(p):
    list_cast=list(p)
    if(p[1]!=None):
        queens={
            "AVAN": "avanzar",
            "RETRO": "retroceder",
            "GIRAI":"giro_izquierda",
            "GIRAD":"giro_derecha",
            "WAIT":"esperar",
            "STOP":"detener"
        }
        TipoDato=queens.get(list_cast[1:2][0])
        file = open("auxiliarLoop.txt", 'a')
        if TipoDato=="esperar":
            resultado="".join([TipoDato]+["("]+list_cast[3:4]+[");\n"])
        else:
            resultado="".join([TipoDato]+["();\n"])
        file.write(resultado)
        file.close()
    
def flatten_vector(vector):
    vector_resultante = []
    for elemento in vector:
        if isinstance(elemento, list):
            vector_resultante.extend(flatten_vector(elemento))
        else:
            vector_resultante.append(elemento)
    return vector_resultante
    
def cb_p_funcion(p):
    list_cast = list(p)
    if(len(list_cast)>4):
        print("1")
        resultado = open("resultado.txt","a")
        quees={"entero": "int",
                 "texto": "String",
                 "decimal": "float",
                 "logico":"bool"}
        tipoDato = quees.get(list_cast[7:8][0])
        print("2")
        args = list_cast[4:5][0]
        print("args:",args)
        argstraducidos = []
        for elemento in args:
            if elemento in quees:
                argstraducidos.extend(quees.get(elemento))
            else:
                argstraducidos.extend(elemento)
        print("td:", [tipoDato])
        print("nombre:", list_cast[2:3])
        textoEscribir="".join([tipoDato]+[" "]+list_cast[2:3]+["("]+argstraducidos+["){}\n"])
        print("textoEscribir:",textoEscribir)
        resultado.write(textoEscribir)
        resultado.close()
        
def cb_p_procedimiento(p):
    list_cast = list(p)
    if(len(list_cast)>4):
        print("1")
        resultado = open("resultado.txt","a")

        quees={"entero": "int",
                 "texto": "String",
                 "decimal": "float",
                 "logico":"bool"}

        args = list_cast[4:5][0]
        print("args:",args)
        print("nombre:", list_cast[2:3])
        argstraducidos = []
        for elemento in args:
            if elemento in quees:
                argstraducidos.extend(quees.get(elemento))
            else:
                argstraducidos.extend(elemento)
        textoEscribir="".join(list_cast[2:3]+["("]+argstraducidos+["){}\n"])
        print("textoEscribir:",textoEscribir)
        resultado.write(textoEscribir)
        resultado.close()