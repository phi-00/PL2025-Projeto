import ply.yacc as yacc
import sys
from lex import tokens, lexer, re

# Variable to store the compiled VM code
output = ""
# Symbol table to track variables
symbol_table = {}
# Variable to track array declarations
array_table = {}
# Track if the compilation was successful
success = True
# Labels counter for control structures
label_counter = 0

precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'NE'),
    ('left', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ASSIGN')
)

# Starting rule
def p_z(p):
    'z : programa'
    global output
    p[0] = p[1]

# Program structure
def p_programa(p):
    '''programa : declaracao_programa declaracao_var declaracao_end_begin
                | declaracao_programa declaracao_end_begin'''
    if len(p) == 4:
        p[0] = f"{p[1]}\n{p[2]}\n{p[3]}"
    else:
        p[0] = f"{p[1]}\n{p[2]}"

def p_declaracao_programa(p):
    'declaracao_programa : PROGRAM IDENTIFIER SEMICOLON'
    global output
    output += f"# Program {p[2]}\n"
    p[0] = p[2]

def p_declaracao_end_begin(p):
    'declaracao_end_begin : BEGIN operacoes END DOT'
    global output
    output += "# Begin main program\n"
    output += p[2]
    output += "STOP\n"
    p[0] = output

# Variable declarations
def p_declaracao_var(p):
    'declaracao_var : VAR declaracoes'
    global output
    output += "# Variable declarations\n"
    p[0] = p[2]

def p_declaracoes_1(p):
    'declaracoes : declaracao declaracoes'
    p[0] = f"{p[1]}{p[2]}"

def p_declaracoes_2(p):
    'declaracoes : declaracao'
    p[0] = p[1]

def p_declaracao_1(p):
    'declaracao : variaveis COLON tipo SEMICOLON'
    global symbol_table, output
    var_type = p[3]
    for var in p[1]:
        if var not in symbol_table:
            symbol_table[var] = {'type': var_type, 'index': len(symbol_table)}
            output += f"PUSHI 0 # Initialize {var} ({var_type})\n"
        else:
            print(f"Error: Variable '{var}' already declared")
            global success
            success = False
    p[0] = ""

def p_declaracao_2(p):
    'declaracao : variaveis COLON ARRAY LBRACKET NUMBER DOT DOT NUMBER RBRACKET OF tipo SEMICOLON'
    global array_table, symbol_table, output
    var_type = p[11]
    start_idx = int(p[5])
    end_idx = int(p[8])
    size = end_idx - start_idx + 1
    
    for var in p[1]:
        if var not in symbol_table:
            array_table[var] = {'type': var_type, 'start': start_idx, 'end': end_idx, 'size': size}
            symbol_table[var] = {'type': 'ARRAY', 'index': len(symbol_table), 'elem_type': var_type}
            # Initialize array with zeros
            for i in range(size):
                output += f"PUSHI 0 # Initialize {var}[{start_idx+i}] ({var_type})\n"
        else:
            print(f"Error: Variable '{var}' already declared")
            global success
            success = False
    p[0] = ""

def p_variaveis_1(p):
    'variaveis : IDENTIFIER'
    p[0] = [p[1]]

def p_variaveis_2(p):
    'variaveis : IDENTIFIER COMMA variaveis'
    p[0] = [p[1]] + p[3]

def p_tipo(p):
    '''tipo : INTEGER
            | REAL
            | BOOLEAN
            | STRING
            | CHAR'''
    p[0] = p[1]

# Operations
def p_operacoes_1(p):
    'operacoes : operacao operacoes'
    p[0] = f"{p[1]}{p[2]}"

def p_operacoes_2(p):
    'operacoes : operacao'
    p[0] = p[1]

def p_operacao(p):
    '''operacao : atribuicao
                | instrucao'''
    p[0] = p[1]

def p_atribuicao(p):
    'atribuicao : IDENTIFIER ASSIGN expressao SEMICOLON'
    global output, symbol_table
    if p[1] in symbol_table:
        var_idx = symbol_table[p[1]]['index']
        output_code = f"{p[3]}STOREG {var_idx} # Store in {p[1]}\n"
    else:
        print(f"Error: Variable '{p[1]}' not declared")
        global success
        success = False
        output_code = f"# Error: Variable '{p[1]}' not declared\n"
    p[0] = output_code

def p_expressao_NUMBER(p):
    'expressao : NUMBER'
    p[0] = f"PUSHI {p[1]}\n"

def p_expressao_identifier(p):
    'expressao : IDENTIFIER'
    global symbol_table
    if p[1] in symbol_table:
        var_idx = symbol_table[p[1]]['index']
        p[0] = f"PUSHG {var_idx} # Push {p[1]}\n"
    else:
        print(f"Error: Variable '{p[1]}' not declared")
        global success
        success = False
        p[0] = f"# Error: Variable '{p[1]}' not declared\n"

