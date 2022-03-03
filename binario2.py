def pasarBaseMayor10(lista, base, baseT):
    pass

def pasarBaseMenor10(lista, base, baseT):
    def pasarAMenor(lista, base, baseT):
        num = ''
        for i in range(0, len(lista)):
            if i == 0:
                lista[i] = int(lista[i])
                while (lista[i] >= baseT):
                    num = num + str(int(lista[i] % baseT))
                    lista[i] = lista[i] / baseT

                num = num + str(int(lista[i]))

            if i==1:
                num = num + '.'
                lista[i] = float('0.' + lista[i])
                for x in range (0, 8):
                    aux = lista[i] * baseT
                    lista[i] = aux
                    num = num + str(int(aux))

        
        return num[::-1]


    if(base > baseT):
        return pasarAMenor(lista, base, baseT)

def pasarBase(lista, base, baseT):
    numero = ''
    

def definirDecimal(num):
    if(num.find('.')):
        num = num.split('.')
    
    else:
        num=[num]

    return num
    if(baseT > 10):
        pasarBaseMayor10(lista, base, baseT)
    else:
        return pasarBaseMenor10(lista, base, baseT)


lista = definirDecimal('32.43')
num = pasarBase(lista, 10, 2)
print('FINAL')
print(num)
 