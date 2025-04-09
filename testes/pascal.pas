----------15---------------
program IguaisConsecutivos;

function iguaisConsecutivos(s: string): Integer;
var
  i, maxLen, currentLen: Integer;
begin
  if Length(s) = 0 then
  begin
    iguaisConsecutivos := 0;
    Exit;
  end;

  maxLen := 1;
  currentLen := 1;

  for i := 2 to Length(s) do
  begin
    if s[i] = s[i - 1] then
    begin
      currentLen := currentLen + 1;
      if currentLen > maxLen then
        maxLen := currentLen;
    end
    else
    begin
      currentLen := 1;
    end;
  end;

  iguaisConsecutivos := maxLen;
end;

var
  s: string;
  result: Integer;
begin
  s := 'aabccccaac';
  result := iguaisConsecutivos(s);
  WriteLn('Comprimento da maior sub-string com caracteres iguais: ', result);
end.

----------------16------------------

program MaiorSubstringDiferente;

function difConsecutivos(s: string): integer;
var
  i, j, maxLen, currentLen: integer;
  charSet: set of char;
begin
  maxLen := 0;
  i := 1;
  while i <= Length(s) do
  begin
    charSet := [];
    currentLen := 0;
    j := i;
    while (j <= Length(s)) and not (s[j] in charSet) do
    begin
      Include(charSet, s[j]);
      Inc(currentLen);
      Inc(j);
    end;
    if currentLen > maxLen then
      maxLen := currentLen;
    Inc(i);
  end;
  difConsecutivos := maxLen;
end;

begin
  WriteLn(difConsecutivos('aabcccaac'));  // Resultado: 3
end.

--------------17------------------------
program MaiorPrefixoComum;

function maiorPrefixo(s1, s2: string): integer;
var
  i, len: integer;
begin
  len := 0;
  i := 1;
  while (i <= Length(s1)) and (i <= Length(s2)) and (s1[i] = s2[i]) do
  begin
    Inc(len);
    Inc(i);
  end;
  maiorPrefixo := len;
end;

begin
  WriteLn(maiorPrefixo('abcdef', 'abcxyz'));  // Resultado: 3
  WriteLn(maiorPrefixo('hello', 'helicopter'));  // Resultado: 3
  WriteLn(maiorPrefixo('pascal', 'python'));  // Resultado: 0
end.

--------------------18--------------------


program MaiorSufixoComum;

function maiorSufixo(s1, s2: string): integer;
var
  i, j, len: integer;
begin
  len := 0;
  i := Length(s1);
  j := Length(s2);
  while (i > 0) and (j > 0) and (s1[i] = s2[j]) do
  begin
    Inc(len);
    Dec(i);
    Dec(j);
  end;
  maiorSufixo := len;
end;

begin
  WriteLn(maiorSufixo('abcdef', 'xyzdef'));  // Resultado: 3
  WriteLn(maiorSufixo('hellow', 'yellow'));  // Resultado: 5
  WriteLn(maiorSufixo('pascal', 'python'));  // Resultado: 0
end.

--------------19-------------------
program SufixoPrefixo;

function sufPref(s1, s2: string): integer;
var
  i, j, len: integer;
begin
  len := 0;
  for i := 1 to Length(s1) do
  begin
    if Copy(s1, Length(s1) - i + 1, i) = Copy(s2, 1, i) then
      len := i;
  end;
  sufPref := len;
end;

begin
  WriteLn(sufPref('batota', 'totalidade'));  // Resultado: 4
  WriteLn(sufPref('abc', 'abcd'));  // Resultado: 3
  WriteLn(sufPref('hello', 'world'));  // Resultado: 0
end.

------------20------------------

program ContaPalavras;

function contaPal(s: string): integer;
var
  i, count: integer;
  inWord: boolean;
