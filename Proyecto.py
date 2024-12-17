import sys
import Guardados
from colorama import Fore, Back, Style, init
Guardados.os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

pygame.init()
pygame.mixer.init()
init(autoreset=True)
pygame.mixer.music.load('music_gameplay.mp3')
pygame.mixer.music.play(-1)

while True:
    volumen_input = input("Ingrese su volumen deseado del 0 al 100: ")
    if volumen_input.isdigit():
        volumen_input = int(volumen_input)
        if 0 <= volumen_input <= 100:
            break
    print(Fore.RED + "Entrada no válida. Debe ser un número entero del 0 al 100. Inténtalo de nuevo." + Fore.RESET)
volumen = volumen_input / 100
pygame.mixer.music.set_volume(volumen)

def music():
    pygame.init()
    pygame.mixer.init()
    init(autoreset=True)
    pygame.mixer.music.load('music_gameplay.mp3')
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1)

def names_players():
    player_1=input('Ingrese Nombre del Jugador 1: ')
    player_1=Fore.RED + player_1 + Fore.RESET
    player_1_ficha=' X '
    player_2=input('Ingrese Nombre del Jugador 2: ')
    player_2_ficha=' O '
    player_2=Fore.YELLOW + player_2 + Fore.RESET
    return player_1, player_1_ficha, player_2, player_2_ficha

def board_global():
    global rows,columns,board
    rows=6
    columns=7
    board=[['\t',1,'\t',2,'\t',3,'\t',4,'\t',5,'\t',6,'\t',7],
        [' '*2,' ---'*7,' -'],
        [6,' ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|'],
        [' '*2,' ---'*7,' -'],
        [5,' ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|'],
        [' '*2,' ---'*7,' -'],
        [4,' ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|'],
        [' '*2,' ---'*7,' -'],
        [3,' ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|'],
        [' '*2,' ---'*7,' -'],
        [2,' ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|'],
        [' '*2,' ---'*7,' -'],
        [1,' ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|','   ','|'],
        ['-'*32]]
    return board

def obtener_numero_entero_en_rango(mensaje,limite,board,jugador_actual):
    ficha_player1=' X '
    ficha_playeiiksr2=' O '
    while True:
        entrada = input(mensaje)
        if entrada.upper()=='E':# salir al menu
            Inicio(board)
        elif entrada.upper()=='S':# guardar tablero
            Guardados.guardar_partida(board,player_1,player_2,ficha_player1,ficha_player2,jugador_actual,carpeta='Partidas')
            print(Fore.LIGHTCYAN_EX + '¡Partida guardada!' + Fore.RESET)
            Inicio(board)
        elif entrada.isdigit():
            numero = int(entrada)
            if 1 <= numero <= limite:
                return numero
            print(Fore.RED + f"El numero tiene que estar en el intervalo [1,{limite}]: " + Fore.RESET)
        else:
            print(Fore.RED + f"El numero tiene que estar en el intervalo [1,{limite}]: " + Fore.RESET)

def print_board(board):
    for fila in board:
        for elemento in fila:
            if isinstance(elemento, int):
                # isinstance() es una funcion que sirve para saber si elemento es un entero(True) o no(False)
                print(Style.BRIGHT + str(elemento), end='')  # Coloca en negrita los numeros
            elif elemento==' X ':
                print(Fore.RED + elemento + Fore.RESET, end='')
            elif elemento==' O ':
                print(Fore.YELLOW + elemento + Fore.RESET, end='')
            elif elemento==' X *':
                print(Fore.GREEN + elemento.replace('*','') + Fore.RESET, end='')
            elif elemento==' O *':
                print(Fore.GREEN + elemento.replace('*', '') + Fore.RESET, end='')
            else:
                print(Fore.BLUE + str(elemento), end='')  # Pinta la matriz de azul
        print()

