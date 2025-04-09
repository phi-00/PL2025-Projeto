{Defina uma função int iguaisConsecutivos (char s[]) que, dada uma string s calcula o
comprimento da maior sub-string com caracteres iguais. Por exemplo, iguaisConsecutivos
("aabcccaac") deve dar como resultado 3, correspondendo à repetição "ccc".}

program TestIguaisConsecutivos;

function iguaisConsecutivos(var s: string): integer;
var
  i, len, currentLen, maxLen: integer;
  currentChar: char;
begin
  len := Length(s);
  
  // Caso de string vazia
  if len = 0 then
  begin
    iguaisConsecutivos := 0;
    exit;
  end;
  
  maxLen := 1;        // Comprimento máximo encontrado até agora
  currentLen := 1;     // Comprimento da sequência atual
  currentChar := s[1]; // Caractere atual
  
  for i := 2 to len do
  begin
    if s[i] = currentChar then
    begin
      // Mesmo caractere, incrementa comprimento atual
      currentLen := currentLen + 1;
      
      // Verifica se a sequência atual é a maior encontrada
      if currentLen > maxLen then
        maxLen := currentLen;
    end
    else
    begin
      // Caractere diferente, começa nova sequência
      currentChar := s[i];
      currentLen := 1;
    end;
  end;
  
  iguaisConsecutivos := maxLen;
end;

var
  str: string;
  resultado: integer;
begin
  writeln('Forneca uma string:');
  readln(str);
  
  resultado := iguaisConsecutivos(str);
  
  writeln('Comprimento da maior subsequencia de caracteres iguais: ', resultado);
end.