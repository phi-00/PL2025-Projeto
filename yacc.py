from lex import tokens, lexer, re
import ply.yacc as yacc
import sys

output = ""  # Variável global para armazenar o código gerado
symbol_table = {}  # Tabela de símbolos para armazenar variáveis e seus valores
label_count = 0

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),  
    ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def new_label():
    global label_count
    label = f"L{label_count}"
    label_count += 1
    return label

# Função para concatenação segura de strings, evitando None
def concat_safe(*args):
    return "".join([str(arg) if arg is not None else "" for arg in args])

# Regra inicial
def p_Z(p):
    'Z : expressao'
    global output
    output = p[1] if p[1] is not None else ""  # Corrigido para evitar None
    p[0] = output

# Regra para a expressão
def p_expressao(p):
    '''expressao : declaracao_programa declaracao_var bloco_programa'''
    p[0] = p[3] if p[3] is not None else ""  # Protege contra None

# Regra para declaração do programa
def p_declaracao_programa(p):
    'declaracao_programa : PROGRAM IDENTIFIER SEMICOLON'
    p[0] = ""

# Regra para declaração de variáveis
def p_declaracao_var(p):
    '''declaracao_var : VAR declaracoes_variaveis
                      | empty'''
    p[0] = ""

# Regra para declarações de variáveis
def p_declaracoes_variaveis(p):
    '''declaracoes_variaveis : lista_variaveis COLON tipo SEMICOLON
                             | declaracoes_variaveis lista_variaveis COLON tipo SEMICOLON'''
    global symbol_table
    if len(p) == 5:
        for var in p[1]:
            symbol_table[var] = None
    else:
        for var in p[2]:
            symbol_table[var] = None
    p[0] = ""

# Regra para lista de variáveis
def p_lista_variaveis(p):
    '''lista_variaveis : IDENTIFIER
                       | IDENTIFIER COMMA lista_variaveis'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# Regra para tipo
def p_tipo(p):
    '''tipo : INTEGER
            | REAL
            | STRING'''
    p[0] = p[1]

# Regra para o bloco do programa
def p_bloco_programa(p):
    'bloco_programa : bloco DOT'
    p[0] = p[1] if p[1] is not None else ""  # Protege contra None

# Regra para o bloco
def p_bloco(p):
    'bloco : BEGIN lista_comandos END'
    p[0] = p[2] if p[2] is not None else ""  # Protege contra None

# Regra para lista de comandos
def p_lista_comandos(p):
    '''lista_comandos : comando
                      | lista_comandos comando'''
    p[0] = concat_safe(p[1], p[2] if len(p) == 3 else "")

# Regras para comandos
def p_comando(p):
    '''comando : comando_simples
               | comando_composto'''
    p[0] = p[1] if p[1] is not None else ""  # Protege contra None

# Regras para comandos simples (atribuição, write, if, while)
def p_comando_simples(p):
    '''comando_simples : atribuicao
                       | write
                       | comando_if
                       | comando_while
                       | comando_for
                       | read'''
    p[0] = p[1] if p[1] is not None else ""  # Protege contra None

# Regras para comandos compostos (bloco)
def p_comando_composto(p):
    'comando_composto : bloco SEMICOLON'
    p[0] = p[1] if p[1] is not None else ""  # Protege contra None

# Regras para atribuição
def p_atribuicao(p):
    'atribuicao : IDENTIFIER ASSIGN expressao_aritmetica SEMICOLON'
    var_name = p[1]
    expressao = p[3]

    if var_name in symbol_table:
        # Adiciona este bloco para guardar valor (IMPORTANTE!)
        if isinstance(expressao, str) and expressao.startswith("PUSHS"):
            # Extrai o valor literal da string
            valor = expressao.split('"')[1]
        elif expressao.startswith("PUSHI"):
            valor = int(expressao.split()[1])
        else:
            valor = None

        symbol_table[var_name] = valor  # Agora sim, guarda o valor!

        codigo = concat_safe(expressao, f"STOREG {list(symbol_table.keys()).index(var_name)}\n")
        p[0] = codigo
    else:
        print(f"Erro: Variável '{var_name}' não declarada.")
        p[0] = ""


# Regras para expressões aritméticas
def p_expressao_aritmetica(p):
    '''expressao_aritmetica : expressao_aritmetica PLUS termo
                            | expressao_aritmetica MINUS termo
                            | expressao_aritmetica TIMES termo
                            | expressao_aritmetica DIVIDE termo
                            | expressao_aritmetica INTDIV termo
                            | termo'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        operador = p[2]
        if operador == '+':
            p[0] = concat_safe(p[1], p[3], "ADD\n")
        elif operador == '-':
            p[0] = concat_safe(p[1], p[3], "SUB\n")
        elif operador == '*':
            p[0] = concat_safe(p[1], p[3], "MUL\n")
        elif operador == '/':
            p[0] = concat_safe(p[1], p[3], "DIV\n")  # float division
        elif operador.lower() == 'DIV' or operador == 'div':
            p[0] = concat_safe(p[1], p[3], "IDIV\n")  # integer division


