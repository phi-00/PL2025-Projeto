import ply.lex as lex
import re
import sys

# Lista de tokens
tokens = [
    'PROGRAM',
    'VAR',
    'TYPE',
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
    'FUNCTION',
    'PROCEDURE',
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULE',
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
    'INTEGER',
    'BOOLEAN',
    'STRING',
    'REAL',
    'CHAR'
]

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'%'
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
t_BOOLEAN = r'boolean'
t_STRING = r'string'
t_REAL = r'real'
t_CHAR = r'char'
t_WRITE = r'write'
t_WRITELN = r'writeln'
t_READLN = r'readln'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_FOR = r'for'
t_DOWNTO = r'downto'
t_TO = r'to'
t_DO = r'do'
t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'
t_WHILE = r'while'
t_FUNCTION = r'function'
t_PROCEDURE = r'procedure'
t_TYPE = r'type'



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