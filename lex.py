import ply.lex as lex
import re

# Lista de tokens
tokens = [
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    'INTEGER',
    'WRITE',
    'WRITELN',
    'READLN',
    'IF',
    'THEN',
    'ELSE',
    'FOR',
    'TO',
    'DO',
    'WHILE',
    'AND',
    'FUNCTION',
    'PROCEDURE',
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
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
]

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
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

# Expressões regulares para tokens com palavras-chave
t_PROGRAM = r'program'
t_VAR = r'var'
t_BEGIN = r'begin'
t_END = r'end'
t_INTEGER = r'integer'
t_WRITE = r'write'
t_WRITELN = r'writeln'
t_READLN = r'readln'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_FOR = r'for'
t_TO = r'to'
t_DO = r'do'
t_WHILE = r'while'
t_FUNCTION = r'function'
t_PROCEDURE = r'procedure'



def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = ' \t\n\r'


def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()


