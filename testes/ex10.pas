{Apresente uma definição da função pré-definida em C char *strstr (char s1[], char
s2[]) que determina a posição onde a string s2 ocorre em s1. A função deverá retornar
NULL caso s2 não ocorra em s1.}

program TestStrstr;

function strstr(s1, s2: string): string;
var
  posicao: integer;
begin
  posicao := Pos(s2, s1);
  
  if posicao > 0 then
    strstr := Copy(s1, posicao, Length(s1) - posicao + 1)
  else
    strstr := '';
end;

var
    str1, str2, result: string;
begin
    writeln('Forneça um texto');
    readln(str1);

    writeln('Forneça outro texto');
    readln(str2);

    result := strstr(str1, str2);
    writeln(result);
end.