program TestaBooleanos;
var
  a, b: integer;
begin
  a := 5;
  b := 10;
  if not (a < b) or (a = 5 and b = 10) then
    writeln('Expressao booleana funciona!');
end.
