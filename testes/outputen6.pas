[DEBUG COMPARACAO] 'PUSHG 0\n' 'PUSHG 1\n' <
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'LT', 'expressao_aritmetica'] ['PUSHG 0\n', '<', 'PUSHG 1\n']
[DEBUG COMPARACAO] 'PUSHG 0\n' 'PUSHI 5\n' =
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'EQ', 'expressao_aritmetica'] ['PUSHG 0\n', '=', 'PUSHI 5\n']
[DEBUG COMPARACAO] 'PUSHG 1\n' 'PUSHI 10\n' =
[DEBUG COND] ['expressao_condicional', 'expressao_aritmetica', 'EQ', 'expressao_aritmetica'] ['PUSHG 1\n', '=', 'PUSHI 10\n']
Resultado: 
 PUSHI 5
STOREG 0
PUSHI 10
STOREG 1
NOT
JZ L4
PUSHS "Expressao booleana funciona!"
WRITES
L4:

