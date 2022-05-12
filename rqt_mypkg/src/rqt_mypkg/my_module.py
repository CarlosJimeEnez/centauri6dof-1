#!/usr/bin/env python
import sys
from ntpath import join
import os
from posixpath import split
import copy
import rospy
import rospkg
import csv
import numpy as np
import moveit_commander.robot as MICRobot
import moveit_commander.planning_scene_interface as MICPlanningSceneInterface
import moveit_commander
import moveit_commander.move_group as MICMoveGroupCommander
import moveit_msgs.msg
import geometry_msgs.msg
import time

from sensor_msgs.msg import JointState
from std_msgs.msg import String
from centauri6dof_moveit.msg import ArmJointState
from moveit_commander.conversions import pose_to_list
from random import randint
from math import pi

import json
import re
from functions import delete_empty_position, find_block, find_name, save_file, save_blocks_in_list, cargar_archivo, borrar_posicion_vacia


downA = 0

#############################CINEMATICA POSE DE EFECTOR FINAL ####################
def go_to_pose_goal (, payload):
    scale=1
    group = .group
    joint_goal = group.get_current_joint_values()
    plan = group.go(wait=True)

    coordinates_motor = [0,0,0]
    coordinates = [0,0,0]
    paylaod_string = str(payload)
    coordinates_motor = re.findall('[0-9,-]+',paylaod_string)

    for index, coordinate in enumerate(coordinates_motor):
    paylaod_string = str(coordinate)
    coordinates_motor[index] = re.findall('[0-9,-]+', paylaod_string)


    index2 = 0
    for index, payload in enumerate(coordinates_motor):
    if index%2 == 0:
        coordinates[index2] = int(coordinates_motor[index][0])
        index2 += 1
    print(coordinates)

    waypoints = []

    wpose = group.get_current_pose().pose
    wpose.position.z += coordinates[0]  # First move up (z)
    wpose.position.y += coordinates[1] #and sideways (y)
    wpose.position.x += coordinates[2]
    waypoints.append(copy.deepcopy(wpose))



    (plan, fraction) = group.compute_cartesian_path(
                                waypoints,   # waypoints to follow
                                0.01,        # eef_steps
                                0.0)         # jump_threshold


    l = len(plan.joint_trajectory.points)

    .goal.position1 = np.int16(((plan.joint_trajectory.points[l-1].positions[0]*np.pi)/180)*(32000/(2*np.pi)))
    .goal.position2 = np.int16(((plan.joint_trajectory.points[l-1].positions[1]*np.pi)/180)*(16400/(2*np.pi)))
    .goal.position3 = np.int16(((plan.joint_trajectory.points[l-1].positions[2]*np.pi)/180)*(72000/(2*np.pi)))
    .goal.position4 = np.int16(((plan.joint_trajectory.points[l-1].positions[3]*np.pi)/180)*(3200/(2*np.pi)))
    .goal.position5 = np.int16(((plan.joint_trajectory.points[l-1].positions[4]*np.pi)/180)*(14400/(2*np.pi)))
    .goal.position6 = np.int16(((plan.joint_trajectory.points[l-1].positions[5]*np.pi)/180)*(3000/(2*np.pi)))
    #Manda los valores a el arduino
    .pub2.publish(.goal)


    print(plan)
    #print(.goal)
    #print(plan.joint_trajectory.points[l-1].positions[0])
    #print(plan.joint_trajectory.points[l-1].positions[1])
    #print(format(wpose))                
    group.execute(plan, wait=True)
    group.stop

    #return plan, fraction


def go_to_vertical_up_start (verti):

    group = .group
    plan = group.go(wait=True)
    joint_goal = group.get_current_joint_values()


    scale = 1
    v = str(verti)
    vert = re.findall('[0-9,-]+', v)
    global vertical
    vertical = int(vert[0])

    global downA
    waypoints = []

    print(vertical)

    while(downA<0):
        if vertical == 1:   
            downA = downA + 2
            print(downA)
            wpose = group.get_current_pose().pose
            wpose.position.z += scale *downA
            waypoints.append(copy.deepcopy(wpose))
        
            (plan, fraction) = group.compute_cartesian_path(
                                            waypoints,  
                                            0.01,        
                                            0.0)  
            time.sleep(0.50)
        else:

            break
        
        
    print (plan)
    group.execute(plan, wait=True)

