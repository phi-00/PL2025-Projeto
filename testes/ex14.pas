{Defina uma função char charMaisfreq (char s[]) que determina qual o caracter mais fre-
quente numa string. A função deverá retornar 0 no caso de s ser a string vazia.}

program TestCharMaisfreq;

function charMaisfreq(var s: string): char;
var
  i, j, len, maxFreq, currentFreq: integer;
  charMaisFrequente: char;
  contado: array[1..255] of boolean;  // Para marcar caracteres já contados
begin
  len := Length(s);
  
  // Caso de string vazia
  if len = 0 then
  begin
    charMaisfreq := #0;  // Retorna o caractere nulo (0)
    exit;
  end;
  
  // Inicializa o array de caracteres contados
  for i := 1 to 255 do
    contado[i] := false;
  
  maxFreq := 0;
  charMaisFrequente := ' ';
  
  for i := 1 to len do
  begin
    // Só verifica se este caractere ainda não foi processado
    if not contado[ord(s[i])] then
    begin
      contado[ord(s[i])] := true;
      currentFreq := 0;
      
      // Conta a frequência do caractere atual
      for j := 1 to len do
      begin
        if s[j] = s[i] then
          currentFreq := currentFreq + 1;
      end;
      
      // Verifica se é o mais frequente até agora
      if currentFreq > maxFreq then
      begin
        maxFreq := currentFreq;
        charMaisFrequente := s[i];
      end;
    end;
  end;
  
  charMaisfreq := charMaisFrequente;
end;

var
  str: string;
  resultado: char;
begin
  writeln('Forneça um texto (ou deixe vazio para testar string vazia):');
  readln(str);
  
  resultado := charMaisfreq(str);
  
  if resultado = #0 then
    writeln('String vazia')
  else
    writeln('Caractere mais frequente: ''', resultado, '''');
end.