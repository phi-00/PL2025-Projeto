{Apresente uma definição da função pré-definida em C char *strcpy (char *dest, char
source[]) que copia a string source para dest retornando o valor desta  ́ultima.}

program TestStrcopy;

function strcopy (var dest: string; source: string): string;
begin
    dest := source;
    strcopy := dest;
end;

var
    src, dst, result: string;
begin
    writeln('Forneça um texto');
    readln(src);

    dst := '';
    result := strcopy(dst, src);
    writeln(result);
end.