begin
  count := 0;
  inWord := False;
  for i := 1 to Length(s) do
  begin
    if s[i] <> ' ' then
    begin
      if not inWord then
      begin
        inWord := True;
        Inc(count);
      end;
    end
    else
      inWord := False;
  end;
  contaPal := count;
end;

begin
  WriteLn(contaPal('a a bb a'));  // Resultado: 4
  WriteLn(contaPal('  hello world  '));  // Resultado: 2
  WriteLn(contaPal('Pascal programming language'));  // Resultado: 3
end.

---------------21---------------
program ContaVogais;

function contaVogais(s: string): integer;
var
  i, count: integer;
begin
  count := 0;
  for i := 1 to Length(s) do
  begin
    if s[i] in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'] then
      Inc(count);
  end;
  contaVogais := count;
end;

begin
  WriteLn(contaVogais('Hello World'));  // Resultado: 3
  WriteLn(contaVogais('Pascal Programming Language'));  // Resultado: 9
  WriteLn(contaVogais('AEIOUaeiou'));  // Resultado: 10
end.

--------------22-------------------
program Contida;

function contida(a, b: string): boolean;
var
  i: integer;
  found: boolean;
begin
  for i := 1 to Length(a) do
  begin
    found := Pos(a[i], b) > 0;
    if not found then
    begin
      contida := False;
      Exit;
    end;
  end;
  contida := True;
end;

begin
  WriteLn(contida('braga', 'bracara augusta'));  // Resultado: True
  WriteLn(contida('braga', 'bracarense'));  // Resultado: False
  WriteLn(contida('abc', 'aabbcc'));  // Resultado: True
end.

----------------23-------------

program Palindromo;

function palindromo(s: string): boolean;
var
  i, j: integer;
begin
  i := 1;
  j := Length(s);
  while (i < j) and (s[i] = s[j]) do
  begin
    Inc(i);
    Dec(j);
  end;
  palindromo := i >= j;
end;

begin
  WriteLn(palindromo('radar'));  // Resultado: True
  WriteLn(palindromo('hello'));  // Resultado: False
  WriteLn(palindromo('level'));  // Resultado: True
end.

-------------24--------------
program RemoveRepetidos;

function remRep(var x: string): integer;
var
  i, j: integer;
begin
  if Length(x) = 0 then
  begin
    remRep := 0;
    Exit;
  end;

  j := 1;
  for i := 2 to Length(x) do
  begin
    if x[i] <> x[j] then
    begin
      Inc(j);
      x[j] := x[i];
    end;
  end;
  SetLength(x, j);
  remRep := j;
end;

var
  s: string;
begin
  s := 'aaabaaabbbaaa';
  WriteLn(remRep(s));  // Resultado: 5
  WriteLn(s);  // Resultado: ababa
end.

--------------------25---------------
program LimpaEspacos;

function limpaEspacos(var t: string): integer;
var
  i, j: integer;
begin
  if Length(t) = 0 then
  begin
    limpaEspacos := 0;
    Exit;
  end;

  // Remover espaços no início
  while (Length(t) > 0) and (t[1] = ' ') do
    Delete(t, 1, 1);

  // Remover espaços no final
  while (Length(t) > 0) and (t[Length(t)] = ' ') do
    Delete(t, Length(t), 1);

  j := 1;
  for i := 2 to Length(t) do
  begin
    if not ((t[i] = ' ') and (t[j] = ' ')) then
    begin
      Inc(j);
      t[j] := t[i];
    end;
  end;
  SetLength(t, j);
  limpaEspacos := j;
end;

var
  s: string;
begin
  s := '  Este  e  um   teste  ';
  WriteLn(limpaEspacos(s));  // Resultado: 15
  WriteLn(s);  // Resultado: 'Este é um teste'
end.

--------------------26---------------
program InsereElemento;

procedure insere(var v: array of integer; N, x: integer);
var
  i, j: integer;
