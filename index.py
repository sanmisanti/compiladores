from ply import yacc
import ply.lex as lex
from os.path import commonpath
from transalte import *
import sys, os

file_path = "resultado.txt"


# Declaración de tokens
reserved = {
    'PEMP': 'INICIOPROG',
    'PTER': 'FINPROG',
    'entero': 'INT',
    'texto': 'STRING',
    'decimal': 'FLOAT',
    'logico': 'BOOL',
    'AVAN': 'AVANZAR',
    'RETRO': 'RETROCEDER',
    'GIRAI': 'GIRARIZQ',
    'GIRAD': 'GIRARDER',
    'STOP': 'DETENER',
    'SI':  'SI',
    'SINO':  'SINO',
    'DURANTE':  'DURANTE',
    'PININ': 'PININ',
    'PINOU': 'PINOU',
    "DEFPI": "DEFPI",
    "DEFP": "PROC",
    "DEFF": "FUNC"
}


tokens = ['IMPORT', 'VBLE', 'MULT', 'RESTA', 'DIV', 'ASIGN', 'COMLIN', 'COMBLO', 'ESPERAR', 'DSTRING', 'COMA', 'IDEN', 'DINT', 'DBOOL',
          'DFLOAT', 'APAR', 'CPAR', 'ACOR', 'CCOR', 'LIBRER', 'DPUNT', 'COMP', 'SUMA', 'FINLINEA', "ALLA", "CLLA"] + list(reserved.values())

# Definición de Tokens (ER)


def t_LIBRER(t):
    r'[a-zA-Z]+(\.)[a-zA-Z]+'
    t.type = reserved.get(t.value, 'LIBRER')    # Check for reserved words
    return t


def t_SUMA(t):
    r'\+'
    t.type = reserved.get(t.value, 'SUMA')    # Check for reserved words
    return t


def t_COMP(t):
    r'(\<=)|(\>=)|(\==)|(\<>)|(\<)|(\>)'
    t.type = reserved.get(t.value, 'COMP')    # Check for reserved words
    return t


def t_RESTA(t):
    r'\-'
    t.type = reserved.get(t.value, 'RESTA')    # Check for reserved words
    return t


def t_MULT(t):
    r'\*'
    t.type = reserved.get(t.value, 'MULT')    # Check for reserved words
    return t



def t_DIV(t):
    r'\%'
    t.type = reserved.get(t.value,'DIV')    # Check for reserved words
    return t



def t_DPUNT(t):
    r':'
    t.type = reserved.get(t.value, 'DPUNT')    # Check for reserved words
    return t


def t_CCOR(t):
    r'\]'
    t.type = reserved.get(t.value, 'CCOR')    # Check for reserved words
    return t


def t_ACOR(t):
    r'\['
    t.type = reserved.get(t.value, 'ACOR')    # Check for reserved words
    return t


def t_CPAR(t):
    r'\)'
    t.type = reserved.get(t.value, 'CPAR')    # Check for reserved words
    return t


def t_APAR(t):
    r'\('
    t.type = reserved.get(t.value, 'APAR')    # Check for reserved words
    return t


def t_COMA(t):
    r','
    t.type = reserved.get(t.value, 'COMA')    # Check for reserved words
    return t


def t_ESPERAR(t):
    r'WAIT'
    t.type = reserved.get(t.value, 'ESPERAR')    # Check for reserved words
    return t


def t_VBLE(t):
    r'VBLE'
    t.type = reserved.get(t.value, 'VBLE')    # Check for reserved words
    return t


def t_IMPORT(t):
    r'INCLUIR'
    t.type = reserved.get(t.value, 'IMPORT')    # Check for reserved words
    return t


def t_COMBLO(t):
    r'//\*\*[ A-Za-z0-9\n]*\*\*//'
    t.type = reserved.get(t.value, 'COMBLO')    # Check for reserved words
    return t


def t_COMLIN(t):
    r'//\*[ A-Za-z0-9]*'
    t.type = reserved.get(t.value, 'COMLIN')    # Check for reserved words
    return t


def t_DSTRING(t):
    r'"[a-zA-Z0-9]+"'
    t.type = reserved.get(t.value, 'DSTRING')    # Check for reserved words
    return t


def t_IDEN(t):
    r'[A-Za-z][A-Za-z0-9]*'
    t.type = reserved.get(t.value, 'IDEN')    # Check for reserved words
    return t


def t_DFLOAT(t):
    r'([0-9]+[.])[0-9]+'
    t.type = reserved.get(t.value, 'DFLOAT')    # Check for reserved words
    return t


def t_DINT(t):
    r'[0-9]+'
    t.type = reserved.get(t.value, 'DINT')    # Check for reserved words
    return t


def t_DBOOL(t):
    r'(true|false)'
    t.type = reserved.get(t.value, 'DBOOL')    # Check for reserved words
    return t


