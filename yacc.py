from lex import tokens, lexer, re
import ply.yacc as yacc
import sys

# Z : expressao '$'

output = ""

# Regra inicial
def p_Z(p):
    'Z : expressao'
    p[0] = p[1]

# Regra para expressao
def p_expressao(p):
    '''expressao : declaracao_programa declaracao_end_begin
                 | declaracao_programa'''
    p[0] = p[1]

# Regra para declaracao_programa
def p_declaracao_programa(p):
    'declaracao_programa : PROGRAM IDENTIFIER SEMICOLON'
    p[0] = p[2]  # Retorna o identificador do programa

# Regra para declaracao_end_begin
def p_declaracao_end_begin(p):
    '''declaracao_end_begin : BEGIN corpo END DOT'''
    p[0] = p[2]  # Retorna o corpo

# Regra para corpo
def p_corpo(p):
    '''corpo : write
             | write corpo'''
    p[0] = p[1]

# Regra para write
def p_write(p):
    'write : WRITELN LPAREN TEXT RPAREN SEMICOLON'
    global output
    output += "PUSHS " + p[3] + "\nWRITES\n"
    p[0] = output  # Retorna o output gerado

# Tratamento de erros
def p_error(p):
    print("Erro sintático no input!")
    print(p)
    if p:
        print(f"Erro próximo ao token: {p.value}")
    else:
        print("Erro inesperado no final do input.")

# Construção do parser
parser = yacc.yacc()

# Leitura da entrada do arquivo
if __name__ == "__main__":
    try:
        # Lê a entrada do arquivo passado via stdin
        entrada = sys.stdin.read()
        entrada = re.sub(r'\s{2,}', ' ', entrada)  # Remove espaços extras

        # Processa a entrada
        conversor = parser.parse(entrada)
        print("Resultado: \n", output)
    except Exception as e:
        print("Erro ao processar entrada:", e)