def go_to_vertical_up_finish(, verti):
    global vertical
    vertical = 0
    vertical = str(verti)
    verticals = re.findall('[0-9,-]+', vertical)
    # global finVertical = int(verticals[0])

    print(vertical)

    group = .group
    join_goal = group.get_current_joint_values()



    def go_to_vertical_down_start (, verti):

    group = .group
    plan = group.go(wait=True)
    joint_goal = group.get_current_joint_values()


    scale = 1
    v = str(verti)
    vert = re.findall('[0-9,-]+', v)
    global vertical
    vertical = int(vert[0])
    global downA

    waypoints = []

    while(downA>-90):
        if vertical == 1:
            downA = downA - 2
            print(downA)
            wpose = group.get_current_pose().pose
            wpose.position.z += scale *downA
            waypoints.append(copy.deepcopy(wpose))

            (plan, fraction) = group.compute_cartesian_path(
                                            waypoints,  
                                            0.01,        
                                            0.0)  
            time.sleep(0.5)
        else:

            break


    group = .group
    group.execute(plan, wait=True)


def go_to_vertical_down_finish (, verti):
    global vertical
    vertical = 0
    vertical = str(verti)
    verticals = re.findall('[0-9,-]+', vertical)
    verticals= int(verticals[0])
    print(verticals)



    group = .group
    join_goal = group.get_current_joint_values()


    def joints_changes():

    #group = .group
    #joint_goal = group.get_current_joint_values()

    for i in xrange(0,6):
        .arr_ShowSl[i].setText(str(.arr_sl[i].value()))
        #joint_goal[i] = (.arr_sl[i].value()*np.pi)/180

    #group.go(joint_goal, wait=True)
    #group.stop()


    # Permite el movimiento del robot con los sliders presionando
    # el boton play
def _Send_joints_teleoperation(, payload):
    group = .group
    joint_goal = group.get_current_joint_values()
    print("Llegada desde la pagina: {}".format(payload))
    #Salida: "[\"64\",\"50\",{\"setpoint\":0},{\"setpoint\":0},{\"setpoint\":0},{\"setpoint\":0}]"

    ### Funcion donde se convierte de JSON a string los valores de entrada:
    setpoints_motor = [0,0,0,0,0,0]
    setpoints = [0,0,0,0,0,0]
    paylaod_string = str(payload)
    #Encuentra los valores int() del str de entrada:
    setpoints_motor = re.findall('[0-9,-]+',paylaod_string)

    for index, setpoint in enumerate(setpoints_motor):
        paylaod_string = str(setpoint)
        setpoints_motor[index] = re.findall('[0-9,-]+', paylaod_string)
        #Salida:  [['64'], [','], ['10'], [','], ['60'], [','], ['-58'], [','], ['67'], [','], ['58']]
    print("setpoint motors: {}".format(setpoints_motor)) #Valores de los sliders
    print("setpoint motors: {}".format(setpoints_motor[1])) #Valores de los sliders

    #Conversion a int del paylaod:
    index2 = 0
    for index, payload in enumerate(setpoints_motor):
        if index%2 == 0:
            setpoints[index2] = int(setpoints_motor[index][0])
            index2 += 1
    #setpoints -> valores int
    print("setpoint motors: {}".format(setpoints)) #Valores de los sliders

    #Guarda los valores de los sliders del widget en la variable de la simulacion:
    for i in xrange(0,6):
        joint_goal[i] = (setpoints[i]*(np.pi))/180
        print((arr_sl[i].value()*np.pi)/180)
    #Mappea el valor para la simulacion:
    #90 - 180 y 90 - 1.57:
    #joint_goal[0] = ((setpoints_motor[0]*np.pi)/180)

    ##### Arduino #####
    goal.position1 = np.int16(((setpoints[0]*np.pi)/180)*(32000/(2*np.pi)))
    goal.position2 = np.int16(((setpoints[1]*np.pi)/180)*(16400/(2*np.pi)))
    goal.position3 = np.int16(((setpoints[2]*np.pi)/180)*(72000/(2*np.pi)))
    goal.position4 = np.int16(((setpoints[3]*np.pi)/180)*(3200/(2*np.pi)))
    goal.position5 = np.int16(((setpoints[4]*np.pi)/180)*(14400/(2*np.pi)))
    goal.position6 = np.int16(((setpoints[5]*np.pi)/180)*(3000/(2*np.pi)))
    #Manda los valores a el arduino
    pub2.publish(goal)

    #Mueve la simulacion:
    group.go(joint_goal, wait=True)
    group.stop()

    current_joints = group.get_current_joint_values()

