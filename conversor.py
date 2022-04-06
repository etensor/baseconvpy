#Juan Camilo Bolaños 70103

from dataclasses import replace
from ibm2ieee import ibm2float32, ibm2float64

from email.policy import strict
import math
import struct
import numpy 
#nuevo
from ibm2ieee import ibm2float32, ibm2float64

# base(number, input_base, output_base)
#Binario a decimal (str)
#Decimal a octal (int)
#Decimal a hexadecimal (int)
print('32 ',ibm2float32(numpy.uint32(0xc1180000)))
def conversor(num, base):
    si = num
    if si.find('.') != -1:
        dec = num[num.find('.')+1:len(num)]
        num = num[0:num.find('.')]

        binarioF = convertir_fraccion(dec, 2)
        octalF = convertir_fraccion(dec, 8)
        decimalF = convertir_fraccion(dec, 10)
        hexadecimalF = convertir_fraccion(dec, 16)

    if base == 2:
        num = int(num)
        binario = str(num)
        octal = binario_a_decimal(str(num))
        octal = decimal_a_octal(octal)
        decimal = binario_a_decimal(str(num))
        hexadecimal = decimal_a_hexadecimal(decimal)

    elif base == 8:
        num = int(num)
        binario = octal_a_decimal(str(num))
        binario = decimal_a_binario(binario)
        octal = str(num)
        decimal = octal_a_decimal(str(num))
        hexadecimal = decimal_a_hexadecimal(num)

    elif base == 10:
        num = int(num)
        binario = decimal_a_binario(num)
        octal = decimal_a_octal(num)
        decimal = str(num)
        hexadecimal = decimal_a_hexadecimal(num)

    elif base == 16:
        binario = hexadecimal_a_decimal(num)
        binario = decimal_a_binario(binario)
        octal = hexadecimal_a_decimal(num)
        octal = decimal_a_octal(octal)
        decimal = hexadecimal_a_decimal(num)
        hexadecimal = num

    if si.find('.') != -1:
        binario = binario + '.' + binarioF
        octal = octal + '.' + octalF
        decimal = decimal + '.' + decimalF
        hexadecimal = hexadecimal + '.' + hexadecimalF

    return binario, octal, decimal, hexadecimal

def remplazo16(num):
        num=int(num)
        if num==10:
            return 'A'
        elif num==11: 
            return  'B'
        elif num==12:
            return  'C'
        elif num==13:
            return  "D"
        elif num==14:
            return  "E"
        elif num==15:
            return  "F"
        else:
            return str(num)

def convertir_fraccion(dec, base):
    msj=""
    dec = dec[::-1] + ".0"
    dec = dec[::-1]
    auxiliar= float(dec)
    for i in range(0,8):
        operacion=auxiliar*base
        msj= msj+""+str(remplazo16(int(operacion)))
        decimal=str(operacion).split('.')
        auxiliar=float("0."+decimal[1])
    return msj

def obtener_caracter_hexadecimal(valor):
    # Lo necesitamos como cadena
    valor = str(valor)
    equivalencias = {
        "10": "A",
        "11": "B",
        "12": "C",
        "13": "D",
        "14": "E",
        "15": "F",
    }
    if valor in equivalencias:
        return equivalencias[valor]
    else:
        return valor

def fraccion(num, base, baseA):
    pass

def decimal_a_hexadecimal(decimal):
    hexadecimal = ""
    while decimal > 0:
        residuo = decimal % 16
        verdadero_caracter = obtener_caracter_hexadecimal(residuo)
        hexadecimal = verdadero_caracter + hexadecimal
        decimal = int(decimal / 16)
    return hexadecimal


def obtener_valor_real(caracter_hexadecimal):
    equivalencias = {
        "F": 15,
        "E": 14,
        "D": 13,
        "C": 12,
        "B": 11,
        "A": 10,
    }
    if caracter_hexadecimal in equivalencias:
        return equivalencias[caracter_hexadecimal]
    else:
        return int(caracter_hexadecimal)


def hexadecimal_a_decimal(hexadecimal):
    hexadecimal = hexadecimal.upper()
    hexadecimal = hexadecimal[::-1]
    decimal = 0
    posicion = 0
    for digito in hexadecimal:
        valor = obtener_valor_real(digito)
        elevado = 16 ** posicion
        equivalencia = elevado * valor
        decimal += equivalencia
        posicion += 1
    return decimal


def decimal_a_octal(decimal):
    octal = ""
    while decimal > 0:
        residuo = decimal % 8
        octal = str(residuo) + octal
        decimal = int(decimal / 8)
    return octal


def octal_a_decimal(octal):
    decimal = 0
    posicion = 0
    octal = octal[::-1]
    for digito in octal:
        valor_entero = int(digito)
        numero_elevado = int(8 ** posicion)
        equivalencia = int(numero_elevado * valor_entero)
        decimal += equivalencia
        posicion += 1
        
    return decimal


