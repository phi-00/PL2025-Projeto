program Maior3;
var
    num1, num2, num3, maior: Integer;
begin
    Write('Introduza o primeiro número: ');
    ReadLn(num1);

    Write('Introduza o segundo número: ');
    ReadLn(num2);

    Write('Introduza o terceiro número: ');
    ReadLn(num3);

    if num1 > num2 then
        if num1 > num3 then maior := num1
        else maior := num3
    else
        if num2 > num3 then maior := num2
        else maior := num3;

    WriteLn('O maior é: ', maior);
end.