def search_colocar(player_move,ficha,board):
    espacio = player_move + 1
    player_move_new = player_move + espacio
    filas_specific = (rows * 2) + 2
    lista_filas=[i for i in range(2,filas_specific,2)] # 2,4,6,8,10,12
    lista_filas_invertida=lista_filas[::-1] # 12,10,8,6,4,2
    full_columns=0 #contador hasta que la columna este llena
    for m in lista_filas_invertida: # filas m toma 12,10,8,6,4,2
        if board[m][player_move_new]=='   ':
            board[m][player_move_new]=ficha
            return 'vacio'
        elif (board[m][player_move_new]==' X ' or board[m][player_move_new]==' O '):
            full_columns+=1
            if full_columns==rows:#que sea igual a 6
                return 'repeat'
        elif m>=4:# 12,10,8,6,4
            if (board[m][player_move_new]==' X ' or board[m][player_move_new]==' O ') and (board[m-2][player_move_new]=='   '):
                board[m-2][player_move_new]=ficha
                return 'abajo y arriba'

def player1_play(player,board,ficha_player):
    global ficha_player1
    player1_move=obtener_numero_entero_en_rango(f'Digite Jugada del Jugador {player} o Salir (E) o Guardar (S): ',7,board,player)
    ficha_player1=' X '
    board_modidicado=search_colocar(player1_move, ficha_player,board)
    if board_modidicado == 'repeat':
        print(Fore.RED + f'La columna {player1_move} esta llena; por favor eligir otra columna.' + Fore.RESET)
        player1_move_new=obtener_numero_entero_en_rango(f'Digite Jugada del Jugador {player} o Salir (E) o Guardar (S): ',7,board,player)
        search_colocar(player1_move_new, ficha_player,board)
        print_board(board)
    else:
        print_board(board)

def player2_play(player,board,ficha_player):
    global ficha_player2
    player2_move = obtener_numero_entero_en_rango(f'Digite Jugada del Jugador {player} o Salir (E) o Guardar (S): ',7,board,player)
    ficha_player2=' O '
    board_modidicado=search_colocar(player2_move, ficha_player,board)
    if board_modidicado == 'repeat':
        print(Fore.RED + f'La columna {player2_move} esta llena; por favor eligir otra columna.' + Fore.RESET)
        player2_move_new=obtener_numero_entero_en_rango(f'Digite Jugada del Jugador {player} o Salir (E) o Guardar (S): ',7,board,player)
        search_colocar(player2_move_new, ficha_player,board)
        print_board(board)
    else:
        print_board(board)

def win_player(board,ficha_player):
    global filas_specific,columns_specific,lista_filas,lista_columns
    aliniar=4
    for i in lista_filas:
        for j in lista_columns:
            if j<=lista_columns[columns-aliniar]: #busqueda horizontal
                if board[i][j]==ficha_player and board[i][j+2]==ficha_player and board[i][j+4]==ficha_player and board[i][j+6]==ficha_player:
                    board[i][j]=board[i][j+2]=board[i][j+4]=board[i][j+6]=ficha_player+"*"
                    print_board(board)
                    return 'Win'
    for i in lista_filas:
        for j in lista_columns:
            if i<=lista_filas[rows-aliniar]: #busqueda vertical
                if board[i][j]==ficha_player and board[i+2][j]==ficha_player and board[i+4][j]==ficha_player and board[i+6][j]==ficha_player:
                    board[i][j] = board[i+2][j] = board[i+4][j] = board[i+6][j] = ficha_player + "*"
                    print_board(board)
                    return 'Win'
    for i in lista_filas:
        for j in lista_columns:
            if j<=lista_columns[columns-aliniar] and i<=lista_filas[rows-aliniar]: #busqueda diagonal izquierdo
                if board[i][j]==ficha_player and board[i+2][j+2]==ficha_player and board[i+4][j+4]==ficha_player and board[i+6][j+6]==ficha_player:
                    board[i][j] = board[i + 2][j + 2] = board[i + 4][j + 4] = board[i + 6][j + 6] = ficha_player + "*"
                    print_board(board)
                    return 'Win'
    for i in lista_filas:
        for j in lista_columns:
            if j>=lista_columns[columns-aliniar] and i<=lista_filas[rows-aliniar]: #busqueda diagonal derecho
                if board[i][j]==ficha_player and board[i+2][j-2]==ficha_player and board[i+4][j-4]==ficha_player and board[i+6][j-6]==ficha_player:
                    board[i][j] = board[i + 2][j - 2] = board[i + 4][j - 4] = board[i + 6][j - 6] = ficha_player + "*"
                    print_board(board)
                    return 'Win'
    return 'No win'

