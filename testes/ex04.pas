{Defina uma função int bitsUm (unsigned int n) que calcula o numero de 
bits iguais a 1 usados na representação binária de um dado numero n.}

program TesteBitsUm;

function bitsUm(n: Cardinal): Integer;
var
  contador: Integer;
begin
  contador := 0;
  
  while n > 0 do
  begin
    if (n and 1) = 1 then
      contador := contador + 1;
    
    n := n shr 1;
  end;
  
  bitsUm := contador;
end;

var
  numero: Cardinal;
  resultado: Integer;
begin
  write('Digite um número inteiro não-negativo: ');
  readln(numero);
  
  resultado := bitsUm(numero);
  
  writeln('O número ', numero, ' tem ', resultado, ' bit(s) igual(is) a 1 na sua representação binária.');
end.