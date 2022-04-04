import re
def find_block(block):
    #Funcion para verificar el tipo de bloque:
    search_const  = ['[grado]', '[cordena]', '[salid]', '[entrad]', '[iper]'] 
    constantes = [
        ['g', 'r', 'a', 'o'], ['c', 'o', 'r', 'd', 'e', 'n', 'a'], 
        ['s', 'a', 'l', 'i', 'd'], ['e', 'n', 't', 'r', 'a', 'd'],
        ['i','p','e','r']
        ]
    tipo_bloques = ["grado", "coord", "salida", "entrada", "grip"]
    cantidad_tipo_bloques = [0,1,2,3,4,5]
    leters = ""

    while(not leters_has_name(leters)):
        
        for bloque, constant, index in zip(search_const, constantes, cantidad_tipo_bloques): 
            if (not leters_has_name(leters)): 
                vars = re.findall(bloque, block)
                #print("bloque:{}, constante:{}, index:{}, vars:{}".format(bloque, constant, index, vars))
                leters = constant

                for var in (vars): 
                    if len(leters) > 0 and not leters_has_name(leters): 
                        for leter in leters:
                            #print("leter:{}, var:{}, cantidad bloques:{} len(leters): {}".format(leter, var, index, len(leters)))
                            if(str(leter) == str(var)):
                                leters.remove(leter)
                    elif(len(leters) == 0): 
                        leters = tipo_bloques[index]

    return leters

def leters_has_name(leters): 
    if (
        leters != 'grado'
        and leters != 'coord'
        and leters != 'salida'
        and leters != 'entrada' 
        and leters != 'grip'
        ): 
        return False
    else: 
        return True