#Regresa a 0 los valores de los sliders: #####################################################
def _Center_joints_teleoperation(payload):
    group = group
    joint_goal = group.get_current_joint_values()

        ### Funcion donde se convierte de JSON a string los valores de entrada:
    setpoints_motor = [0,0,0,0,0,0]
    setpoint = [0,0,0,0,0,0]
    paylaod_string = str(payload)
    #Encuentra los valores int() del str de entrada:
    setpoints_motor = re.findall('[0-9,-]+',paylaod_string)


    for index, setpoint in enumerate(setpoints_motor):
        paylaod_string = str(setpoint)
        setpoints_motor[index] = re.findall('[0-9,-]+', paylaod_string)
        #Salida:  [['64'], [','], ['10'], [','], ['60'], [','], ['-58'], [','], ['67'], [','], ['58']]
    # print("setpoint motors: {}".format(setpoints_motor)) #Valores de los sliders
    # print("setpoint motors: {}".format(setpoints_motor[1])) #Valores de los sliders

    #Conversion a int del paylaod:
    index2 = 0
    for index, payload in enumerate(setpoints_motor):
        if index%2 == 0:
            setpoints[index2] = int(setpoints_motor[index][0])
            index2 += 1
    #setpoints -> valores int
    print("setpoint motors: {}".format(setpoint)) #Valores de los sliders


    for i in xrange(0,6):
        arr_sl[i].setValue(0)
        ## joint_goal[i] = (.arr_sl[i].value()*np.pi)/180
        joint_goal[i] = (setpoint[i]*(np.pi))/180

    goal.position1 = np.int16(((setpoint[0]*np.pi)/180)*(32000/(2*np.pi)))
    goal.position2 = np.int16(((setpoint[1]*np.pi)/180)*(16400/(2*np.pi)))
    goal.position3 = np.int16(((setpoint[2]*np.pi)/180)*(72000/(2*np.pi)))
    goal.position4 = np.int16(((setpoint[3]*np.pi)/180)*(3200/(2*np.pi)))
    goal.position5 = np.int16(((setpoint[4]*np.pi)/180)*(14400/(2*np.pi)))
    goal.position6 = np.int16(((setpoint[5]*np.pi)/180)*(3000/(2*np.pi)))

    pub2.publish(goal)

    group.go(joint_goal, wait=True)
    group.stop()
###---------------------------------------------------LLEGADA DE LOS BLOQUES DE PAGINA------------------------

def format_secuencias(payload):
    payload = str(payload)
    payload = payload.split("}")
    payload.pop() #--Elimina el ultimo elemento de la lista.
    print(payload)

    ## Cada objeto en la lista representa un bloque (grados, coordenadas, ...)
    bloques = []
    for index ,content in enumerate(payload):
        payload = content.split(",")
        bloques.append(payload)

    ## Busqueda del tipo de bloques en la lista bloques:
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

        ##################################################Aca termina el formate de los bloques ##############################################################       

    print("ToDo List:{}".format(to_do_list))

    for bloque in to_do_list:
        if bloque["tipo"] == "grado":
            group = group
            joint_goal = group.get_current_joint_values()

            for i in xrange(0,6):
                joint_goal[i] = (bloque["angulos"][i]*(np.pi))/180
                print((arr_sl[i].value()*np.pi)/180)
            ##bloque["velocidad"]

            goal.position1 = np.int16(((bloque["angulos"][0]*np.pi)/180)*(32000/(2*np.pi)))
            goal.position2 = np.int16(((bloque["angulos"][1]*np.pi)/180)*(16400/(2*np.pi)))
            goal.position3 = np.int16(((bloque["angulos"][2]*np.pi)/180)*(72000/(2*np.pi)))
            goal.position4 = np.int16(((bloque["angulos"][3]*np.pi)/180)*(3200/(2*np.pi)))
            goal.position5 = np.int16(((bloque["angulos"][4]*np.pi)/180)*(14400/(2*np.pi)))
            goal.position6 = np.int16(((bloque["angulos"][5]*np.pi)/180)*(3000/(2*np.pi)))

            pub2.publish(goal)
            group.go(joint_goal, wait=True)
            group.stop()

        elif bloque["tipo"] == "coordenada":
            group = group
            joint_goal = group.get_current_joint_values()

            for i in xrange(0,3):
                joint_goal[i] = (bloque["paths"][i]*(np.pi))/180
                print((arr_sl[i].value()*np.pi)/180)

            pose_goal = geometry_msgs.msg.Pose()
            pose_goal.orientation.w = 100
            pose_goal.position.x = (bloque["paths"][0])
            pose_goal.position.y = (bloque["paths"][1])
            pose_goal.position.z = (bloque["paths"][2])
            group.set_pose_target(pose_goal)
            group.go(joint_goal, wait=True)
            group.stop()

            plan = group.go(joint_goal, wait=True)
            group.stop()

            group.clear_pose_targets()
            current_pose = group.get_current_pose().pose