# Regras para termos
def p_termo(p):
    '''termo : LPAREN expressao_aritmetica RPAREN
             | NUMBER
             | IDENTIFIER
             | TEXT'''
    if len(p) == 4:
        # Caso com parênteses: apenas retorna o código da expressão interna
        p[0] = p[2]
    elif isinstance(p[1], int):
        p[0] = f"PUSHI {p[1]}\n"
    elif isinstance(p[1], str) and (p[1].startswith("'") or p[1].startswith('"')):
        p[0] = f'PUSHS "{p[1][1:-1]}"\n'
    elif p[1] in symbol_table:
        p[0] = f"PUSHG {list(symbol_table.keys()).index(p[1])}\n"
    else:
        print(f"Erro: Valor ou variável '{p[1]}' não reconhecido.")
        p[0] = ""


# Regras para writeln
def p_writeln(p):
    'write : WRITELN LPAREN argumentos RPAREN SEMICOLON'
    codigo = ""
    for arg in p[3]:
        if isinstance(arg, str) and (arg.startswith("'") or arg.startswith('"')):
            codigo += f'PUSHS "{arg[1:-1]}"\nWRITES\n'
        elif arg in symbol_table:
            codigo += f"PUSHG {list(symbol_table.keys()).index(arg)}\nWRITEI\n"
        else:
            print(f"Erro: Argumento '{arg}' não reconhecido.")
    p[0] = codigo if codigo else ""  # Protege contra None

# Regras para write
def p_write(p):
    'write : WRITE LPAREN argumentos RPAREN SEMICOLON'
    codigo = ""
    for arg in p[3]:
        if isinstance(arg, str) and (arg.startswith("'") or arg.startswith('"')):
            # Se for uma string literal, usa WRITES
            codigo += f'PUSHS "{arg[1:-1]}"\nWRITES\n'  # WRITES já escreve sem newline
        elif arg in symbol_table:
            # Verifica se a variável é do tipo string ou outro tipo
            var_value = symbol_table[arg]  # Pega o valor da variável
            if isinstance(var_value, str):
                # Se for string, usa WRITES
                codigo += f"PUSHG {list(symbol_table.keys()).index(arg)}\nWRITES\n"
            elif isinstance(var_value, int):  # Caso seja um inteiro
                # Se for inteiro, usa WRITEI
                codigo += f"PUSHG {list(symbol_table.keys()).index(arg)}\nWRITEI\n"
            else:
                print(f"Erro: Tipo desconhecido para a variável '{arg}'.")
        else:
            print(f"Erro: Argumento '{arg}' não reconhecido.")
    p[0] = codigo if codigo else ""


# Regras para readln
def p_readln(p):
    'read : READLN LPAREN argumentos RPAREN SEMICOLON'
    codigo = ""
    for arg in p[3]:
        if arg in symbol_table:
            var_index = list(symbol_table.keys()).index(arg)
            codigo += f"READ\nSTOREG {var_index}\n"
        else:
            print(f"Erro: Variável '{arg}' não declarada.")
    p[0] = codigo if codigo else ""  # Protege contra None


