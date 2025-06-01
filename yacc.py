from lex import tokens, lexer, re
import ply.yacc as yacc
import sys

output = ""  # Variável global para armazenar o código gerado
symbol_table = {}  # Tabela de símbolos para armazenar variáveis e seus valores
label_count = 0
next_free_address = 0

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('right', 'NOT'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'INTDIV', 'MOD'),
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
        var_list = p[1]
        tipo = p[3].upper() if isinstance(p[3], str) else p[3]
    else:
        var_list = p[2]
        tipo = p[4].upper() if isinstance(p[4], str) else p[4]

    for var in var_list:
        if var in symbol_table:
            print(f"[INFO] Variável '{var}' já declarada — ignorada.")
            continue
        
        addr = len(symbol_table)
    
        if isinstance(tipo, tuple) and tipo[0] == 'ARRAY':
            lower_bound = tipo[1]
            upper_bound = tipo[2]
            element_type = tipo[3]
    
            symbol_table[var] = {
                'address': addr,
                'type': 'ARRAY',
                'range': (lower_bound, upper_bound),
                'element_type': element_type,
                'value': None
            }
        else:
            symbol_table[var] = {
                'address': addr,
                'type': tipo,
                'value': None
            }



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
                      | lista_comandos SEMICOLON comando
                      | lista_comandos SEMICOLON'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]  # ignora o ; final
    else:
        p[0] = concat_safe(p[1], p[3])


# Regras para comandos
def p_comando(p):
    '''comando : comando_simples
               | comando_composto'''
    p[0] = p[1] if p[1] is not None else ""

# Regras para comandos simples (atribuição, write, if, while)
def p_comando_simples(p):
    '''comando_simples : atribuicao
                       | write
                       | writeln
                       | read
                       | comando_if
                       | comando_while
                       | comando_for'''
    p[0] = p[1]


# Regras para comandos compostos (bloco)
def p_comando_composto(p):
    '''comando_composto : bloco'''
    p[0] = p[1] if p[1] is not None else ""

# Regras para atribuição
def p_atribuicao(p):
    'atribuicao : IDENTIFIER ASSIGN expressao_aritmetica'
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
    'atribuicao : IDENTIFIER LBRACKET expressao_aritmetica RBRACKET ASSIGN expressao_aritmetica'

    global next_free_address

    nome_array = p[1]
    index_code = p[3]
    value_code = p[6]

    if nome_array not in symbol_table:
        raise Exception(f"Array '{nome_array}' não declarado.")

    array_info = symbol_table[nome_array]
    addr = array_info['address']
    start = array_info['range'][0]
    end = array_info['range'][1]

    import re
    # Se índice é constante, atribui direto com STOREG
    match = re.match(r'PUSHI (\d+)', index_code.strip())
    if match:
        idx_val = int(match.group(1))
        if idx_val < start or idx_val > end:
            raise Exception(f"Índice {idx_val} fora dos limites.")
        desloc = idx_val - start
        endereco_final = addr + desloc
        p[0] = value_code + f"STOREG {endereco_final}\n"
        return

    # Índice variável: guarda índice numa variável temporária
    temp_idx_var = f"__temp_idx_{new_label()}"
    temp_idx_addr = next_free_address
    symbol_table[temp_idx_var] = {
        'address': temp_idx_addr,
        'type': 'INTEGER',
        'value': None
    }
    next_free_address += 1

    index_store = index_code + f"STOREG {temp_idx_addr}\n"

    # Verificação de limites
    bounds_fail_label = new_label()
    bounds_ok_label = new_label()

    bounds_check = (
        f"PUSHG {temp_idx_addr}\nPUSHI {start}\nINF\n"
        f"JZ {bounds_fail_label}\n"
        f"PUSHG {temp_idx_addr}\nPUSHI {end}\nSUP\n"
        f"JZ {bounds_fail_label}\n"
        f"JUMP {bounds_ok_label}\n"
        f"{bounds_fail_label}:\n"
        f'PUSHS "Index out of bounds"\nWRITES\n'
        f"{bounds_ok_label}:\n"
    )

    # Gerar cascata IF para cada posição do array
    if_chain = ""
    for i in range(start, end + 1):
        label_true = new_label()
        label_next = new_label()
        deslocamento = i - start
        endereco_real = addr + deslocamento

    if_chain += (
        f"PUSHG {temp_idx_addr}\n"
        f"PUSHI {i}\n"
        "SUB\n"
        f"JZ {label_true}\n"
        f"JUMP {label_next}\n"
        f"{label_true}:\n"
        + value_code +
        f"STOREG {endereco_real}\n"
        f"{label_next}:\n"
    )

    p[0] = index_store + bounds_check + if_chain

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
            p[0] = concat_safe(p[1], p[3], "DIV\n")  # Divisão inteira
        elif operador.lower() == 'mod' or operador == 'MOD':  # Para MOD
            p[0] = concat_safe(p[1], p[3], "MOD\n")   # Geração de código para MOD