def decimal_a_binario(decimal):
    if decimal <= 0:
        return "0"
    binario = ""
    while decimal > 0:
        residuo = int(decimal % 2)
        decimal = int(decimal / 2)
        binario = str(residuo) + binario
    return binario

def binario_a_decimal(binario):
    posicion = 0
    decimal = 0
    binario = binario[::-1]
    for digito in binario:
        multiplicador = 2**posicion
        decimal += int(digito) * multiplicador
        posicion += 1
    return decimal

def analizar(num, base):
    if num.find('.') == -1:
        return entero(num, int(base))

    else:
        frac = num[num.find('.')+1::]
        num = num[:num.find('.')]
        binario, octal, decimal, hexadecimal = entero(num, int(base))
        fraccionBinario, fraccionOctal, fraccionDecimal, fraccionHexadecimal = fraccion(frac, base)
        return binario + '.' + fraccionBinario, octal + '.' + fraccionOctal, decimal + '.' + fraccionDecimal, hexadecimal + '.' + fraccionHexadecimal

def entero(num, base):
    if base == 2:
        binario = num
        decimal = str(binario_a_decimal(num))
        octal = str(decimal_a_octal(int(decimal)))
        hexadecimal = str(decimal_a_hexadecimal(int(decimal)))
    elif base == 8:
        decimal = str(octal_a_decimal(str(num)))
        binario = str(decimal_a_binario(int(decimal)))
        octal = num
        hexadecimal = str(decimal_a_hexadecimal(int(decimal)))
    elif base == 10:
        binario = str(decimal_a_binario(int(num)))
        octal = str(decimal_a_octal(int(num)))
        decimal = num
        hexadecimal = str(decimal_a_hexadecimal(int(num)))
    elif base == 16:
        num = num.upper()
        decimal = str(hexadecimal_a_decimal(num))
        binario = str(decimal_a_binario(int(decimal)))
        octal = str(decimal_a_octal(int(decimal)))
        hexadecimal = num

    return binario, octal, decimal, hexadecimal

def fraccion(num, base):
    if base == 10:
        fraccionDecimal = num
    else:
        fraccionDecimal = fraccion_a_fracciondecimal(num, base)

    fraccionBinario, fraccionOctal, fraccionHexadecimal = fracciondecimal_a_fraccion(fraccionDecimal)

    return fraccionBinario, fraccionOctal, fraccionDecimal, fraccionHexadecimal

def fraccion_a_fracciondecimal(num, base):
    i = -1
    fraccion = 0
    for x in num:
        valorReal = obtener_valor_real(x)
        fraccion += int(valorReal) * (int(base) ** int(i))
        i -= 1

    fraccion = str(fraccion)
    return fraccion[fraccion.find('.')+1::]

def fracciondecimal_a_fraccion(num):
    num = num[::-1] + '.0'
    num = num[::-1]
    bases = [2, 8, 16]
    salida = list()
    aux = num
    resultado = ''

    for x in bases:
        for i in range(0, 8):
            if float(num) == 0:
                break

            num = float(num) * x
            num = str(num)
            resultado += obtener_caracter_hexadecimal(int(num[:num.find('.')]))
            num = num[num.find('.')+1::]
            num = num[::-1] + '.0'
            num = float(num[::-1])

        salida.append(resultado)
        resultado = ''
        num = aux
    
    return salida[0], salida[1], salida[2]

def floatingPoint(real_no):
 
    sign_bit = 0

    if(real_no < 0):
        sign_bit = 1
 
    real_no = abs(real_no)

    int_str = bin(int(real_no))[2 : ]

    fraction_str = binaryOfFraction(real_no - int(real_no))
 
    ind = int_str.index('1')

    exp_str = bin((len(int_str) - ind - 1) + 127)[2 : ]
 
    mant_str = int_str[ind + 1 : ] + fraction_str
 
    mant_str = mant_str + ('0' * (23 - len(mant_str)))

    return sign_bit, exp_str, mant_str

def binaryOfFraction(fraction):

    binary = str()

    while (fraction):

        fraction *= 2

def floatingPoint(real_no):
 
    sign_bit = 0
 
    if(real_no < 0):
        sign_bit = 1
 
    real_no = abs(real_no)
 
    int_str = bin(int(real_no))[2 : ]
 
    fraction_str = binaryOfFraction(real_no - int(real_no))
 
    ind = int_str.index('1')
 
    exp_str = bin((len(int_str) - ind - 1) + 127)[2 : ]
 
    mant_str = int_str[ind + 1 : ] + fraction_str
 
    mant_str = mant_str + ('0' * (23 - len(mant_str)))

    return sign_bit, exp_str, mant_str

def binaryOfFraction(fraction):
 
    binary = str()
 
    while (fraction):
         
        fraction *= 2
 
        if (fraction >= 1):
            int_part = 1
            fraction -= 1
        else:
            int_part = 0

        binary += str(int_part)
        binary += str(int_part)
 
    return binary