def ejecutar_archivo(archivo): 
    '''Ejecuta las ordenes de un archivo cargado desde la pag: '''
    print("LLegada del archivo: {}".format(archivo))
    archivo = str(archivo)
    archivo = archivo.split('"')
    #En archivo tenemos el lugar en donde se encuentra el documento a buscar:
    archivo = archivo[2].replace("\\", "")

    archivo_cargado = cargar_archivo(archivo)
    #Eliminamos una "u" que no se de donde aparecen :c: 
    archivo_cargado = archivo_cargado.replace("u", "")

    #Eliminamos las "[]" del inicio y fin para crear un diccionario: 
    archivo_cargado = archivo_cargado.replace(archivo_cargado[0], "")
    archivo_cargado = archivo_cargado.replace(archivo_cargado[-1], "")
    
    archivo_cargado = archivo_cargado.split("}")
    archivo_cargado.pop() #--Elimina el ultimo elemento de la lista porque viene vacio. 

    ## Cada objeto en la lista representa un bloque (grados, coordenadas, ...) 
    to_do_list = []
    bloques = []
    for index ,content in enumerate(archivo_cargado):
        archivo_cargado = content.split(",")
        bloques.append(archivo_cargado)
    print("Bloques: {}".format(bloques))
    
    for bloque in bloques: 
        for index, content in enumerate(bloque): 
            #Borramos los espacios en blanco: 
            if len(content) < 1: 
                bloque.pop(index)
            #COORDENADA: 
            if content ==  " 'tipo': 'coordenada'": 
                #Para acceder a cada bloque usamos la variable bloque: 
                # luego creamos un diccionario que se guardara en una lista: 
                
                ##Creacion de las variables:  
                payload = []
                coordenada = {
                    "tipo": "coordenada", 
                    "paths": [], 
                    "velocidad": 0,
                    "delay": 0
                } 
                for content in bloque: 
                    payload.append(re.findall('[0-9,-]+', content))  
                
                #Eliminamos los espacios en blanco:
                payload = borrar_posicion_vacia(payload)
                
                for index, valores in enumerate(payload): 
                    if index == 0 : 
                        coordenada["delay"] = int(valores[0]) 
                    elif index == 4: 
                        coordenada["velocidad"] = int(valores[0])
                    else: 
                        coordenada["paths"].append(int(valores[0]))
                to_do_list.append(coordenada)
            
            ## GRADOS:     
            elif content == " 'tipo': 'grado'": 
                #Para acceder a cada bloque usamos la variable bloque: 
                # luego creamos un diccionario que se guardara en una lista: 
                
                ##Creacion de las variables:  
                payload = []
                grados = {
                    "tipo": "grado", 
                    "angulos": [], 
                    "velocidad": 0, 
                    "delay": 0,
                } 

                for content in bloque: 
                    payload.append(re.findall('[0-9,-]+', content))  
                #Eliminamos los espacios en blanco: 
                payload = borrar_posicion_vacia(payload)

                for index, valores in enumerate(payload): 
                    if index == 0 : 
                        grados["delay"] = int(valores[0]) 
                    elif index == 7: 
                        grados["velocidad"] = int(valores[0])
                    else: 
                        grados["angulos"].append(int(valores[0]))
                to_do_list.append(grados)
            
            ## ENTRADA: 
            elif content == " 'tipo': 'entrada'": 
                #Para acceder a cada bloque usamos la variable bloque: 
                # luego creamos un diccionario que se guardara en una lista: 
                
                ##Creacion de las variables:  
                payload = []
                entrada = {
                    "tipo": "entrada", 
                    "valor_entrada": [], 
                    "entrada_selec": 0, 
                    "continuar_en": 0,
                    "delay": 0 
                } 

                for content in bloque: 
                    payload.append(re.findall('[0-9,-]+', content))  
                #Eliminamos los espacios en blanco: 
                payload = borrar_posicion_vacia(payload)

                for index, valores in enumerate(payload): 
                    if index == 0 : 
                        entrada["delay"] = int(valores[0]) 
                    elif index == 1: 
                        entrada["entrada_selec"] = int(valores[0])
                    elif index == 2: 
                        entrada["continuar_en"] = int(valores[0])
                    else: 
                        entrada["valor_entrada"] = int(valores[0])
                to_do_list.append(entrada)

            ## SALIDA: 
            elif content == " 'tipo': 'salida'": 
                ##Creacion de las variables:  
                payload = []
                salida = {
                    "tipo": "salida", 
                    "salidas": [],
                    "delay": 0 
                } 

                for content in bloque: 
                    payload.append(re.findall('[0-9,-]+', content))  
                for index, valores in enumerate(payload): 
                    if index == 0: 
                        salida["delay"] == int(valores[0]) 
                    elif index == 6: 
                        pass
                    else: 
                        if len(valores) > 0:  
                            salida["salidas"].append(int(valores[0]))
                        else: 
                            salida["salidas"].append(int(1))                    
                to_do_list.append(salida)
            
            ##GRIPPER: 
            elif content == " 'tipo': 'gripper'": 
                ##Creacion de las variables:  
                payload = []
                gripper = {
                    "tipo": "gripper", 
                    "apertura": 0,
                    "delay": 0 
                }                

                for content in bloque: 
                    payload.append(re.findall('[0-9,-]+', content))  
                #Eliminamos los espacios en blanco: 
                payload = borrar_posicion_vacia(payload)

                for index, valor in enumerate(payload): 
                    if index == 0: 
                        gripper["delay"] = int(valor[0]) 
                    else: 
                        gripper["apertura"] = int(valor[0])
                
                to_do_list.append(gripper)


    print ("llegada de datos ejecutar {} " .format(to_do_list))

    ## Ejecucion del tipo de cada bloque::: 
    for bloque in to_do_list:
        ## ---- GRADO: 
        if bloque["tipo"] == "grado":
            group = group
            joint_goal = group.get_current_joint_values()

            for i in xrange(0,6):
                joint_goal[i] = (bloque["angulos"][i]*(np.pi))/180
                print((arr_sl[i].value()*np.pi)/180)
            ##bloque["velocidad"]

            goal.position1 = np.int16(((bloque["angulos"][0]*np.pi)/180)*(32000/(2*np.pi)))
            goal.position2 = np.int16(((bloque["angulos"][1]*np.pi)/180)*(16400/(2*np.pi)))
            goal.position3 = np.int16(((bloque["angulos"][2]*np.pi)/180)*(72000/(2*np.pi)))
            goal.position4 = np.int16(((bloque["angulos"][3]*np.pi)/180)*(3200/(2*np.pi)))
            goal.position5 = np.int16(((bloque["angulos"][4]*np.pi)/180)*(14400/(2*np.pi)))
            goal.position6 = np.int16(((bloque["angulos"][5]*np.pi)/180)*(3000/(2*np.pi)))

            pub2.publish(goal)
            group.go(joint_goal, wait=True)
            group.stop()

        ## ---- COORDENADA: 
        elif bloque["tipo"] == "coordenada":
            group = group
            joint_goal = group.get_current_joint_values()

            for i in xrange(0,3):
                joint_goal[i] = (bloque["paths"][i]*(np.pi))/180
                print((arr_sl[i].value()*np.pi)/180)

            pose_goal = geometry_msgs.msg.Pose()
            pose_goal.orientation.w = 100
            pose_goal.position.x = (bloque["paths"][0])
            pose_goal.position.y = (bloque["paths"][1])
            pose_goal.position.z = (bloque["paths"][2])
            group.set_pose_target(pose_goal)
            group.go(joint_goal, wait=True)
            group.stop()

            plan = group.go(joint_goal, wait=True)
            group.stop()

            group.clear_pose_targets()
            current_pose = .group.get_current_pose().pose

        elif bloque["tipo"] == "salida":
            salidas = "" 
            print("Ejecutando bloque: SALIDA.")
            #Selecciona la salida que tiene valor 1 y la publica hacia el Micro
            for index, salida in enumerate(bloque["salidas"]): 
                if salida == 1: 
                    salidas = salidas + str(index)
                pub = rospy.Publisher("salidasDigitales", String, queue_size=10)
                rospy.Rate(20)
                pub.publish(salidas)