# Regras para termos
def p_termo(p):
    '''termo : LPAREN expressao_aritmetica RPAREN
             | NUMBER
             | IDENTIFIER
             | TEXT
             | TRUE
             | FALSE
             | LENGTH LPAREN IDENTIFIER RPAREN'''
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
        p[0] = p[2]  # Expressão entre parênteses
    elif len(p) == 5 and p.slice[1].type == 'LENGTH':
        var = p[3]
        if var in symbol_table:
            tipo = symbol_table[var]['type']
            addr = symbol_table[var]['address']
            if tipo.upper() != 'STRING':
                raise Exception(f"Função length só pode ser usada com strings. '{var}' é do tipo {tipo}.")
            p[0] = f"PUSHG {addr}\nSTRLEN\n"
        else:
            raise Exception(f"Variável '{var}' não declarada.")

def p_termo_array(p):
    '''termo : IDENTIFIER LBRACKET expressao_aritmetica RBRACKET'''
    var = p[1]
    index_code = p[3]

    if var not in symbol_table:
        print(f"Erro: variável '{var}' não declarada.")
        p[0] = ""
        return

    var_info = symbol_table[var]
    tipo = var_info['type']

    # Se for uma STRING, trata como array de CHAR
    if tipo == 'STRING':
        addr = var_info['address']
        code = concat_safe(index_code, f"PUSHI {addr}\nADD\nLOADN\n")
        p[0] = code
        return

    # Se for ARRAY declarado
    if isinstance(var_info, dict) and tipo == 'ARRAY':
        start = var_info['range'][0]
        base_addr = var_info['address']
        offset_code = concat_safe(index_code, f"PUSHI {start}\nSUB\n")
        full_code = concat_safe(offset_code, f"PUSHI {base_addr}\nADD\nLOADN\n")
        p[0] = full_code
        return

    print(f"Erro: '{var}' não é um array nem uma string indexável.")
    p[0] = ""


# Regras para writeln
def p_writeln(p):
    'writeln : WRITELN LPAREN argumentos RPAREN'
    codigo = ""
    for arg in p[3]:
        if isinstance(arg, str) and (arg.startswith("'") or arg.startswith('"')):
            codigo += f'PUSHS "{arg[1:-1]}"\nWRITES\n'

        elif isinstance(arg, str) and arg in symbol_table:
            var_info = symbol_table[arg]
            tipo = var_info['type']
            addr = var_info['address']
            tipo = tipo.upper()

            if tipo == 'BOOLEAN':
                label_false = new_label()
                label_end = new_label()
                codigo += f"PUSHG {addr}\n"
                codigo += f"JZ {label_false}\n"
                codigo += f'PUSHS "true"\nWRITES\n'
                codigo += f"JUMP {label_end}\n"
                codigo += f"{label_false}:\n"
                codigo += f'PUSHS "false"\nWRITES\n'
                codigo += f"{label_end}:\n"
            elif tipo == 'CHAR':
                codigo += f"PUSHG {addr}\nWRITEI\n"
            elif tipo == 'STRING':
                codigo += f"PUSHG {addr}\nWRITES\n"
            else:
                codigo += f"PUSHG {addr}\nWRITEI\n"

        elif isinstance(arg, tuple) and arg[0] == 'array':
            nome_array = arg[1]
            indice = arg[2]

            if nome_array in symbol_table:
                array_info = symbol_table[nome_array]
                tipo = array_info['element_type']
                base_addr = array_info['address']

                codigo += f"PUSHI {base_addr}\n"
                codigo += indice['code']
                codigo += "ADD\n"
                codigo += "LOADN\n"

                tipo = tipo.upper()
                if tipo == 'BOOLEAN':
                    label_false = new_label()
                    label_end = new_label()
                    codigo += f"JZ {label_false}\n"
                    codigo += f'PUSHS "true"\nWRITES\n'
                    codigo += f"JUMP {label_end}\n"
                    codigo += f"{label_false}:\n"
                    codigo += f'PUSHS "false"\nWRITES\n'
                    codigo += f"{label_end}:\n"
                elif tipo == 'CHAR':
                    codigo += "WRITEI\n"
                elif tipo == 'STRING':
                    codigo += "WRITES\n"
                else:
                    codigo += "WRITEI\n"
            else:
                print(f"Erro: Array '{nome_array}' não declarado.")
        else:
            print(f"Erro: Argumento inválido em writeln: {arg}")

    p[0] = codigo

