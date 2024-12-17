import re
import ast
from datetime import datetime
import os
from colorama import Fore, Back, Style, init

def obtener_fecha_actual():
    return datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

def quitar_colores(texto_coloreado):
    return re.sub(r'\x1b\[[0-9;]*[mG]', '', texto_coloreado)

def guardar_partida(tablero, player_1, player_2, ficha_player1, ficha_player2, jugador_actual, carpeta='Partidas'):
    fecha_actual = obtener_fecha_actual()

    # Evita que se agreguen códigos de color al nombre del archivo
    # strip para eliminar salto de linea
    player_1=quitar_colores(player_1).strip()
    player_2=quitar_colores(player_2).strip()
    jugador_actual=quitar_colores(jugador_actual).strip()
    ficha_player1=quitar_colores(ficha_player1).strip()
    ficha_player2 = quitar_colores(ficha_player2).strip()

    nombre_tablero = f"{player_1}_vs_{player_2}_{fecha_actual}"
    nombre_archivo = f"{carpeta}/partida_{nombre_tablero}.txt"

    with open(nombre_archivo, 'w') as file:
        file.write(f"{player_1}\n")
        file.write(f"{player_2}\n")
        file.write(f"{ficha_player1}\n")
        file.write(f"{ficha_player2}\n")
        file.write(f"{jugador_actual}\n")
        file.write(str(tablero))

def cargar_partida(nombre_archivo):
    with open(f'Partidas/{nombre_archivo}', 'r') as file:
        player_1=file.readline().strip()
        player_2=file.readline().strip()
        ficha_player1=file.readline().strip()
        ficha_player2=file.readline().strip()
        jugador_actual = file.readline().strip()
        board=ast.literal_eval(file.readline()) #para pasar de string a una matriz con los valores originales
    return player_1,player_2,ficha_player1,ficha_player2,jugador_actual,board

def Cargar():
    global archivos
    print(Fore.LIGHTCYAN_EX + 'Elija una partida guardada: ' + Fore.RESET)
    carpeta='Partidas'
    archivos = os.listdir(carpeta)#una lista con los archivos de la carpeta
    if not archivos:
        print("No hay partidas guardadas.")
        return
    i=1
    for archivo in archivos:
        print(f'{i}:',archivo)
        i+=1
    return archivos