begin
  i := 0;
  while (i < N) and (v[i] < x) do
    Inc(i);

  for j := N downto i + 1 do
    v[j] := v[j - 1];

  v[i] := x;
end;

var
  v: array[1..10] of integer = (1, 3, 5, 7, 9, 0, 0, 0, 0, 0);
  N, i: integer;
begin
  N := 5;
  insere(v, N, 4);
  N := N + 1;

  for i := 1 to N do
    Write(v[i], ' ');
  WriteLn;
end.

------------------27-------------
program MergeVetores;

procedure merge(var r: array of integer; a: array of integer; b: array of integer; na, nb: integer);
var
  i, j, k: integer;
begin
  i := 0;
  j := 0;
  k := 0;

  while (i < na) and (j < nb) do
  begin
    if a[i] <= b[j] then
    begin
      r[k] := a[i];
      Inc(i);
    end
    else
    begin
      r[k] := b[j];
      Inc(j);
    end;
    Inc(k);
  end;

  while i < na do
  begin
    r[k] := a[i];
    Inc(i);
    Inc(k);
  end;

  while j < nb do
  begin
    r[k] := b[j];
    Inc(j);
    Inc(k);
  end;
end;

var
  a: array[1..5] of integer = (1, 3, 5, 7, 9);
  b: array[1..4] of integer = (2, 4, 6, 8);
  r: array[1..9] of integer;
  i: integer;
begin
  merge(r, a, b, 5, 4);

  for i := 1 to 9 do
    Write(r[i], ' ');
  WriteLn;
end.

------------28-----------------
program TestCrescente;

function crescente(a: array of Integer; i, j: Integer): Integer;
var
  k: Integer;
begin
  for k := i to j - 1 do
  begin
    if a[k] > a[k + 1] then
    begin
      crescente := 0;
      Exit;
    end;
  end;
  crescente := 1;
end;

var
  a: array[0..3] of Integer = (1, 2, 4, 5);  // Vetor ordenado
  result: Integer;
begin
  result := crescente(a, 0, 3);
  WriteLn('Resultado: ', result);
end.

-------------29-------------------
program RetiraNeg;

function retiraNeg(var v: array of Integer; N: Integer): Integer;
var
  i, j: Integer;
begin
  j := 0;
  for i := 0 to N - 1 do
  begin
    if v[i] >= 0 then
    begin
      v[j] := v[i];
      j := j + 1;
    end;
  end;
  retiraNeg := j;
end;

var
  v: array[0..5] of Integer = (1, -2, 3, -4, 5, -6);
  N, i: Integer;
begin
  N := retiraNeg(v, 6);
  WriteLn('Número de elementos não retirados: ', N);
  Write('Vetor resultante: ');
  for i := 0 to N - 1 do
  begin
    Write(v[i], ' ');
  end;
  WriteLn;
end.


--------30-----------------
program MenosFreq;

function menosFreq(v: array of Integer; N: Integer): Integer;
var
  i, currentCount, minCount, minElement, currentElement: Integer;
begin
  if N = 0 then
  begin
    menosFreq := -1; // Retorna -1 se o vetor estiver vazio
    Exit;
  end;

  currentElement := v[0];
  currentCount := 1;
  minElement := v[0];
  minCount := N + 1; // Inicializa com um valor maior que qualquer possível contagem

  for i := 1 to N do
  begin
    if (i < N) and (v[i] = currentElement) then
    begin
      currentCount := currentCount + 1;
    end
    else
    begin
      if currentCount < minCount then
      begin
        minCount := currentCount;
        minElement := currentElement;
      end;
      currentElement := v[i];
      currentCount := 1;
    end;
  end;

  menosFreq := minElement;
end;

var
  v: array[0..9] of Integer = (1, 1, 2, 2, 2, 3, 4, 4, 5, 5);
  N, result: Integer;
begin
  N := 10;
  result := menosFreq(v, N);
  WriteLn('Elemento menos frequente: ', result);
end.