# Regras para write
def p_write(p):
    'write : WRITE LPAREN argumentos RPAREN'
    codigo = ""
    for arg in p[3]:
        if isinstance(arg, str) and (arg.startswith("'") or arg.startswith('"')):
            # Constante string
            codigo += f'PUSHS "{arg[1:-1]}"\nWRITES\n'

        elif isinstance(arg, str) and arg in symbol_table:
            var_info = symbol_table[arg]
            tipo = var_info['type']
            addr = var_info['address']
            tipo = tipo.upper()

            if tipo == 'BOOLEAN':
                label_false = new_label()
                label_end = new_label()
                codigo += f"PUSHG {addr}\n"
                codigo += f"JZ {label_false}\n"
                codigo += f'PUSHS "true"\nWRITES\n'
                codigo += f"JUMP {label_end}\n"
                codigo += f"{label_false}:\n"
                codigo += f'PUSHS "false"\nWRITES\n'
                codigo += f"{label_end}:\n"
            elif tipo == 'CHAR':
                codigo += f"PUSHG {addr}\nWRITEI\n"
            elif tipo == 'STRING':
                codigo += f"PUSHG {addr}\nWRITES\n"
            else:
                codigo += f"PUSHG {addr}\nWRITEI\n"

        elif isinstance(arg, tuple) and arg[0] == 'array':
            nome_array = arg[1]
            indice = arg[2]

            if nome_array in symbol_table:
                array_info = symbol_table[nome_array]
                tipo = array_info['element_type']
                base_addr = array_info['address']

                codigo += f"PUSHI {base_addr}\n"
                codigo += indice['code']
                codigo += "ADD\n"
                codigo += "LOADN\n"

                tipo = tipo.upper()
                if tipo == 'BOOLEAN':
                    label_false = new_label()
                    label_end = new_label()
                    codigo += f"JZ {label_false}\n"
                    codigo += f'PUSHS "true"\nWRITES\n'
                    codigo += f"JUMP {label_end}\n"
                    codigo += f"{label_false}:\n"
                    codigo += f'PUSHS "false"\nWRITES\n'
                    codigo += f"{label_end}:\n"
                elif tipo == 'CHAR':
                    codigo += "WRITEI\n"
                elif tipo == 'STRING':
                    codigo += "WRITES\n"
                else:
                    codigo += "WRITEI\n"
            else:
                print(f"Erro: Array '{nome_array}' não declarado.")
        else:
            print(f"Erro: Argumento inválido em write: {arg}")

    p[0] = codigo if codigo else ""