#---- Guardar archivo:: 
def guardar_archivo(payload): 
    print("Llegada desde la pagina{}".format(payload))
    payload = str(payload)
    payload = payload.split("}")
    payload.pop() #--Elimina el ultimo elemento de la lista. 


    ## Cada objeto en la lista representa un bloque (grados, coordenadas, ...) 
    bloques = []
    for index ,content in enumerate(payload):
        payload = content.split(",")
        bloques.append(payload)

    #Busqueda del nombre: 
    nombre_archivo = find_name(bloques[0][0])
    print("Nombre: {}".format(nombre_archivo))

    #ELiminamos la primera pos del primer bloque para 
    # eliminar el dato del nombre y quedarnos solo con el
    # cont: 
    bloques[0].pop(0)

    ## Busqueda del tipo de bloques en la lista bloques: 
    to_do_list = []
    for index, content in enumerate(bloques):                 
        delete_empty_position(content[0], content)
        bloque = find_block(content[0])

    #---    #Bloque Grado: 
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

    # -- Guardar el archivo:   
    save_file(nombre_archivo, to_do_list)


#Confuguracin MoveitGroup: 
robot = MICRobot.RobotCommander()
scene = MICPlanningSceneInterface.PlanningSceneInterface()
group_name = "centauri6dof_arm"
group = MICMoveGroupCommander.MoveGroupCommander(group_name)

