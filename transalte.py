def escribirFinal():
    archivo = open("resultado.txt", "r")

    compilado = open("compilado.ino", "w")
    compilado.write("")
    compilado.close()

    compilado = open("compilado.ino", "a")

    lineas = archivo.readlines()

    archivo.close()
    for linea in reversed(lineas):
        compilado.write(linea)
    compilado = open("compilado.ino", "a")
    setup=open("auxiliar.txt", "r")
    texto = setup.readlines()
    texto = [elemento for elemento in texto if elemento != "\n"]
    compilado.write("".join(texto))
    
    auxLoop = open("auxiliarLoop.txt","r")
    textoLoop=auxLoop.readlines()
    compilado.write("void loop(){\n")
    for linea in reversed(textoLoop):
        compilado.write(linea)
    
    compilado.write("}")
    compilado.close()
    setup.close()
    auxLoop=open("auxiliarLoop.txt","w")
    auxLoop.close()
    auxSetup = open("auxiliar.txt","w")
    auxSetup.close()


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


def cb_p_defpi(p,isfirst):
    
    
    list_cast = list (p)
    print("1")
    if(p[1]!=None):
        print("2")
        file = open("resultado.txt", 'a')
        quees = {"PINOU": "OUTPUT",
                 "PININ": "INPUT"}
        td = quees.get(list_cast[3:4][0])
        print(isfirst)
        if (isfirst):
            archivoAuxiliarWrite = open("auxiliar.txt","w")
            print("3")
            archivoAuxiliarWrite.writelines(['void setup(){\n'] + ['\n'] +['\n}\n'])
            archivoAuxiliarWrite.close()
        pinNP= ["pinMode("]+list_cast[5:6]+[", "]+[td]+[");"]
        print("pinMP", pinNP)
        archivoAuxiliarRead = open("auxiliar.txt","r")
        archivoAuxiliarReadList=archivoAuxiliarRead.readlines()
        print("archivoAuxiliarReadList: ",archivoAuxiliarReadList)
        index = archivoAuxiliarReadList.index('\n')
       
        print("indeXx: ", index)
        archivoAuxiliarReadList[index]=pinNP
        vectorInterior = archivoAuxiliarReadList[index]
        archivoAuxiliarReadList[index:index+1] = ["\n\n"]+vectorInterior
        print("archivoAuxiliarReadList2: ",archivoAuxiliarReadList)
        resultado="".join(archivoAuxiliarReadList)
        archivoAuxiliarWrite = open("auxiliar.txt","w")
        archivoAuxiliarWrite.write(resultado)
        archivoAuxiliarWrite.close()
        file.close()
        
        archivoAuxiliarRead.close()

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
    