program TesteArray;
var
  arr: array [1..5] of integer;
  i: integer;

begin
  for i := 1 to 5 do
    arr [i] := i;

  for i := 1 to 5 do
    writeln('Elemento ', i, ': ', arr[i]);
end.
