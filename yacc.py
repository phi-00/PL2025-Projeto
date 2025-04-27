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
    ('left', 'MOD'),
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

def p_expressao_array(p):
    'expressao : IDENTIFIER LBRACKET expressao RBRACKET'
    nome_array = p[1]
    indice = p[3]

    if nome_array not in symbol_table:
        print(f"Erro: array '{nome_array}' não declarado")
        return

    base_addr = symbol_table[nome_array]['address']

    p[0] = {
        'code': f"PUSHI {base_addr}\n{indice['code']}ADD\nLOADN\n",
        'type': symbol_table[nome_array]['type']
    }


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
        var_list = p[1]
        tipo = p[3]
    else:
        var_list = p[2]
        tipo = p[4]

    for var in var_list:
        if isinstance(tipo, tuple) and tipo[0] == 'ARRAY':
            start_idx, end_idx = tipo[1], tipo[2]
            size = end_idx - start_idx + 1
            address = len(symbol_table)

            symbol_table[var] = {
                'type': 'ARRAY',
                'range': (start_idx, end_idx),
                'element_type': tipo[3],
                'address': address
            }

            for i in range(size):
                symbol_table[f"{var}[{i}]"] = {
                    'address': address + i,
                    'type': tipo[3]
                }


        else:
            if var not in symbol_table:
                address = len(symbol_table)
                symbol_table[var] = {
                    'address': address,
                    'type': tipo,
                    'value': None
                }
            else:
                print(f"Erro: Variável '{var}' já declarada.")

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
            | STRING
            | BOOLEAN
            | CHAR
            | array_tipo'''  # Refatorando para separar o array
    p[0] = p[1]

def p_array_tipo(p):
    'array_tipo : ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF tipo'
    p[0] = ('ARRAY', p[3], p[5], p[8])  # Salva o intervalo do array e o tipo de dado


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
    expressao = p[3] if p[3] is not None else ""

    if var_name in symbol_table:
        var_info = symbol_table[var_name]

        # Verifica se é um dicionário com chave 'address'
        if isinstance(var_info, dict) and 'address' in var_info:
            endereco = var_info['address']
        else:
            # Fallback: usar a posição da variável na tabela
            endereco = list(symbol_table.keys()).index(var_name)

        # Geração do código
        if var_info['type'] == 'CHAR':
            codigo = concat_safe(expressao, f"STOREG {endereco}\n")  # Para char
        else:
            codigo = concat_safe(expressao, f"STOREG {endereco}\n")

        # (Opcional) Atualiza o valor da variável, se for PUSHI ou PUSHS
        if isinstance(var_info, dict):
            valor = None
            if expressao.startswith("PUSHS"):
                valor = expressao.split('"')[1]
            elif expressao.startswith("PUSHI"):
                valor = int(expressao.split()[1])
            var_info['value'] = valor
            symbol_table[var_name] = var_info

        p[0] = codigo
    else:
        print(f"Erro: Variável '{var_name}' não declarada.")
        p[0] = ""

# Regras para atribuição de array
def p_atribuicao_array(p):
    'atribuicao : IDENTIFIER LBRACKET expressao_aritmetica RBRACKET ASSIGN expressao_aritmetica SEMICOLON'
    var = p[1]
    index_code = p[3]
    value_code = p[6]
    
    # Verifica se a variável é um array
    if var in symbol_table and symbol_table[var]['type'] == 'ARRAY':
        var_info = symbol_table[var]
        start = var_info['range'][0]
        end = var_info['range'][1]
        
        # Verifica se o índice está dentro do intervalo válido
        erro_label = new_label()
        fim_label = new_label()
        check_index_code = concat_safe(index_code,
                               f"PUSHI {start}\nLT\nJZ {erro_label}\n",
                               index_code,
                               f"PUSHI {end}\nGT\nJZ {erro_label}\n",
                               f"JUMP {fim_label}\n",
                               f"{erro_label}:\nPUSHS \"Index out of bounds\"\nWRITES\n",
                               f"{fim_label}:\n")

        
        # Cálculo do endereço do índice
        offset_code = concat_safe(index_code, f"PUSHI {start}\nSUB\n")
        calc_addr = concat_safe(offset_code, f"PUSHI {var_info['address']}\nADD\n")
        
        # Gerar código de armazenamento
        store_code = concat_safe(value_code, calc_addr, "STOREN\n")
        
        # Junta as instruções
        p[0] = concat_safe(check_index_code, store_code)
    else:
        print(f"Erro: '{var}' não é um array declarado.")
        p[0] = ""


# Regras para expressões aritméticas
def p_expressao_aritmetica(p):
    '''expressao_aritmetica : expressao_aritmetica PLUS termo
                            | expressao_aritmetica MINUS termo
                            | expressao_aritmetica TIMES termo
                            | expressao_aritmetica DIVIDE termo
                            | expressao_aritmetica INTDIV termo
                            | expressao_aritmetica MOD termo  
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
            p[0] = concat_safe(p[1], p[3], "DIV\n")  # Divisão normal
        elif operador.lower() == 'div' or operador == 'DIV':
            p[0] = concat_safe(p[1], p[3], "IDIV\n")  # Divisão inteira
        elif operador.lower() == 'mod' or operador == 'MOD':  # Para MOD
            p[0] = concat_safe(p[1], p[3], "MOD\n")   # Geração de código para MOD