def p_expressao_plus(p):
    'expressao : expressao PLUS expressao'
    p[0] = f"{p[1]}{p[3]}ADD\n"

def p_expressao_minus(p):
    'expressao : expressao MINUS expressao'
    p[0] = f"{p[1]}{p[3]}SUB\n"

def p_expressao_times(p):
    'expressao : expressao TIMES expressao'
    p[0] = f"{p[1]}{p[3]}MUL\n"

def p_expressao_divide(p):
    'expressao : expressao DIVIDE expressao'
    p[0] = f"{p[1]}{p[3]}DIV\n"

# Instructions
def p_instrucao(p):
    '''instrucao : inst_readln
                 | inst_writeln
                 | inst_write
                 | inst_if
                 | inst_while
                 | inst_for'''
    p[0] = p[1]

def p_inst_readln(p):
    'inst_readln : READLN LPAREN IDENTIFIER RPAREN SEMICOLON'
    global output, symbol_table
    if p[3] in symbol_table:
        var_idx = symbol_table[p[3]]['index']
        var_type = symbol_table[p[3]]['type']
        if var_type == 'INTEGER':
            p[0] = f"READ\nATOI\nSTOREG {var_idx} # Read into {p[3]}\n"
        elif var_type == 'REAL':
            p[0] = f"READ\nATOF\nSTOREG {var_idx} # Read into {p[3]}\n"
        else:
            p[0] = f"READ\nSTOREG {var_idx} # Read into {p[3]}\n"
    else:
        print(f"Error: Variable '{p[3]}' not declared")
        global success
        success = False
        p[0] = f"# Error: Variable '{p[3]}' not declared\n"

def p_inst_writeln(p):
    'inst_writeln : WRITELN LPAREN texto_imprimir RPAREN SEMICOLON'
    p[0] = f"{p[3]}PUSHS \"\\n\"\nWRITES\n"


def p_inst_write(p):
    'inst_write : WRITE LPAREN texto_imprimir RPAREN SEMICOLON'
    p[0] = p[3]


def p_texto_imprimir_1(p):
    'texto_imprimir : TEXT'
    text = p[1][1:-1]  # Remove surrounding quotes
    p[0] = f"PUSHS \"{text}\"\nWRITES\n"

def p_texto_imprimir_2(p):
    'texto_imprimir : IDENTIFIER'
    global symbol_table
    if p[1] in symbol_table:
        var_idx = symbol_table[p[1]]['index']
        var_type = symbol_table[p[1]]['type']
        if var_type == 'INTEGER' or var_type == 'REAL':
            p[0] = f"PUSHG {var_idx}\nWRITEI\n"
        else:
            p[0] = f"PUSHG {var_idx}\nWRITES\n"
    else:
        print(f"Error: Variable '{p[1]}' not declared")
        global success
        success = False
        p[0] = f"# Error: Variable '{p[1]}' not declared\n"

def p_texto_imprimir_3(p):
    'texto_imprimir : TEXT COMMA texto_imprimir'
    text = p[1][1:-1]  # Remove surrounding quotes
    p[0] = f"PUSHS \"{text}\"\nWRITES\n{p[3]}"

def p_texto_imprimir_4(p):
    'texto_imprimir : IDENTIFIER COMMA texto_imprimir'
    global symbol_table
    if p[1] in symbol_table:
        var_idx = symbol_table[p[1]]['index']
        var_type = symbol_table[p[1]]['type']
        if var_type == 'INTEGER' or var_type == 'REAL':
            p[0] = f"PUSHG {var_idx}\nWRITEI\n{p[3]}"
        else:
            p[0] = f"PUSHG {var_idx}\nWRITES\n{p[3]}"
    else:
        print(f"Error: Variable '{p[1]}' not declared")
        global success
        success = False
        p[0] = f"# Error: Variable '{p[1]}' not declared\n{p[3]}"

# Control Structures

def p_inst_if(p):
    'inst_if : IF condicoes THEN corpo_ciclo else'
    p[0] = p[2] + p[5] + p[4]

def p_else_empty(p):
    'else :'
    global label_counter
    label = label_counter
    label_counter += 1
    p[0] = f"JZ endif_{label}\n"

def p_else_else(p):
    'else : ELSE corpo_ciclo'
    global label_counter
    label = label_counter
    label_counter += 1
    p[0] = f"JZ else_{label}\nJUMP endif_{label}\nelse_{label}:\n{p[2]}endif_{label}:\n"