def t_ALLA(t):
    r'{'
    t.type = reserved.get(t.value, 'ALLA')    # Check for reserved words
    return t


def t_CLLA(t):
    r'}'
    t.type = reserved.get(t.value, 'CLLA')    # Check for reserved words
    return t


t_FINLINEA = r'\.'
t_ASIGN = r'='
t_ignore_esp = r'[ ]'


def t_error(t):
    print("Se encontró un error: %s" % repr(t.value[0]))
    t.lexer.skip(1)

# 5) Definir la función t_newline para el contador de linea


def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    


__file__ = "index.py"

lexer = lex.lex()
lexer.lineno=0


# ACA EMPIEZA EL SEMANTICO

def depurar(texto):
    depurador = open("depurador.txt","a")
    depurador.write(texto)
    depurador.close


def p_s(p):
    's : INICIOPROG import FINPROG'
    depurar("s\n")
    pass


def p_import(p):
    '''import : IMPORT APAR LIBRER CPAR FINLINEA import
         | declvar'''
    depurar("import\n")
    traducir(p, cb_p_librerias)
    pass


def p_declvar(p):
    '''declvar : VBLE APAR IDEN INT CPAR FINLINEA declvar
         | VBLE APAR IDEN STRING CPAR FINLINEA declvar
         | VBLE APAR IDEN FLOAT CPAR FINLINEA declvar
         | VBLE APAR IDEN BOOL CPAR FINLINEA declvar
         | COMLIN FINLINEA declvar
         | COMBLO FINLINEA declvar
         | c'''
    depurar("declvar\n")
    if (len(list(p))>4):
        traducir(p, cb_p_declvar)
    pass


def p_c(p):
    ''' c : IDEN ASIGN DSTRING FINLINEA c
          | IDEN ASIGN DBOOL FINLINEA c
          | IDEN ASIGN DFLOAT FINLINEA c
          | IDEN ASIGN DINT FINLINEA c
          | COMLIN FINLINEA c
          | COMBLO FINLINEA c
          | d'''
    depurar("c\n")
    if(len(list(p))>2):
        if ("//*" not in list(p)[1:2][0]):
            traducir(p,cb_p_asignacion)
    pass


def p_d(p):
    ''' d : IDEN ASIGN IDEN SUMA DINT FINLINEA d
          | IDEN ASIGN IDEN RESTA DINT FINLINEA d
          | IDEN ASIGN IDEN MULT DINT FINLINEA d
          | IDEN ASIGN IDEN DIV DINT FINLINEA d
          | IDEN ASIGN IDEN SUMA DFLOAT FINLINEA d
          | IDEN ASIGN IDEN RESTA DFLOAT FINLINEA d
          | IDEN ASIGN IDEN MULT DFLOAT FINLINEA d
          | IDEN ASIGN IDEN DIV DFLOAT FINLINEA d
          | IDEN ASIGN IDEN SUMA IDEN FINLINEA d
          | IDEN ASIGN IDEN RESTA IDEN FINLINEA d
          | IDEN ASIGN IDEN MULT IDEN FINLINEA d
          | IDEN ASIGN IDEN DIV IDEN FINLINEA d
          | IDEN ASIGN DINT SUMA DINT FINLINEA d
          | IDEN ASIGN DINT RESTA DINT FINLINEA d
          | IDEN ASIGN DINT MULT DINT FINLINEA d
          | IDEN ASIGN DINT DIV DINT FINLINEA d
          | IDEN ASIGN DFLOAT SUMA DFLOAT FINLINEA d
          | IDEN ASIGN DFLOAT RESTA DFLOAT FINLINEA d
          | IDEN ASIGN DFLOAT MULT DFLOAT FINLINEA d
          | IDEN ASIGN DFLOAT DIV DFLOAT FINLINEA d
          | COMLIN FINLINEA d
          | COMBLO FINLINEA d
          | e
          | empty'''
    depurar("d\n")
    if (len(list(p))>4):
        traducir(p,cb_p_d)
    pass

def p_empty(p):
    'empty :'
    depurar("empty\n")
    pass


def p_e(p):
    ''' e : FUNC IDEN APAR argumentos CPAR DPUNT INT ALLA declvar CLLA e
          | FUNC IDEN APAR argumentos CPAR DPUNT STRING ALLA declvar CLLA e
          | FUNC IDEN APAR argumentos CPAR DPUNT FLOAT ALLA declvar CLLA e
          | FUNC IDEN APAR argumentos CPAR DPUNT BOOL ALLA declvar CLLA e
          | COMLIN FINLINEA e
          | COMBLO FINLINEA e
          | f'''
    if(len(list(p))>=4):
        cb_p_funcion(p)
    depurar("e\n")
    pass




