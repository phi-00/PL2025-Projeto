program MaiorNum;
var
  numero, maior: integer;
begin
  maior := -32768;
  
  write('Digite um numero (0 para terminar): ');
  readln(numero);
  
  if numero = 0 then
    writeln('Nenhum numero foi digitado!')
  else
  begin
    while numero <> 0 do
    begin
      if numero > maior then
        maior := numero;
      
      write('Digite um numero (0 para terminar): ');
      readln(numero);
    end;
    
    writeln('O maior numero da sequencia e: ', maior);
  end;
end.