def p_condicoes_1(p):
    'condicoes : condicao'
    p[0] = p[1]

def p_condicoes_2(p):
    'condicoes : LPAREN condicoes RPAREN AND LPAREN condicoes RPAREN'
    p[0] = f"{p[2]}{p[6]}AND\n"

def p_condicoes_3(p):
    'condicoes : LPAREN condicoes RPAREN OR LPAREN condicoes RPAREN'
    p[0] = f"{p[2]}{p[6]}OR\n"

def p_condicoes_4(p):
    'condicoes : NOT LPAREN condicoes RPAREN'
    p[0] = f"{p[3]}NOT\n"

def p_condicao(p):
    'condicao : expressao compara expressao'
    p[0] = f"{p[1]}{p[3]}{p[2]}"

def p_compara_lt(p):
    'compara : LT'
    p[0] = "INF\n"

def p_compara_gt(p):
    'compara : GT'
    p[0] = "SUP\n"

def p_compara_le(p):
    'compara : LE'
    p[0] = "INFEQ\n"

def p_compara_ge(p):
    'compara : GE'
    p[0] = "SUPEQ\n"

def p_compara_eq(p):
    'compara : EQ'
    p[0] = "EQUAL\n"

def p_compara_ne(p):
    'compara : NE'
    p[0] = "EQUAL\nNOT\n"

def p_inst_while(p):
    'inst_while : WHILE condicoes DO corpo_ciclo'
    global label_counter
    start_label = f"while_{label_counter}"
    end_label = f"end_while_{label_counter}"
    label_counter += 1
    
    p[0] = f"{start_label}:\n{p[2]}JZ {end_label}\n{p[4]}JUMP {start_label}\n{end_label}:\n"

def p_inst_for_to(p):
    'inst_for : FOR IDENTIFIER ASSIGN NUMBER TO NUMBER DO corpo_ciclo'
    global label_counter, symbol_table, output
    start_val = p[4]
    end_val = p[6]
    var = p[2]

    if var not in symbol_table:
        symbol_table[var] = {'type': 'INTEGER', 'index': len(symbol_table)}
        output += f"PUSHI 0 # Initialize loop variable {var}\n"

    idx = symbol_table[var]['index']
    start_label = f"for_{label_counter}"
    end_label = f"end_for_{label_counter}"
    label_counter += 1

    p[0] = f"PUSHI {start_val}\nSTOREG {idx} # {var} = {start_val}\n" \
           f"{start_label}:\n" \
           f"PUSHG {idx}\nPUSHI {end_val}\nINFEQ\nJZ {end_label}\n" \
           f"{p[8]}" \
           f"PUSHG {idx}\nPUSHI 1\nADD\nSTOREG {idx}\n" \
           f"JUMP {start_label}\n" \
           f"{end_label}:\n"


def p_inst_for_downto(p):
    'inst_for : FOR IDENTIFIER ASSIGN NUMBER DOWNTO NUMBER DO corpo_ciclo'
    global label_counter, symbol_table
    
    if p[2] in symbol_table:
        var_idx = symbol_table[p[2]]['index']
        start_val = int(p[4])
        end_val = int(p[6])
        
        start_label = f"for_{label_counter}"
        end_label = f"end_for_{label_counter}"
        label_counter += 1
        
        init_code = f"PUSHI {start_val}\nSTOREG {var_idx}\n"
        
        test_code = f"{start_label}:\nPUSHG {var_idx}\nPUSHI {end_val}\nINFEQ\nJZ {end_label}\n"
        
        decrement_code = f"PUSHG {var_idx}\nPUSHI 1\nSUB\nSTOREG {var_idx}\nJUMP {start_label}\n{end_label}:\n"
        
        p[0] = f"{init_code}{test_code}{p[8]}{decrement_code}"
    else:
        print(f"Error: Variable '{p[2]}' not declared")
        global success
        success = False
        p[0] = f"# Error: Variable '{p[2]}' not declared\n"

def p_corpo_ciclo_1(p):
    'corpo_ciclo : BEGIN operacoes END SEMICOLON'
    p[0] = p[2]

def p_corpo_ciclo_2(p):
    'corpo_ciclo : operacao'
    p[0] = p[1]

# Error handling
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")
    global success
    success = False

parser = yacc.yacc()


def parse_input(data):
    global output, success, symbol_table, array_table, label_counter
    
    # Reset
    output = ""
    success = True
    symbol_table = {}
    array_table = {}
    label_counter = 0
    
    result = parser.parse(data)
    
    return output, success

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            data = file.read()
    else:
        data = sys.stdin.read()
    
    output, success = parse_input(data)
    
    if success:
        print(output)
    else:
        print("# Compilation failed with errors")