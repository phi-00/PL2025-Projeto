{Defina uma função int qDig (unsigned int n) que calcula o numero de dígitos necessários
para escrever o inteiro n em base decimal. Por exemplo, qDig (440) deve retornar 3.}

program TesteQDig;

function qDig(n: Cardinal): Integer;
var
  contador: Integer;
begin
  if n = 0 then
  begin
    qDig := 1;
    exit;
  end;
  
  contador := 0;
  
  while n > 0 do
  begin
    contador := contador + 1;
    n := n div 10;
  end;
  
  qDig := contador;
end;

var
  numero: Cardinal;
  resultado: Integer;
begin
  write('Digite um número inteiro não-negativo: ');
  readln(numero);
  
  resultado := qDig(numero);
  
  writeln('O número ', numero, ' tem ', resultado, ' digitos na sua representação binária.');
end.