def gameplay(board,player_1,player_2, ficha_player1, ficha_player2):
    global filas_specific,columns_specific,lista_filas,lista_columns,rows,columns
    rows=6
    columns=7
    print_board(board)
    filas_specific = (rows * 2) + 2
    lista_filas = [i for i in range(2, filas_specific, 2)] # 2,4,6,8,10,12
    columns_specific = (columns * 2) + 3
    lista_columns = [i for i in range(3, columns_specific, 2)] # 3,5,7,9,11,13,15
    empieza_turnos=1
    for i in lista_filas:
        for j in lista_columns:
            if board[i][j] == ' X ' or board[i][j] == ' O ' or board[i][j] == '   ':
                if empieza_turnos % 2 != 0:
                    player1_play(player_1,board,ficha_player1)
                    if win_player(board,ficha_player1)=='Win':
                        pygame.mixer.music.stop()
                        print('FELICIDADES',player_1,'GANASTE')
                        pygame.mixer.init()
                        pygame.mixer.music.load('music_win.mp3')
                        pygame.mixer.music.set_volume(volumen)
                        pygame.mixer.music.play()
                        input('Presione enter para salir al menu inicial')
                        while pygame.mixer.music.get_busy():
                            pass
                        music()
                        Inicio(board)
                elif empieza_turnos % 2 == 0:
                    player2_play(player_2,board,ficha_player2)
                    if win_player(board,ficha_player2)=='Win':
                        pygame.mixer.music.stop()
                        print('FELICIDADES',player_2,'GANASTE')
                        pygame.mixer.init()
                        pygame.mixer.music.load('music_win.mp3')
                        pygame.mixer.music.set_volume(volumen)
                        pygame.mixer.music.play()
                        input('Presione enter para salir al menu inicial')
                        while pygame.mixer.music.get_busy():
                            pass
                        music()
                        Inicio(board)
                empieza_turnos+=1
    print('EMPATE, NINGUN JUGADOR A GANADO')
    return

def Inicio(board):
    global player_1,player_2
    print(Fore.YELLOW + 'Bienvenidos a Four In Row del Grupo The Warriors of Utec')
    print(Fore.YELLOW + '*'*25 + ' Menu ' + '*'*25)
    print(Fore.CYAN + '1: Nuevo Juego')
    print(Fore.GREEN + '2: Carga Juego')
    print(Fore.RED + '3: Salir' + Fore.RESET)
    option=obtener_numero_entero_en_rango('Digite Opcion: ',3,board,'')
    if option==1:
        player_1, ficha_player1, player_2, ficha_player2 = names_players()
        board = board_global()
        gameplay(board, player_1, player_2, ficha_player1, ficha_player2)
    elif option==2:
        archivos=Guardados.Cargar()
        option=obtener_numero_entero_en_rango('Digite Opcion: ',len(archivos),board,'')
        player_1, player_2, ficha_player1, ficha_player2,jugador_actual, board = Guardados.cargar_partida(archivos[option-1])
        player_1 = Fore.RED + player_1 + Fore.RESET
        player_2 = Fore.YELLOW + player_2 + Fore.RESET
        # Ahora comprobamos quién es el jugador actual y ajustamos el turno inicial
        print_board(board)
        if jugador_actual == player_1:
            gameplay(board, player_1, player_2,ficha_player1,ficha_player2)
        elif jugador_actual == player_2:
            gameplay(board, player_2, player_1,ficha_player1,ficha_player2)

    elif option==3:
        print('¡Gracias por jugar!')
        sys.exit()
board=board_global()
Inicio(board)

