import ply.lex as lex
import re
import sys

# Lista de tokens
tokens = [
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    'WRITE',
    'WRITELN',
    'READLN',
    'IF',
    'THEN',
    'ELSE',
    'FOR',
    'TO',
    'DOWNTO',
    'DO',
    'WHILE',
    'AND',
    'OR',
    'NOT',
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'INTDIV',
    'MOD',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'COLON',
    'COMMA',
    'DOT',
    'LT',
    'GT',
    'LE',
    'GE',
    'EQ',
    'NE',
    'INTEGER',
    'BOOLEAN',
    'STRING',
    'REAL',
    'CHAR',
    'ARRAY',
    'OF',
    'TEXT',
    'TRUE',
    'FALSE',
    'DOTDOT',
    'LENGTH',
]

def t_TEXT(t):
    r'\'([^\\\']|\\.)*\''
    return t


def t_COMMENT(t):
    r'\{[^\}]*\}'
    pass


# Expressões regulares para tokens simples (literals)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'='
t_NE = r'<>'
t_DOTDOT = r'\.\.'


def t_INTDIV(t):
    r'(?i:div)'
    return t

def t_MOD(t):
    r'(?i:mod)'
    return t

# Controlo de fluxo
def t_IF(t):
    r'(?i:if)'
    return t

def t_THEN(t):
    r'(?i:then)'
    return t

def t_ELSE(t):
    r'(?i:else)'
    return t

def t_FOR(t):
    r'(?i:for)'
    return t

def t_DOWNTO(t):
    r'(?i:downto)'
    return t

def t_TO(t):
    r'(?i:to)'
    return t

def t_DO(t):
    r'(?i:do)'
    return t

def t_AND(t):
    r'(?i:and)'
    return t

def t_OR(t):
    r'(?i:or)'
    return t

def t_NOT(t):
    r'(?i:not)'
    return t

def t_WHILE(t):
    r'(?i:while)'
    return t

def t_LENGTH(t):
    r'(?i:length)'
    return t

# Declaração de variáveis
def t_INTEGER(t):
    r'(?i:integer)'
    return t

def t_REAL(t):
    r'(?i:real)'
    return t

def t_BOOLEAN(t):
    r'(?i:boolean)'
    return t

def t_TRUE(t):
    r'(?i:true)'
    t.value = True
    return t

def t_FALSE(t):
    r'(?i:false)'
    t.value = False
    return t


def t_STRING(t):
    r'(?i:string)'
    return t

def t_CHAR(t):
    r'(?i:char)'
    return t

def t_CHAR_LITERAL(t):
    r"'([^\\']|\\.)'"  # Caractere entre aspas simples
    t.value = t.value[1:-1]  # Remove as aspas
    return t


def t_ARRAY(t):
    r'(?i:array)'
    return t

def t_OF(t):
    r'(?i:of)'
    return t

def t_VAR(t):
    r'(?i:var)'
    return t

# Leitura e Escrita
def t_READLN(t):
    r'(?i:readln)'
    return t

def t_WRITELN(t):
    r'(?i:writeln)'
    return t

def t_WRITE(t):
    r'(?i:write)'
    return t

# Inicialização de programas

def t_BEGIN(t):
    r'(?i:begin)'
    return t

def t_PROGRAM(t):
    r'(?i:program)'
    return t

def t_END(t):
    r'(?i:end)'
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_NUMBER(t):
    r'[+|-]?\d+'
    t.value = int(t.value)
    return t


t_ignore = ' \t\n\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

def main():
    data = sys.stdin.read()
    lexer.input(data)
    for token in lexer:
        print(token)

if __name__ == '__main__':
    main()