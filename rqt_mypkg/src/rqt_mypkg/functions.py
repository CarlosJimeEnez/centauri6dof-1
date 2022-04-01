import re
def find_block(block):
    #Funcion para verificar el tipo de bloque:
    search_const  = ['[grado]', '[cordena]', '[salid]', '[entrad]', '[grip]'] 
    constantes = [
        ['g', 'r', 'a', 'o'], ['c', 'o', 'r', 'd', 'e', 'n', 'a'], 
        ['s', 'a', 'l', 'i', 'd'], ['e', 'n', 't', 'r', 'a', 'd']
        ]
    tipo_bloques = ["grado", "coord", "salida", "entrada", "grip"]
    cantidad_tipo_bloques = [0,1,2,3,4,5]

    while(
        leters != 'grados' and leters != 'coordenada'
        and leters != 'salida' and leters != 'entrada' 
        and leters != 'grip'
        ):

        for bloque, constant, index in zip(search_const, constantes, cantidad_tipo_bloques): 
            vars = re.findall(bloque, block)
            print(vars)
            leters = constant
            for var in (vars): 
                if len(leters) > 0: 
                    for leter in leters:
                        if(str(leter) == str(var)):  
                            leters.remove(leter)
                elif(len(leters) == 0): 
                    leters = tipo_bloques[index]
                
    print(leters)
