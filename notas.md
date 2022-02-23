iEEE754 -> 32 bit (simple) | 64 bit (double)

    signo.exponente.mantisa:

    signo ) 1 : - | 0 : +
    exponente ) normalizar: pasar la cifra mas significativa a la izquierda, 2 elevado al numero de cifras movidas hacia el 0.
    mantisa )  ? 

1 cifra para el exponente,
8 para el exponente
23 para la mantisa


$$ 168.35 = 10101000.01011000110 _{2}$$
Normalizamos
$$ 1.0101000101100110 \times 2^7 \quad|\quad exp = 7$$
-- mantisa  -- exp

Exponente: 
  $$  exp = 7 \quad | \quad 7 + 127 = 134 $$
  $$  134 = 100000110_{2} $$

$$ 0. 10000110 010100000101100110 $$

