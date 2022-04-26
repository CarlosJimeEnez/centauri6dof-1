import re
import os
import json 

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
    leters = "no name"

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

def find_name(payload): 
    '''
    Busca el nombre del archivo que viene desde el cliente
    y retorna un string con el nombre del archivo: 
    ''' 

    nombre = payload.split(":")
    nombre = re.split(r'\b', nombre[1])
    nombre = nombre[0].split('"')
    
    nombre[2] = nombre[2].replace('\\',"")

    nombre_archivo = ""
    for letra in nombre[2]: 
        nombre_archivo = nombre_archivo + letra 
    
    return nombre_archivo

def delete_empty_position(string, cadena):
    '''Borra los espacios en blanco: '''
    if len(string) < 1: 
        cadena.pop(0)
    return cadena 

def borrar_posicion_vacia(payload): 
    for value in payload : 
        if len(value) < 1: 
            payload.remove(value)
    return payload


def save_file(nombre_archivo, payload): 
    print("Estas en: " + os.getcwd())    
    os.chdir("/home/bleary/pruebas")
    with open(nombre_archivo + ".json", mode = 'w') as file:
        json.dump(payload, file)
        print("ToDo List:{}".format(payload))
    os.chdir("/home/bleary/ws_moveit/src/centauri6dof/rqt_mypkg/src")
    print("Volviendo a la carpeta archivo: " + os.getcwd())


def save_blocks_in_list(bloques): 
    '''Guardamos en una lista que luego retornamos, donde cada posicion de la lista es un tipo de bloque:  '''
    to_do_list = []
    for index, content in enumerate(bloques):
        #Si la lista tiene un elemento vacio en la primera
        #posicion lo elimina
        if content[0] == "": 
            content.pop(0)

        #Encuentra el tipo de bloque que llega desde la pagina: x
        bloque = find_block(content[0])

#---        #Bloque Grado: 
        if (bloque == 'grado'): 
            ##Creacion de las variables:  
            payload = []
            grados = {
                "tipo": "grado", 
                "angulos": [], 
                "velocidad": 0,
                "delay": 0
            } 

            for content2 in (content): 
                payload.append(re.findall('[0-9,-]+', content2))  
            
            #Borrar el primer elemento si es nulo
            while len(payload[0]) < 1 :
                payload.pop(0)

            for index, content3 in enumerate(payload): 
                if index == 6 : 
                    grados["velocidad"] = int(content3[0])
                elif index == 7: 
                    grados["delay"] = int(content3[0])
                else: 
                    grados["angulos"].append(int(content3[1]))
            to_do_list.append(grados)

#--        ##Bloque-Coord
        elif (bloque == 'coord'): 
            #print("Bloque coordenada: {}".format(content))
            #Creacion de las variables:  
            payload = []
            coordenada = {
                "tipo": "coordenada", 
                "paths": [], 
                "velocidad": 0,
                "delay": 0
            } 

            for content2 in (content): 
                payload.append(re.findall('[0-9,-]+', content2))  
            
            #Borrar el primer elemento si es nulo
            while len(payload[0]) < 1 :
                payload.pop(0)

            for index, content3 in enumerate(payload): 
                if index == 3 : 
                    coordenada["velocidad"] = int(content3[0])
                elif index == 4: 
                    coordenada["delay"] = int(content3[0])
                else: 
                    coordenada["paths"].append(int(content3[0]))
            to_do_list.append(coordenada)

#---        ##Bloq - entrada
        elif  (bloque == 'entrada'): 
            #print("Bloque entrada: {}".format(content))
            #Creacion de las variables:  
            payload = []
            entrada = {
                "tipo": "entrada", 
                "entrada_select": 0, 
                "continuar_en": 0,
                "valor_entrada": 0, 
                "delay": 0
            } 

            for content2 in (content): 
                payload.append(re.findall('[0-9,-]+', content2))  
            
            #Borrar el primer elemento si es nulo
            while len(payload[0]) < 1 :
                payload.pop(0)


            for index, content3 in enumerate(payload): 
                if index == 0 : 
                    entrada["entrada_select"] = int(content3[0])
                elif index == 1: 
                    entrada["continuar_en"] = int(content3[0])
                elif index == 2: 
                    entrada["valor_entrada"] = int(content3[0])
                else: 
                    entrada["delay"] = int(content3[0])

            to_do_list.append(entrada)

#---    # #Bloq - salida: 
        elif (bloque == "salida"): 
            #Creacion de las variables:  
            payload = [] #Es una variable temporal donde guardar los valores que llegan del bloque
            salida = {
                "tipo": "salida", 
                "salidas": [0,0,0,0,0],  
                "delay": 0
            } 

            for content2 in (content): 
                payload.append(re.findall('[0-9,-]+', content2))  
            
            #Borrar el primer elemento si es nulo
            while len(payload[0]) < 1 :
                payload.pop(0)                
        

            for index, contenido in enumerate(payload): 
                if index == 5: 
                    salida["delay"] = int(contenido[0])
                elif len(contenido) == 2:
                    salida["salidas"][index] = int(contenido[1])
            
            #reset payload: 
            payload = []
            for contenido in content: 
                payload.append(re.findall('true', contenido))
            payload.pop(0)                

            for index, contenido in enumerate(payload): 
                if len(contenido) > 0: 
                    salida["salidas"][index] = contenido[0] 
                    print("salida:{}".format(salida["salidas"]))

            to_do_list.append(salida)

# --    # #Bloq - grip
        elif(bloque == "grip"):
            #Creacion de las variables:  
            payload = [] #Es una variable temporal donde guardar los valores que llegan del bloque
            gripper = {
                "tipo": "gripper", 
                "apertura": 0,  
                "delay": 0
            } 

            for content2 in (content): 
                payload.append(re.findall('[0-9,-]+', content2))  

            while(len(payload[0]) < 1):                 
                payload.pop(0)
            
            for index, contenido in enumerate(payload): 
                if (index == 0): 
                    gripper["apertura"] = int(contenido[0])
                else: 
                    gripper["delay"] = int(contenido[0])
            
            to_do_list.append(gripper)
    
    return to_do_list 

def cargar_archivo(archivo): 
    print("Estas en: " + os.getcwd())
    with open(archivo) as file: 
        data = json.load(file)
    return str(data) 