# Regras para readln
def p_readln(p):
    'read : READLN LPAREN argumentos RPAREN'
    codigo = ""
    for arg in p[3]:
        if isinstance(arg, str) and arg in symbol_table:
            var_info = symbol_table[arg]
            addr = var_info['address']
            tipo = var_info['type']

            if tipo == 'CHAR':
                codigo += f"READC\nSTOREG {addr}\n"
            elif tipo == 'STRING':
                codigo += f"READ\nSTOREG {addr}\n"
            else:
                codigo += f"READ\nATOI\nSTOREG {addr}\n"  # ← converte string lida em inteiro

        elif isinstance(arg, tuple) and arg[0] == 'array':
            nome_array = arg[1]
            indice = arg[2]  # {'code': código da expressão índice}

            if nome_array in symbol_table:
                array_info = symbol_table[nome_array]
                tipo = array_info['element_type']
                base_addr = array_info['address']

                # Gera o código para calcular o endereço final do elemento do array
                codigo += f"PUSHI {base_addr}\n"
                codigo += indice['code']
                codigo += "ADD\n"

                if tipo.upper() == 'CHAR':
                    codigo += "READC\nSTOREN\n"
                else:
                    codigo += "READ\nSTOREN\n"
            else:
                print(f"Erro: Array '{nome_array}' não declarado.")
        else:
            print(f"Erro: argumento inválido em readln: {arg}")

    p[0] = codigo if codigo else ""


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
                 | IDENTIFIER
                 | IDENTIFIER LBRACKET expressao_aritmetica RBRACKET'''
    if len(p) == 2:
        p[0] = p[1] if p[1] is not None else ""
    else:
        var = p[1]
        index_code = p[3]  # expressao_aritmetica retorna uma string com código

        if var in symbol_table and symbol_table[var]['type'] == 'ARRAY':
            p[0] = ('array', var, {'code': index_code})
        else:
            raise Exception(f"'{var}' não é um array declarado.")


# Regras para expressões condicionais lógicas (AND / OR)
def p_expressao_condicional_logica(p):
    '''expressao_condicional : expressao_condicional AND expressao_condicional
                             | expressao_condicional OR expressao_condicional'''
    left = p[1] if p[1] is not None else ""
    right = p[3] if p[3] is not None else ""

    if p[2] == 'AND':
        false_label = new_label()
        end_label = new_label()
        p[0] = (
            concat_safe(left, f"JZ {false_label}\n") +
            right + f"JZ {false_label}\n" +
            "PUSHI 1\n" +
            f"JUMP {end_label}\n" +
            f"{false_label}:\nPUSHI 0\n" +
            f"{end_label}:\n"
        )

    elif p[2] == 'OR':
        true_label = new_label()
        end_label = new_label()
        p[0] = (
            concat_safe(left, f"JNZ {true_label}\n") +
            right + f"JNZ {true_label}\n" +
            "PUSHI 0\n" +
            f"JUMP {end_label}\n" +
            f"{true_label}:\nPUSHI 1\n" +
            f"{end_label}:\n"
        )



# Regras para expressões condicionais
def p_expressao_condicional(p):
    '''expressao_condicional : expressao_aritmetica GT expressao_aritmetica
                             | expressao_aritmetica LT expressao_aritmetica
                             | expressao_aritmetica GE expressao_aritmetica
                             | expressao_aritmetica LE expressao_aritmetica
                             | expressao_aritmetica EQ expressao_aritmetica
                             | expressao_aritmetica NE expressao_aritmetica'''
    op = p[2]
    code_left = p[1] if p[1] is not None else ""
    code_right = p[3] if p[3] is not None else ""

    print("[DEBUG COMPARACAO]", repr(code_left), repr(code_right), op)
    print("[DEBUG COND]", [s.type for s in p.slice], p[1:] if len(p) > 1 else "-none-")


    if op == '>':
        p[0] = concat_safe(code_left, code_right, "SUP\n")
    elif op == '<':
        p[0] = concat_safe(code_left, code_right, "INF\n")
    elif op == '>=':
        label_true = new_label()
        label_end = new_label()
        p[0] = (
            concat_safe(code_left, code_right) +
            "INF\n" +
            f"JZ {label_true}\n" +
            "PUSHI 0\n" +
            f"JUMP {label_end}\n" +
            f"{label_true}:\n" +
            "PUSHI 1\n" +
            f"{label_end}:\n"
        )
    elif op == '<=':
        label_true = new_label()
        label_end = new_label()
        p[0] = (
            concat_safe(code_left, code_right) +
            "SUP\n" +
            f"JZ {label_true}\n" +
            "PUSHI 0\n" +
            f"JUMP {label_end}\n" +
            f"{label_true}:\n" +
            "PUSHI 1\n" +
            f"{label_end}:\n"
        )
    elif op == '=':
        label_true = new_label()
        label_end = new_label()
        p[0] = (
            concat_safe(code_left, code_right) +
            "SUB\n" +
            f"JZ {label_true}\n" +
            "PUSHI 0\n" +
            f"JUMP {label_end}\n" +
            f"{label_true}:\n" +
            "PUSHI 1\n" +
            f"{label_end}:\n"
        )
    elif op == '<>':
        label_false = new_label()
        label_end = new_label()
        p[0] = (
            concat_safe(code_left, code_right) +
            "SUB\n" +
            f"JZ {label_false}\n" +
            "PUSHI 1\n" +
            f"JUMP {label_end}\n" +
            f"{label_false}:\n" +
            "PUSHI 0\n" +
            f"{label_end}:\n"
        )

        # DEBUG: print symbol_table contents
        print("[DEBUG symbol_table]", symbol_table)


# Regras para NOT
def p_expressao_condicional_not(p):
    '''expressao_condicional : NOT expressao_condicional'''
    cond = p[2] if p[2] is not None else ""
    p[0] = concat_safe(p[2], "NOT\n")

# Regras para expressões booleanas (com parênteses)
def p_expressao_condicional_paren(p):
    'expressao_condicional : LPAREN expressao_condicional RPAREN'
    p[0] = p[2] if p[2] is not None else ""  # Protege contra None

def p_expressao_condicional_bool_expr(p):
    'expressao_condicional : expressao_aritmetica'
    p[0] = p[1] if p[1] is not None else ""

def p_comando_if_then(p):
    'comando_if : IF expressao_condicional THEN comando %prec IFX'
    cond = p[2]
    then_code = p[4]
    false_label = new_label()
    p[0] = concat_safe(cond, f"JZ {false_label}\n", then_code, f"{false_label}:\n")

def p_comando_if_then_else(p):
    'comando_if : IF expressao_condicional THEN comando ELSE comando'
    cond = p[2]
    then_code = p[4]
    else_code = p[6]
    false_label = new_label()
    end_label = new_label()
    p[0] = concat_safe(cond, f"JZ {false_label}\n", then_code, f"JUMP {end_label}\n", f"{false_label}:\n", else_code, f"{end_label}:\n")

# Regras para o comando while
def p_comando_while(p):
    'comando_while : WHILE expressao_condicional DO comando'
    start_label = new_label()
    end_label = new_label()
    cond = p[2] if p[2] is not None else ""
    p[0] = f"{start_label}:\n{cond}JZ {end_label}\n{p[4]}JUMP {start_label}\n{end_label}:\n"


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
    cond_label = new_label()
    end_label = new_label()

    var_index = list(symbol_table.keys()).index(p[2])

    # Inicialização de i := valor inicial
    init = p[4] + f"STOREG {var_index}\n"

    # Condição: se i < limite → salta para o fim
    cond = (
        f"{cond_label}:\n"
        f"PUSHG {var_index}\n" +
        p[6] +
        "INF\n" +
        f"JZ {start_label}\n" +  # se NÃO for menor → executa
        f"JUMP {end_label}\n"    # senão, termina
    )

    # Corpo e decremento
    corpo = (
        f"{start_label}:\n" +
        p[8] +
        f"PUSHG {var_index}\n"
        "PUSHI 1\n"
        "SUB\n"
        f"STOREG {var_index}\n"
        f"JUMP {cond_label}\n"
        f"{end_label}:\n"
    )

    p[0] = init + cond + corpo

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
        with open(sys.argv[1], 'r') as f:
            entrada = f.read()
        entrada = re.sub(r'\s{2,}', ' ', entrada)
        conversor = parser.parse(entrada)
        print("Resultado: \n", output)
    except Exception as e:
        print("Erro ao processar entrada:", e)
