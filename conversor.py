#Juan Camilo Bolaños

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
    # Convertir a minúsculas para hacer las cosas más simples
    hexadecimal = hexadecimal.upper()
    # La debemos recorrer del final al principio, así que la invertimos
    hexadecimal = hexadecimal[::-1]
    decimal = 0
    posicion = 0
    for digito in hexadecimal:
        # Necesitamos que nos dé un 10 para la A, un 9 para el 9, un 11 para la B, etcétera
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
    # Invertir octal, porque debemos recorrerlo de derecha a izquierda
    # pero for in empieza de izquierda a derecha
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
    # Aquí almacenamos el resultado
    binario = ""
    # Mientras se pueda dividir...
    while decimal > 0:
        # Saber si es 1 o 0
        residuo = int(decimal % 2)
        # E ir dividiendo el decimal
        decimal = int(decimal / 2)
        # Ir agregando el número (1 o 0) a la izquierda del resultado
        binario = str(residuo) + binario
    return binario


def binario_a_decimal(binario):
    posicion = 0
    decimal = 0
    # Invertir la cadena porque debemos recorrerla de derecha a izquierda
    # https://parzibyte.me/blog/2019/06/26/invertir-cadena-python/
    binario = binario[::-1]
    for digito in binario:
        # Elevar 2 a la posición actual
        multiplicador = 2**posicion
        decimal += int(digito) * multiplicador
        posicion += 1
    return decimal

def floatingPoint(real_no):
 
    # Setting Sign bit
    # default to zero.
    sign_bit = 0
 
    # Sign bit will set to
    # 1 for negative no.
    if(real_no < 0):
        sign_bit = 1
 
    # converting given no. to
    # absolute value as we have
    # already set the sign bit.
    real_no = abs(real_no)
 
    # Converting Integer Part
    # of Real no to Binary
    int_str = bin(int(real_no))[2 : ]
 
    # Function call to convert
    # Fraction part of real no
    # to Binary.
    fraction_str = binaryOfFraction(real_no - int(real_no))
 
    # Getting the index where
    # Bit was high for the first
    # Time in binary repres
    # of Integer part of real no.
    ind = int_str.index('1')
 
    # The Exponent is the no.
    # By which we have right
    # Shifted the decimal and
    # it is given below.
    # Also converting it to bias
    # exp by adding 127.
    exp_str = bin((len(int_str) - ind - 1) + 127)[2 : ]
 
    # getting mantissa string
    # By adding int_str and fraction_str.
    # the zeroes in MSB of int_str
    # have no significance so they
    # are ignored by slicing.
    mant_str = int_str[ind + 1 : ] + fraction_str
 
    # Adding Zeroes in LSB of
    # mantissa string so as to make
    # it's length of 23 bits.
    mant_str = mant_str + ('0' * (23 - len(mant_str)))
 
    # Returning the sign, Exp
    # and Mantissa Bit strings.
    return sign_bit, exp_str, mant_str

def binaryOfFraction(fraction):
 
    # Declaring an empty string
    # to store binary bits.
    binary = str()
 
    # Iterating through
    # fraction until it
    # becomes Zero.
    while (fraction):
         
        # Multiplying fraction by 2.
        fraction *= 2
 
        # Storing Integer Part of
        # Fraction in int_part.
        if (fraction >= 1):
            int_part = 1
            fraction -= 1
        else:
            int_part = 0
     
        # Adding int_part to binary
        # after every iteration.
        binary += str(int_part)
 
    # Returning the binary string.
    return binary