## Cantidad de grados max para cada articulacion: 
Artuculacion 0: -90 a 90. 
Articulacion 1:  80 a -80. 
Articulacion 2: -90 a 90. 
Articulacion 3: -75 a 75. 
Articulacion 4: -90 a 90. 
Articulacion 5: -90 a 90. 

## Algoritmos que se me acaban de ocurrir pero pueden funcionar: 
Dado el siguiente String:
``` python 
 print("String formated: {}. lengh: {}".format(payload, len(payload)))        
        #Salida: String formated: ['data: "[{\\"tipo\\":\\"grado\\",\\"m0\\":\\"18\\",\\"m1\\":\\"\\",\\"m2\\":\\"33\\",\\"m3\\":\\"\\",\\"m4\\":\\"\\\n  \\",\\"m5\\":\\"\\",\\"vel\\":\\"\\",\\"delay\\":\\"\\"',
        #  ',{\\"tipo\\":\\"entrada\\",\\"entrada_seleccionada\\"\\\n  :\\"2\\",\\"continuar_en\\":0,\\"valor_entrada\\":0,\\"delay\\":0', 
        # ']"']. lengh: 3
```

Donde cadad # es una posicion en la lista podemos hacer los siguiente: 
### Algoritmo 
- Dividimos la string entrante con split() para cada: ```}``` 
- Cada posicion de la cadena resultante la dividimos con split()  ```,``` esto formara una una nueva cadena en cada posicion de la anterior cadena. Cada una de estas nuevas cadenas representa un bloque.
```python
## Cada objeto en la lista representa un bloque (grados, coordenadas, ...) 
        bloques = []
        for index ,content in enumerate(payload):
            payload = content.split(",")
            bloques.append(payload)
```

- Buscamos el tipo a el que pertenece cada nueva cadena creada con: 
 ```if (tipo) exist: do this; else: do that``` 
 En esta funcion creamos una listas con unas letras clabes que las especificamos en re.findall() y buscamos
 esas letras en un array que especificamos en leters
```python
#Funcion para verificar el tipo de bloque:
            vars = re.findall('[grado]', content[0])
            print(vars)
            leters = ['g', 'r', 'a', 'o']
            for var in (vars): 
                if len(leters) > 0 and leters != "grados": 
                    for leter in leters:
                        if(str(leter) == str(var)):  
                            leters.remove(leter)
                else: 
                    leters = 'grados'  
            print(leters)
```

- Creamos un diccionario para cada tipo de bloque, donde rellenamos los campos del nombre y el payload.
Estructura del dicc: "tipo": "", and "payload": "" 
```python 
#Bloque-grados
            if 'data: "[{\\"tipo\\":\\"grado\\"' in content: 
                print("Bloque grados: {}".format(content))
                
                #Creacion de las variables:  
                payload = []
                grados = {
                    "tipo": "grado", 
                    "angulos": [], 
                    "velocidad": 0,
                    "delay": 0
                } 

                for content2 in (content): 
                    payload.append(re.findall('[0-9,-]+', content2))  
                payload.pop(0)
                print(payload)
                for index, content3 in enumerate(payload): 
                    if index == 6 : 
                        grados["velocidad"] = int(content3[0])
                    elif index == 7: 
                        grados["delay"] = int(content3[0])
                    else: 
                        grados["angulos"].append(content3[1])
                to_do_list.append(grados)
                #print("GRADOS: {}".format(grados))
```
- Agregamos el diccionario a una lista segun el orden de los bloques. 
```python
to_do_list.append(grados)
```
          