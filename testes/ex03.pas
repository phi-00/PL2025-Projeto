{Defina um programa que lê (usando a função scanf uma sequência de numeros inteiros 
terminada com o número 0 e imprime no ecra o segundo maior elemento.}

program SegundoMaior;
var
  numero, maior, segmaior: integer;
begin
  maior := -32768;
  segmaior := -32768;
  
  write('Digite um numero (0 para terminar): ');
  readln(numero);
  
  { Se o primeiro número for 0, não há sequência para processar }
  if numero = 0 then
    writeln('Nenhum numero foi digitado!')
  else
  begin
    maior := numero;
    write('Digite um numero (0 para terminar): ');
    readln(numero);
    if numero = 0 then
      writeln('Sequência de um só número (não existe segundo maior)!')
    else
    begin
      if numero > maior then
      begin
        segmaior := maior;
        maior := numero;
      end
      else
        segmaior := numero;
      
      write('Digite um numero (0 para terminar): ');
      readln(numero);
      
      { Processa a sequência enquanto não encontrar o 0 }
      while numero <> 0 do
      begin
        { Verifica se o número atual é maior que o maior encontrado até agora }
        if numero > maior then
        begin
          segmaior := maior;
          maior := numero;
        end
        else if (numero > segmaior) and (numero < maior) then
          segmaior := numero;
        
        { Lê o próximo número }
        write('Digite um numero (0 para terminar): ');
        readln(numero);
      end;
      
      { Imprime o resultado }
      writeln('O segundo maior numero da sequencia e: ', segmaior);
    end;
  end;
end.