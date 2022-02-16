from decimal import getcontext
#getcontext().prec = 24 # 32 bit ieee754 <-- ?
                        # 64 bit -> 53 ->? <== X <=0.0
                        # formato ieee754'

### -> b16 -> b2 -> b8 
#  3 bits -> b8
#  4 bits -> b16
# | <-- primero |==> res[::-1]
# ----------------------------

class Conversor():
    exts = [chr(65+i) for i in range(6)]

    def convert_decbase(self,num, base, prec=24):
        getcontext().prec = prec
        num = num.split('.')
        
        z,q = int(num[0]),float('0.'+num[1])
        result = ""

        while (z > 1):
            res = int(z%base)
            z  /= int(base)
            if (res > 9 and base > 10): 
                result += self.exts[res-10]
            else: result += str(res)
        
        result = result[::-1] + '.'
        
        idx = 0
        while(q > 0  and idx < prec):
            res = q * base
            if (res > 9): result += self.exts[int(res)-10]
            else: result += str(int(res))
            q = round(res - int(res),prec)
            idx+=1

        
        #print(f"\t {num} -B{base}-> {result}")
        return result

    basedict = {chr(65+i): 10+i for i in range(6)}

    def convert_to_dec(self,num,base,prec=24):
        getcontext().prec = prec
        
        q = ''
        if '.' in num:
            num = num.split('.')
            z,q = num[0],num[1]
        else:
            z = num
     

        result = ""
        res = 0.0

        idxn = 0
        while(idxn < len(z)):
            x = z[idxn]
            if (base > 10 and x in self.basedict.keys()):
                x = self.basedict[x]
            xi = int(x)
            res += xi*(base**(len(z)-idxn-1))
            idxn+=1

        result += str(res)

        idxn = 0
        resq = 0.0
        if q != '':   
            while(idxn < len(q)):
                x = q[idxn]
                if x == '.':
                    idxn+=1
                    continue
                if (base > 10 and x in self.basedict.keys()):
                    x = self.basedict[x]
                xi = int(x)
                resq += xi*(base**((idxn+1)*-1))
                idxn+=1
        
        #result = str(round(int(res) + resq, len(z)+len(q)+1))
        result = str(int(res) + resq)
        #print(z+'.'+q,f" -- B{base} -> DEC  |   ",res+resq)
        return result


    #----------------------------------------------------------------
    # Maneras más óptimas existirán para directamente convertir de cualquier base
    # a cualquier otra. Seguimos buscándolas 

    def convertirNM(self,num,bN,bM,prec=16):
        return self.convert_decbase(self.convert_to_dec(num, bN,prec), bM,prec) if bN != bM else num




#print(convert_to_dec('13F.A',16))



'''   interactivo: 
numx = input('ingrese numero: ')
bN = int(input('de base N: '))
bM = int(input('a base M: '))

cc = Conversor()

print(cc.convertirNM(numx,bN,bM))

'''


#x=convert_to_dec(convert_decbase(numx, 2),2)

#onvert_decbase(numx, 8)
#convert_decbase(numx, 16)
# 2 -> 8: 2 -> 10 -> 8
#x = convert_decbase(convert_to_dec(numx,2),8) # funciona bN -> bM <== bN -> b10 -> bM | suboptimo ?

#print(f" EPA : {x}")

#print(convertirNM(numx,10,8))
#print(convert_decbase(convert_to_dec(numx,10),8))
