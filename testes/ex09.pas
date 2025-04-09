{Apresente uma definição da função pré-definida em C int strcmp (char s1[], char s2[])
que compara (lexicograficamente) duas strings. O resultado deverá ser
• 0 se as strings forem iguais
• <0 se s1 < s2
• >0 se s1 > s2}

program TestStrcmp;

function strcmp (var str1: string; str2: string): Integer;
begin
    if str1 = str2 then
        strcmp := 0
    else if str1 < str2 then
        strcmp := -1
    else if str1 > str2 then
        strcmp := 1
end;

var
    str1, str2: string;
    result: Integer;
begin
    writeln('Forneça um texto');
    readln(str1);

    writeln('Forneça outro texto');
    readln(str2);

    result := strcmp(str1, str2);
    writeln(result);
end.