# Regras para termos
def p_termo(p):
    '''termo : LPAREN expressao_aritmetica RPAREN
             | NUMBER
             | IDENTIFIER
             | TEXT
             | TRUE
             | FALSE'''
    if len(p) == 2:
        if p.slice[1].type == 'NUMBER':
            p[0] = f"PUSHI {p[1]}\n"
        elif p.slice[1].type == 'TRUE':
            p[0] = "PUSHI 1\n"
        elif p.slice[1].type == 'FALSE':
            p[0] = "PUSHI 0\n"
        elif p.slice[1].type == 'TEXT':
            p[0] = f'PUSHS "{p[1][1:-1]}"\n'
        elif p.slice[1].type == 'IDENTIFIER':
            var = p[1]
            if var in symbol_table:
                addr = symbol_table[var]['address']
                p[0] = f"PUSHG {addr}\n"
            else:
                print(f"Erro: variável '{var}' não declarada.")
                p[0] = ""
    elif len(p) == 4:
        p[0] = p[2]  # Para parênteses (expressão)

def p_termo_array(p):
    '''termo : IDENTIFIER LBRACKET expressao_aritmetica RBRACKET'''
    var = p[1]
    index_code = p[3]
    if var in symbol_table and symbol_table[var]['type'] == 'ARRAY':
        var_info = symbol_table[var]
        start = var_info['range'][0]
        base_addr = var_info['address']
        offset_code = concat_safe(index_code, f"PUSHI {start}\nSUB\n")
        full_code = concat_safe(offset_code, f"PUSHI {base_addr}\nADD\nLOADN\n")
        p[0] = full_code
    else:
        print(f"Erro: '{var}' não é um array declarado.")
        p[0] = ""

# Regras para writeln
def p_writeln(p):
    'write : WRITELN LPAREN argumentos RPAREN SEMICOLON'
    codigo = ""
    for arg in p[3]:
        if isinstance(arg, str) and (arg.startswith("'") or arg.startswith('"')):
            # Constante string
            codigo += f'PUSHS "{arg[1:-1]}"\nWRITES\n'
        
        elif isinstance(arg, tuple) and arg[0] == 'array':  # Verifica se o argumento é um array
            nome_array = arg[1]  # Nome do array
            indice = arg[2]  # Índice do array
            
            if nome_array in symbol_table:
                tipo = symbol_table[nome_array]['type']
                addr = symbol_table[nome_array]['address']
                
                # Carrega o endereço base do array
                codigo += f"PUSHG {addr}\n"
                
                # Carrega o índice do array
                codigo += f"{indice['code']}"  # Corrigido para garantir o cálculo do índice
                
                # Soma o índice ao endereço base do array
                codigo += "ADD\n"
                
                # A partir daqui, o código será semelhante a como tratamos variáveis
                if tipo == 'BOOLEAN':
                    label_false = new_label()
                    label_end = new_label()
                    codigo += f"JZ {label_false}\n"
                    codigo += f'PUSHS "true"\nWRITES\n'
                    codigo += f"JUMP {label_end}\n"
                    codigo += f"LABEL {label_false}\n"
                    codigo += f'PUSHS "false"\nWRITES\n'
                    codigo += f"LABEL {label_end}\n"
                elif tipo == 'CHAR':
                    # Para char, imprimir o valor do caractere
                    codigo += f"WRITEI\n"  # Escreve o caractere
                else:
                    codigo += f"WRITEI\n"  # Escreve o valor genérico
        elif arg in symbol_table:
            tipo = symbol_table[arg]['type']
            addr = symbol_table[arg]['address']
            if tipo == 'BOOLEAN':
                label_false = new_label()
                label_end = new_label()
                codigo += f"PUSHG {addr}\n"
                codigo += f"JZ {label_false}\n"
                codigo += f'PUSHS "true"\nWRITES\n'
                codigo += f"JUMP {label_end}\n"
                codigo += f"LABEL {label_false}\n"
                codigo += f'PUSHS "false"\nWRITES\n'
                codigo += f"LABEL {label_end}\n"
            else:
                codigo += f"PUSHG {addr}\nWRITEI\n"

    p[0] = codigo


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
            if symbol_table[arg]['type'] == 'CHAR':
                codigo += f"READC\nSTOREG {var_index}\n"  # Para char
            else:
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
        print(f"Erro próximo ao token: {p.value} na linha: {p.lineno}")
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