# Regras para argumentos
def p_argumentos(p):
    '''argumentos : argumento
                  | argumento COMMA argumentos'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# Regras para argumento
def p_argumento(p):
    '''argumento : TEXT
                 | IDENTIFIER'''
    p[0] = p[1] if p[1] is not None else ""  # Protege contra None

# Regras para expressões condicionais lógicas (AND / OR)
def p_expressao_condicional_logica(p):
    '''expressao_condicional : expressao_condicional AND expressao_condicional
                             | expressao_condicional OR expressao_condicional'''
    if p[2] == 'AND':
        p[0] = concat_safe(p[1], p[3], "AND\n")
    elif p[2] == 'OR':
        p[0] = concat_safe(p[1], p[3], "OR\n")


# Regras para expressões condicionais
def p_expressao_condicional(p):
    '''expressao_condicional : expressao_aritmetica GT expressao_aritmetica
                             | expressao_aritmetica LT expressao_aritmetica
                             | expressao_aritmetica GE expressao_aritmetica
                             | expressao_aritmetica LE expressao_aritmetica
                             | expressao_aritmetica EQ expressao_aritmetica
                             | expressao_aritmetica NE expressao_aritmetica'''
    if p[2] == '>':
        op = 'SUP'
    elif p[2] == '<':
        op = 'INF'
    elif p[2] == '>=':
        op = 'GE'
    elif p[2] == '<=':
        op = 'LE'
    elif p[2] == '=':
        op = 'EQ'
    elif p[2] == '<>':
        op = 'NE'
    else:
        raise ValueError(f"Operador desconhecido: {p[2]}")

    p[0] = concat_safe(p[1], p[3], f"{op}\n")

# Regras para NOT
def p_expressao_condicional_not(p):
    '''expressao_condicional : NOT expressao_condicional'''
    p[0] = concat_safe(p[2], "NOT\n")

# Regras para expressões booleanas (com parênteses)
def p_expressao_condicional_paren(p):
    'expressao_condicional : LPAREN expressao_condicional RPAREN'
    p[0] = p[2] if p[2] is not None else ""  # Protege contra None


# Regras para comandos if           
def p_comando_if(p):
    '''comando_if : IF expressao_condicional THEN comando %prec IFX
                  | IF expressao_condicional THEN comando ELSE comando'''
    false_label = new_label()
    end_label = new_label()
    if len(p) == 5:
        # Para a expressão 'not (a > b) or (a = 5 and b = 10)', deve-se calcular o valor corretamente antes
        codigo = concat_safe(p[2], f"JZ {false_label}\n", p[4], f"{false_label}:\n")
    else:
        codigo = concat_safe(p[2], f"JZ {false_label}\n", p[4], f"JUMP {end_label}\n", f"{false_label}:\n", p[6], f"{end_label}:\n")
    p[0] = codigo


# Regras para o comando while
def p_comando_while(p):
    'comando_while : WHILE expressao_condicional DO comando'
    start_label = new_label()
    end_label = new_label()
    p[0] = f"{start_label}:\n{p[2]}JZ {end_label}\n{p[4]}JUMP {start_label}\n{end_label}:\n"

# Regras para o comando for
def p_comando_for(p):
    '''comando_for : FOR IDENTIFIER ASSIGN expressao_aritmetica TO expressao_aritmetica DO comando'''
    start_label = new_label()
    end_label = new_label()

    var_index = list(symbol_table.keys()).index(p[2])

    # Inicialização da variável de controlo
    init = p[4] + f"STOREG {var_index}\n"

    # Condição: se i > limite, termina
    cond = (
        f"{start_label}:\n"
        f"PUSHG {var_index}\n"
        + p[6] +
        "SUP\n"
        "NOT\n"
        f"JZ {end_label}\n"
    )

    # Corpo do ciclo + incremento
    corpo = (
        p[8] +
        f"PUSHG {var_index}\n"
        "PUSHI 1\n"
        "ADD\n"
        f"STOREG {var_index}\n"
        f"JUMP {start_label}\n"
        f"{end_label}:\n"
    )

    p[0] = init + cond + corpo


# Regras para o comando for com DOWNTO
def p_comando_for_downto(p):
    '''comando_for : FOR IDENTIFIER ASSIGN expressao_aritmetica DOWNTO expressao_aritmetica DO comando'''
    start_label = new_label()
    end_label = new_label()

    var_index = list(symbol_table.keys()).index(p[2])

    init = p[4] + f"STOREG {var_index}\n"

    cond = (f"{start_label}:\n" +
        f"PUSHG {var_index}\n" +
        p[6] +
        "INF\n" +  # i < limite inferior → termina
        f"JZ {end_label}\n")


    corpo = p[8]

    dec = (f"PUSHG {var_index}\n" +
       "PUSHI 1\n" +
       "SUB\n" +
       f"STOREG {var_index}\n" +
       f"JUMP {start_label}\n" +
       f"{end_label}:\n")


    p[0] = init + cond + corpo + dec


# Regras para o comando empty
def p_empty(p):
    'empty :'
    p[0] = ""

# Tratamento de erros
def p_error(p):
    print("Erro sintático no input!")
    if p:
        print(f"Erro próximo ao token: {p.value}")
    else:
        print("Erro inesperado no final do input.")

# Cria o parser
parser = yacc.yacc(debug=True, write_tables=False)
parser.trace = False

if __name__ == "__main__":
    try:
        entrada = sys.stdin.read()
        entrada = re.sub(r'\s{2,}', ' ', entrada)
        conversor = parser.parse(entrada)
        print("Resultado: \n", output)
    except Exception as e:
        print("Erro ao processar entrada:", e)
