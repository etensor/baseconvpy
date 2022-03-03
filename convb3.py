from decimal import getcontext
import re
#getcontext().prec = 24 # 32 bit -> 23
        #ieee754        # 64 bit -> 53
                        # formato ieee754'

### -> b16 -> b2 -> b8 
#  3 bits -> b8
#  4 bits -> b16
# | <-- primero |==> res[::-1]
# ----------------------------


class Conversor():
        
    basedict = {chr(65+i): 10+i for i in range(6)}
    exts = list(basedict.keys())

    def convert_decbase(self,num, base, prec=16):
        if num == '' or len(num) == 0:
            return num
        getcontext().prec = prec
        frac = True
        result = ''
        if num[0] == '-':
            result+='-'
            num = num[1:]
        if base == 10 or num == '0.0':
            return num
        
        if '.' not in num:
            num += '.0'
            frac = False

        num = num.split('.')
        z,q = int(num[0]),float('0.'+num[1])
        
        aux = ''
        while (z >= 1):
            res = int(z%base)
            z  /= int(base)
            if (res > 9 and base > 10): 
                aux += self.exts[res-10]
            else: aux += str(res)
        
        result += aux[::-1]
        if frac:
            result += '.'
        
        
        idx = 0
        while(q > 0  and idx < prec):
            res = q * base
            if (res > 9): result += self.exts[int(res)-10]
            else: result += str(int(res))
            q = round(res - int(res),prec)
            idx+=1

        
        #print(f"\t {num} -B{base}-> {result}")
        return result


    def convert_to_dec(self,num,base,prec=16):
        getcontext().prec = prec
        if num in('0.0',''):
            return num

        if '.' not in num:
            num += '.0'
        
        z,q = num.split('.')
        

        result = ""
        res = 0.0

        idxn = 0
        z = z.strip()
        if z[0] =='-':
            result += z[0]
            z = z[1:]
        while(idxn < len(z)):
            x = z[idxn]
            if (base > 10 and x in self.basedict.keys()):
                x = self.basedict[x]
            xi = int(x)
            res += xi*(base**(len(z)-idxn-1))
            idxn+=1


        idxn = 0
        resq = 0.0
        if q != '':   
            while(idxn < len(q)):
                x = q[idxn]
                if x == '.':
                    idxn+=1
                    continue
                if (x in self.basedict.keys()):
                    x = self.basedict[x]
                    
                xi = int(x)
                resq += xi*(base**((idxn+1)*-1))
                idxn+=1
        
        #result = str(round(int(res) + resq, len(z)+len(q)+1))
        result += str(int(res) + resq)
        #print(z+'.'+q,f" -- B{base} -> DEC  |   ",res+resq)
        return result


    #----------------------------------------------------------------
    # Maneras más óptimas existirán para directamente convertir de cualquier base
    # a cualquier otra. Seguimos buscándolas 

    def convertirNM(self,num,bN,bM,prec=23):
        return self.convert_decbase(self.convert_to_dec(num, bN,prec), bM,prec) if bN != bM else num


    def binM(self,num : str) -> str:
        return bin(int(num)).replace('0b','') #if num  != '' else num
   

    def dec_ieee3264(self,num,mod=32): # 8<>11|127<>1023|23<>52
        if num == '':
            return '',''
        if mod==32:
            exp=127
            mnt=23
        elif mod==64:
            exp=1023
            mnt=52
        else: return '',''

        res = ''
        if num[0] == '-':
            num = num[1:]
            res += '1'
        else:
            res += '0'
        
        num = self.convert_decbase(num,2,prec=mnt-5)
        if '.' not in num:
            num += '.0'
        z,q = num.split('.')
        
        shift = len(z) - 1

        exponente = self.convert_decbase(str( exp+shift ),2)
        res += '. '+exponente+' '

        q = z[1:] + q

        idx = 0
        while (idx < mnt):
            res += q[idx] if idx < len(q) else '0'
            idx+=1
        
        return res,shift


    def bin_ieee_dec(self,num,shift):
        return self.ieee3264_2n(self.dec_ieee3264(num),shift)
    
    def ieee3264_2n(self,num,shift=0,baseT=16):
        if num in ('0.0',''):
            return '',''

        num = num.replace(' ','')

        if len(num) == 33:
            expb = 8
            ds = 127
            mntb = 23
        elif len(num) == 65:
            expb = 11
            ds = 1023
            mntb = 52
        else: return '',''
     
        #exponente = ds + int(self.convertirNM(str(num[1:expb+1]),2,baseT))
        #exT = self.convertirNM(str(num[2:expb+2]), 2, baseT)
        aux_exp = self.convert_to_dec(str(num[2:expb+2]), 2, prec=expb)
        exp_dec = int(aux_exp[:len(aux_exp)-2]) - ds


        desnorm_mnt = '1'+str(num[expb+2:expb+2+shift] + '.' + num[expb+2+shift:])
        significando = '1.'+str(num[expb+2:]) #expb+2+shift] + '.' + num[expb+2+shift:])

        mnt_dec = self.convert_to_dec(
            num = desnorm_mnt,
            base= 2 ,prec=mntb
            )

        significando_dec = self.convert_to_dec(significando, 2)
        #print(f"\nexp: {exp_dec}, significando DEC: {significando_dec}")
        #print(f"DEC: {mnt_dec}  |  HEX: {self.convertirNM(desnorm_mnt,bN=2,bM=16) }")
        return f"e:{exp_dec},s:{significando_dec}",str(mnt_dec)
        



#'''   interactivo: 
numx = input('ingrese numero: ')
#bN = int(input('de base N: '))
#bM = int(input('a base M: '))
numx = re.sub(r'[^\w.]','',numx)
print(numx)

cc = Conversor()

print(cc.convert_decbase(numx,2))
#print(cc.dec_ieee3264(numx))
ie,lz = cc.dec_ieee3264(numx,mod=32)
ie6,lz6 = cc.dec_ieee3264(numx,mod=64)

print(f" DEC -> BIN -> IEEE : {ie}")
print(cc.ieee3264_2n(ie, shift=lz , baseT=16))
print(cc.ieee3264_2n(ie, shift=lz , baseT=8))


print(cc.ieee3264_2n(ie6,shift=lz6, baseT=16))
print(cc.ieee3264_2n(ie6,shift=lz6, baseT=8))

#print(cc.dec_ieee3264(numx,mod=64))
#print(cc.convertirNM(numx,bN,bM))
#print(cc.dec_iiie32(numx))

#'''