#Publicador a Moveit: 
display_trajectory_publisher = rospy.Publisher(
    '/move_group/display_planned_path',
    moveit_msgs.msg.DisplayTrajectory,
    queue_size=20
)

# We can get the name of the reference frame for this robot:
planning_frame = group.get_planning_frame()
print ("============ Reference frame: %s" % planning_frame)

# We can also print the name of the end-effector link for this group:
eef_link = group.get_end_effector_link()
print ("============ End effector: %s" % eef_link)

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print ("============ Robot Groups:", robot.get_group_names())

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print ("============ Printing robot state")
print (robot.get_current_state())
print ("")

box_name = ''
robot = robot
scene = scene
group = group
display_trajectory_publisher = display_trajectory_publisher
planning_frame = planning_frame
eef_link = eef_link
group_names = group_names

############# INICIO DEL GUI ##########
rospy.Subscriber("/move_group/fake_controller_joint_states", JointState)
moveit_commander.roscpp_initialize(sys.argv)
#rospy.init_node('/move_group/fake_controller_joint_states', JointState, anonymous=True)

### Nodos subscriptos:
rospy.Subscriber('send_home', String, _Center_joints_teleoperation)
rospy.Subscriber('gripper', String, _fcn_gripper)
rospy.Subscriber('end_efector', String, go_to_pose_goal)
rospy.Subscriber('/secuencia_mov', String, format_secuencias)
rospy.Subscriber('/vertical_start', String, go_to_vertical_up_start)
rospy.Subscriber('vertical_finish', String, go_to_vertical_up_finish)
rospy.Subscriber('/vertical_down_start', String, go_to_vertical_down_start)
rospy.Subscriber('/vertical_down_finish', String, go_to_vertical_down_finish)
rospy.Subscriber('/guardar_archivo', String, guardar_archivo)
#Ejecuta el programa que llega desde la pagina de ejecutar: 
rospy.Subscriber('/ejecutar_archivo', String, ejecutar_archivo)
