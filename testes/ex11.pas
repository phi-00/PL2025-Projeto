{Defina uma função void strrev (char s[]) que inverte uma string.}

program TestStrrev;

function strrev (var str: string): string;
var
    i, len: integer;
    temp: string;
begin
    len := Length(str);
    temp := '';

    for i := len downto 1 do
        temp := temp + str[i];

    strrev := temp;
end;

var
    str, result: string;
begin
    writeln('Forneça um texto');
    readln(str);

    result := strrev(str);
    writeln(result);
end.