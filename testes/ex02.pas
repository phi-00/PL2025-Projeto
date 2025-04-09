program CalculaMedia;
var
    media: double;
    numero, soma, contador: integer;
begin
  contador := 0;
  soma := 0;
  media := 0;
  
  write('Digite um numero (0 para terminar): ');
  readln(numero);
  
  if numero = 0 then
    writeln('Nenhum numero foi digitado!')
  else
  begin
    while numero <> 0 do
    begin
        soma := soma + numero;
        contador := contador + 1;

      
      write('Digite um numero (0 para terminar): ');
      readln(numero);
    end;
    
    write('Contador: ', contador);
    write('Soma: ', soma);
    media := soma / contador;
    writeln('media: ', media:0:2);
  end;
end.
