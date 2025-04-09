{Defina uma função void strnoV (char s[]) que retira todas as vogais de uma string.}

program TestStrnoV;

function strnoV (var str: string): string;
var
    i, len: integer;
    result: string;
begin
    len := Length(str);
    result := '';

    for i := 1 to len do
    begin
        if (Upcase(str[i]) <> 'A') and (Upcase(str[i]) <> 'E') and (Upcase(str[i]) <> 'I') and (Upcase(str[i]) <> 'O') and (Upcase(str[i]) <> 'U') then
        begin
            result := result + str[i];
        end;
    end;

    strnoV := result;
end;

var
    str, result: string;
begin
    writeln('Forneça um texto');
    readln(str);

    result := strnoV(str);
    writeln(result);
end.