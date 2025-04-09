{Defina uma função int trailingZ (unsigned int n) que calcula o número de bits a 0 no
final da representação binária de um número (i.e., o expoente da maior potência de 2 
que ́e divisor desse numero).}

program TesteTrailingZ;

function trailingZ(n: Cardinal): Integer;
var
  contador: Integer;
begin
  if n = 0 then
  begin
    trailingZ := 32;
    exit;
  end;
  
  contador := 0;
  
  while (n and 1) = 0 do
  begin
    contador := contador + 1;
    n := n shr 1;
  end;
  
  trailingZ := contador;
end;

var
  numero: Cardinal;
  resultado: Integer;
begin
  write('Digite um número inteiro não-negativo: ');
  readln(numero);
  
  resultado := trailingZ(numero);
  
  writeln('O número ', numero, ' tem ', resultado, ' bits 0 no final da sua representação binária.');
end.