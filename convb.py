from decimal import getcontext
# dpenillac@69675
#getcontext().prec = 24 # 32 bit ieee754 <-- ?
                        # 64 bit -> 53 ->?<== X <=0.0
                        # formato ieee754'

### -> b16 -> b2 -> b8 
#  3 bits -> b8
#  4 bits -> b16
# | <-- primero |==> res[::-1]


def convert_decbase(num, base, prec=24):
    getcontext().prec = prec
    num = num.split('.')
    exts = [chr(65+i) for i in range(base-10)]
    z,q = int(num[0]),float('0.'+num[1])
    result = ""

    while (z > 1):
        res = int(z%base)
        z  /= int(base)
        if (res > 9):
            result += exts[res-10]
        else:
            result += str(res)
    
    result = result[::-1] + '.'
    
    idx = 0
    while(q > 0  and idx < prec):
        res = q * base
        if (res > 9): result += exts[int(res)-10]
        else: result += str(int(res))
        q = round(res - int(res),prec)
        idx+=1

    
    print(f"\t {num} -B{base}-> {result}")
    return result


def convert_to_dec(num,base,prec=24):
    getcontext().prec = prec
    num = num.split('.')
    z,q = num[0],num[1]
    basedict = []
    result = ""
    res = 0.0
    if base > 10:
        basedict = {chr(65+i): 10+i for i in range(base-10)}

    idxn = 0
    while(idxn < len(z)):
        x = z[idxn]
        if (base > 10 and x in basedict.keys()):
            x = basedict[x]
        xi = int(x)
        res += xi*(base**(len(z)-idxn-1))
        idxn+=1

    result += str(res)

    idxn = 0
    resq = 0.0
    while(idxn < len(q)):
        x = q[idxn]
        if (base > 10 and x in basedict.keys()):
            x = basedict[x]
        xi = int(x)
        resq += xi*(base**((idxn+1)*-1))
        idxn+=1
    
    result = str(int(res) + resq)
    print(result,' | ',res+resq)
    return result
        


convert_decbase('37178.42247',2)
convert_decbase('135.245',8)
convert_decbase('7821852.14754',16)

convert_to_dec('EFC.ABC',16)
convert_to_dec('BA9831.BBA12',13)
convert_to_dec('315131.12351',6)

# falta: oct -> hexa || ... 