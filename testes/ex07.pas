{Apresente uma definição da função pré-definida em C char *strcat (char s1[], char
s2[]) que concatena a string s2 a s1 (retornando o endereço da primeira).}

program TestStrcat;

function strcat (var s1: string; s2: string): string;
begin
    s1 := s1 + s2;
    strcat := s1;
end;

var
    str1, str2, result: string;
begin
    writeln('Forneça um texto');
    readln(str1);

    writeln('Forneça outro texto');
    readln(str2);

    result := strcat(str1, str2);

    writeln(result);

end.