def p_argumentos(p):
    '''argumentos : IDEN DPUNT INT COMA argumentos2
                  | IDEN DPUNT FLOAT COMA argumentos2
                  | IDEN DPUNT STRING COMA argumentos2
                  | IDEN DPUNT BOOL COMA argumentos2
                  | IDEN DPUNT INT
                  | IDEN DPUNT FLOAT
                  | IDEN DPUNT STRING
                  | IDEN DPUNT BOOL
                  | '''
    p[0] = p[1:]
    p[0] = flatten_vector(p[0])
    depurar("argumentos\n")
    pass


def p_argumentos2(p):
    '''argumentos2 : IDEN DPUNT INT COMA argumentos2
                  | IDEN DPUNT FLOAT COMA argumentos2
                  | IDEN DPUNT STRING COMA argumentos2
                  | IDEN DPUNT BOOL COMA argumentos2
                  | IDEN DPUNT INT argumentos
                  | IDEN DPUNT FLOAT argumentos
                  | IDEN DPUNT STRING argumentos
                  | IDEN DPUNT BOOL argumentos '''
    p[0] = p[1:]
    depurar("argumentos2\n")
    pass


def p_f(p):
    ''' f : PROC IDEN APAR argumentos CPAR ALLA declvar CLLA f
          | COMLIN FINLINEA f
          | COMBLO FINLINEA f
          | g'''
    if(len(list(p))>=4):
        cb_p_procedimiento(p)
    depurar("f\n")
    pass


def p_g(p):
    ''' g : DEFPI APAR PININ DPUNT DINT CPAR FINLINEA g
          | DEFPI APAR PINOU DPUNT DINT CPAR FINLINEA g
          | DEFPI APAR PININ DPUNT IDEN CPAR FINLINEA g
          | DEFPI APAR PINOU DPUNT IDEN CPAR FINLINEA g
          | COMLIN FINLINEA g
          | COMBLO FINLINEA g
          | h'''
    if (len(list(p))>4):
        cb_p_defpi(p)
    depurar("g\n")
    pass
        



def p_h(p):
    ''' h : SI APAR IDEN COMP IDEN CPAR APAR declvar CPAR SINO APAR declvar CPAR h
          | SI APAR IDEN COMP DINT CPAR APAR declvar CPAR SINO APAR declvar CPAR h
          | SI APAR IDEN COMP DFLOAT CPAR APAR declvar CPAR SINO APAR declvar CPAR h
          | SI APAR IDEN COMP IDEN CPAR APAR declvar CPAR h
          | SI APAR IDEN COMP DINT CPAR APAR declvar CPAR h
          | SI APAR IDEN COMP DFLOAT CPAR APAR declvar CPAR h
          | DURANTE APAR IDEN COMP IDEN CPAR ACOR declvar CCOR h
          | DURANTE APAR IDEN COMP DINT CPAR ACOR declvar CCOR h
          | DURANTE APAR IDEN COMP DFLOAT CPAR ACOR declvar CCOR h
          | COMLIN FINLINEA h
          | COMBLO FINLINEA h
          | mov
          | empty'''
    longitud =len(list(p))
    if(longitud>1):
        if (list(p)[1:2][0] == "DURANTE"):
            traducir(p,cb_p_durante)
        elif (longitud==11):
            traducir(p,cb_p_si)
        elif (longitud==15):
            traducir(p,cb_p_sino)
    depurar("h\n")
    pass



def p_mov(p):
    '''mov : AVANZAR APAR CPAR FINLINEA mov
           | RETROCEDER APAR CPAR FINLINEA mov
           | GIRARIZQ APAR CPAR FINLINEA mov
           | GIRARDER APAR CPAR FINLINEA mov
           | ESPERAR APAR DINT CPAR FINLINEA mov
           | DETENER APAR CPAR FINLINEA mov
           | COMLIN FINLINEA mov
           | COMBLO FINLINEA mov
           | empty ''' 
    if (len(list(p))>4):
        traducir(p,cb_p_mov)
    depurar("mov\n")
    pass
    


def p_error(p):
    print("Error sintáctico en la li­nea: " + str(p.lineno)
          + ". No se esperaba el token: " + str(p.value))
    depurar("error\n")
    raise Exception('syntax', 'error')


__file__ = "index.py"
parser2 = yacc.yacc(write_tables=False)

while True:
    try:

        s = input('Enter para comenzar análisis > ')   # Use raw_input on Python
        
        limpiarArchivos()
        
        
        
        #Leo la entrada
        textoprueba = open("texto_prueba.txt", "r")
        entrada = textoprueba.read()
        textoprueba.close()
        
        
        lexer.input(entrada)
        print('Token - Lexema')
        while True:
            tok = lexer.token()
            if not tok:
                break
            print('(', tok.type, ',', tok.value, ')')
    except EOFError:
        print("EOFError")
        break
    try:
        parser2.parse(entrada)
        print("Analsis correcto")
        try:
            escribirFinal()
            print("ARCHIVO COMPILADO CORRECTAMENTE EN 'compilado.txt'")
        except:
            print("Error escribiendo")

    except Exception as e:
        print(e)
        print("Analisis Incorrecto")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
