from decimal import getcontext
from math import log
#from convb import *

base_ext = {chr(65+i): 10+i for i in range(6)}

def extender_sistema(num) -> int:
    global base_ext
    try: 
        return int(num)
    except:
        return int(base_ext[num])




# bin -> oct | hex

def dosn_bin(num,base,baseT,prec=24):
    #if num.find('.') == False: num += '.00' # si pasa un entero

    getcontext().prec = prec

    num = num.split('.')
    z,q = num[0],num[1]
    #pot_max = int( log(base) / log(2) )
    #pot_dos = [2**(pot_max-1-i) for i in range(pot_max)]

    result = ""
    # hex -> bin |
    idxn = 0
    while(idxn < len(z)):
        x = extender_sistema(z[idxn])
        print(f"xmod | {x}")

        while(x >= baseT):
            result += str(extender_sistema(x % baseT))
            x /= baseT
        
        idxn+=1
           
    result = result[::-1] + '.'
    print(f"RESULT : {result}")
        
    qf = float('0.'+q)
    idx = 0
    while (qf > 0.0 and idx < prec):
        res = qf * baseT
        result += str(extender_sistema(int(res)))
        qf = round(res - int(res), prec)
        idx+=1

    print('RESULTADO: ',num,f" ---B{baseT} -> ",result)        
    return result


    


    ''' 
    idxn = 0
    while(idxn < len(z)):
        x = z[idxn]
        if (base > 10 and x in base_ext.keys()):
            x = base_ext[x]
        x = int(x) 
        i = 0 

        while(x >= 0.0 and i < len(pot_dos)):
            if (x - pot_dos[i] >= 0.0):
                result += '1'
                x -= pot_dos[i]
            else:
                result += '0'

            i += 1
        
        idxn +=1
    
    idxn = 0
    #while(idxn < len(q)):
    #    x = q[idxn]
    #    if (base > 10 and x in base_ext.keys()):
    #        x = base_ext[x]
    #    x = int(x)
    #    i = 0

    '''

    
    #return result

numx = input('Please enter the number: ')

print(dosn_bin(numx,16,2))
print(dosn_bin(numx,16,8))
print(dosn_bin(numx,10,16))



#print(dosn_bin('AFBC56.00',16))
#print(dosn_bin('8BF1.00',16))
#print(dosn_bin('7521.00',8))

#print(convert_to_dec(dosn_bin('32.00',16)+'.00',2))

#print(convert_decbase('573.00',8))


'''
           lista[i] = int(lista[i])
                while (lista[i] >= baseT):
                    num = num + str(int(lista[i] % baseT))
                    lista[i] = lista[i] / baseT

                num = num + str(int(lista[i]
'''
