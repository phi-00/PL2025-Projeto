program Loop;
var
  i: Integer;
begin
  i := 0;
  while i < 3 do
  begin
    writeln('i = ', i);
    i := i + 1;
  end;
end.
