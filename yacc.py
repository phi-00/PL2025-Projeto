from lex import tokens, lexer, re
import ply.yacc as yacc
import sys

output = ""  # Variável global para armazenar o código gerado
symbol_table = {}  # Tabela de símbolos para armazenar variáveis e seus valores

# Regra inicial
def p_Z(p):
    'Z : expressao'
    global output
    p[0] = p[1]

# Regra para expressao
def p_expressao(p):
    '''expressao : declaracao_programa declaracao_var declaracao_end_begin
                 | declaracao_programa declaracao_end_begin'''
    p[0] = p[1]

# Regra para declaracao_programa
def p_declaracao_programa(p):
    'declaracao_programa : PROGRAM IDENTIFIER SEMICOLON'
    p[0] = p[2]  # Retorna o identificador do programa

# Regra para declaracao_var
def p_declaracao_var(p):
    '''declaracao_var : VAR lista_variaveis COLON tipo SEMICOLON
                      | declaracao_var lista_variaveis COLON tipo SEMICOLON'''
    global symbol_table
    if len(p) == 6:  # Caso base: VAR lista_variaveis COLON tipo SEMICOLON
        for var in p[2]:
            symbol_table[var] = None  # Inicializa as variáveis na tabela de símbolos
    else:  # Caso recursivo: declaracao_var lista_variaveis COLON tipo SEMICOLON
        for var in p[2]:
            symbol_table[var] = None
    p[0] = f"Variáveis: {p[2]} do tipo {p[4]}"

# Regra para lista_variaveis
def p_lista_variaveis(p):
    '''lista_variaveis : IDENTIFIER
                       | IDENTIFIER COMMA lista_variaveis'''
    if len(p) == 2:  # Caso base: IDENTIFIER
        p[0] = [p[1]]
    else:  # Caso recursivo: IDENTIFIER COMMA lista_variaveis
        p[0] = [p[1]] + p[3]

# Regra para tipo
def p_tipo(p):
    '''tipo : INTEGER
            | REAL
            | STRING'''
    p[0] = p[1]

# Regra para declaracao_end_begin
def p_declaracao_end_begin(p):
    '''declaracao_end_begin : BEGIN corpo END DOT'''
    p[0] = p[2]  # Retorna o corpo

# Regra para corpo
def p_corpo(p):
    '''corpo : comando
             | comando corpo'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

# Regra para comando
def p_comando(p):
    '''comando : atribuicao
               | write'''
    p[0] = p[1]

# Regra para atribuicao
def p_atribuicao(p):
    'atribuicao : IDENTIFIER ASSIGN expressao_aritmetica SEMICOLON'
    global output, symbol_table
    if p[1] in symbol_table:
        output += f"PUSHG {list(symbol_table.keys()).index(p[1])}\n"
        output += f"PUSHI {p[3]}\n"
        output += f"STOREG {list(symbol_table.keys()).index(p[1])}\n"
        symbol_table[p[1]] = p[3]  # Atualiza o valor da variável na tabela de símbolos
    else:
        print(f"Erro: Variável '{p[1]}' não declarada.")
    p[0] = output

# Regra para expressao_aritmetica
def p_expressao_aritmetica(p):
    '''expressao_aritmetica : termo
                            | expressao_aritmetica PLUS termo'''
    global output
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]
        output += "ADD\n"

# Regra para termo
def p_termo(p):
    '''termo : NUMBER
             | IDENTIFIER'''
    global output, symbol_table
    if isinstance(p[1], int):  # Número
        p[0] = int(p[1])
        output += f"PUSHI {p[1]}\n"
    elif p[1] in symbol_table:  # Variável
        p[0] = symbol_table[p[1]]
        output += f"PUSHG {list(symbol_table.keys()).index(p[1])}\n"
    else:
        print(f"Erro: Variável '{p[1]}' não declarada.")

# Regra para write
def p_write(p):
    '''write : WRITELN LPAREN argumentos RPAREN SEMICOLON'''
    global output, symbol_table
    for arg in p[3]:  # Processa cada argumento
        if isinstance(arg, str) and (arg.startswith("'") or arg.startswith('"')):  # Caso seja texto
            output += f'PUSHS "{arg[1:-1]}"\nWRITES\n'
        elif arg in symbol_table:  # Caso seja uma variável
            output += f"PUSHG {list(symbol_table.keys()).index(arg)}\nWRITEI\n"
        else:
            print(f"Erro: Argumento '{arg}' não reconhecido.")
    p[0] = output

# Regra para argumentos
def p_argumentos(p):
    '''argumentos : argumento
                  | argumento COMMA argumentos'''
    if len(p) == 2:  # Caso base: um único argumento
        p[0] = [p[1]]
    else:  # Caso recursivo: argumento COMMA argumentos
        p[0] = [p[1]] + p[3]

# Regra para argumento
def p_argumento(p):
    '''argumento : TEXT
                 | IDENTIFIER'''
    p[0] = p[1]

# Tratamento de erros
def p_error(p):
    print("Erro sintático no input!")
    if p:
        print(f"Erro próximo ao token: {p.value}")
    else:
        print("Erro inesperado no final do input.")

# Construção do parser
parser = yacc.yacc()

# Leitura da entrada do arquivo
if __name__ == "__main__":
    try:
        entrada = sys.stdin.read()
        entrada = re.sub(r'\s{2,}', ' ', entrada)  # Remove espaços extras
        conversor = parser.parse(entrada)
        print("Resultado: \n", output)
    except Exception as e:
        print("Erro ao processar entrada:", e)



