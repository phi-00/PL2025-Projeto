[DEBUG COMPARACAO] 'PUSHG 1\n' 'PUSHG 0\nPUSHI 2\nDIV\n' <=
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'LE', 'expressao_aritmetica'] ['PUSHG 1\n', '<=', 'PUSHG 0\nPUSHI 2\nDIV\n']
[DEBUG COMPARACAO] 'PUSHG 0\nPUSHG 1\nMOD\n' 'PUSHI 0\n' =
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'EQ', 'expressao_aritmetica'] ['PUSHG 0\nPUSHG 1\nMOD\n', '=', 'PUSHI 0\n']
Resultado: 
 PUSHS "Introduza um número inteiro positivo:"
WRITES
READ
ATOI
STOREG 0
PUSHI 1
STOREG 2
PUSHI 2
STOREG 1
L5:
JZ L6
PUSHG 0
PUSHG 1
MOD
PUSHI 0
SUB
JZ L2
PUSHI 0
JUMP L3
L2:
PUSHI 1
L3:
JZ L4
PUSHI 0
STOREG 2
L4:
PUSHG 1
PUSHI 1
ADD
STOREG 1
JUMP L5
L6:
PUSHG 2
JZ L7
PUSHG 0
WRITEI
PUSHS " é um número primo"
WRITES
JUMP L8
L7:
PUSHG 0
WRITEI
PUSHS " não é um número primo"
WRITES
L8:

