[DEBUG COMPARACAO] 'PUSHG 0\n' 'PUSHG 1\n' >
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'GT', 'expressao_aritmetica'] ['PUSHG 0\n', '>', 'PUSHG 1\n']
[DEBUG COMPARACAO] 'PUSHG 0\n' 'PUSHG 2\n' >
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'GT', 'expressao_aritmetica'] ['PUSHG 0\n', '>', 'PUSHG 2\n']
[DEBUG COMPARACAO] 'PUSHG 1\n' 'PUSHG 2\n' >
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'GT', 'expressao_aritmetica'] ['PUSHG 1\n', '>', 'PUSHG 2\n']
Resultado: 
 PUSHS "Introduza o primeiro número: "
WRITES
READ
ATOI
STOREG 0
PUSHS "Introduza o segundo número: "
WRITES
READ
ATOI
STOREG 1
PUSHS "Introduza o terceiro número: "
WRITES
READ
ATOI
STOREG 2
PUSHG 0
PUSHG 1
SUP
JZ L4
PUSHG 0
PUSHG 2
SUP
JZ L0
PUSHG 0
STOREG 3
JUMP L1
L0:
PUSHG 2
STOREG 3
L1:
JUMP L5
L4:
PUSHG 1
PUSHG 2
SUP
JZ L2
PUSHG 1
STOREG 3
JUMP L3
L2:
PUSHG 2
STOREG 3
L3:
L5:
PUSHS "O maior é: "
WRITES
PUSHG 3
WRITEI

