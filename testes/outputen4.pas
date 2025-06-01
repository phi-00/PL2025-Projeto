[DEBUG COMPARACAO] 'PUSHG 0\n' 'PUSHI 3\n' <
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'LT', 'expressao_aritmetica'] ['PUSHG 0\n', '<', 'PUSHI 3\n']
Resultado: 
 PUSHI 0
STOREG 0
L0:
PUSHG 0
PUSHI 3
INF
JZ L1
PUSHS "i = "
WRITES
PUSHG 0
WRITEI
PUSHG 0
PUSHI 1
ADD
STOREG 0
JUMP L0
L1:

