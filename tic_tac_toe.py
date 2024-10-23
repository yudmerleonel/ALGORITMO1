import tkinter as tk
from tkinter import messagebox

# Estado inicial del tablero: lista de 9 elementos (' ' para vacío)
tablero = [' ' for _ in range(9)]

def mostrar_tablero(tablero):
    print(f"{tablero[0]} | {tablero[1]} | {tablero[2]}")
    print("--+---+--")
    print(f"{tablero[3]} | {tablero[4]} | {tablero[5]}")
    print("--+---+--")
    print(f"{tablero[6]} | {tablero[7]} | {tablero[8]}")
    print()

def verificar_ganador(tablero, jugador):
    # Combinaciones ganadoras
    combinaciones = [(0,1,2), (3,4,5), (6,7,8),  # Filas
                     (0,3,6), (1,4,7), (2,5,8),  # Columnas
                     (0,4,8), (2,4,6)]           # Diagonales
    for combo in combinaciones:
        if tablero[combo[0]] == tablero[combo[1]] == tablero[combo[2]] == jugador:
            return True
    return False

def movimientos_restantes(tablero):
    return [i for i in range(9) if tablero[i] == ' ']

def minimax(tablero, profundidad, es_maximizador):
    if verificar_ganador(tablero, 'X'):
        return -1  # Usuario gana
    if verificar_ganador(tablero, 'O'):
        return 1  # IA gana
    if not movimientos_restantes(tablero):
        return 0  # Empate

    if es_maximizador:
        mejor_puntuacion = -float('inf')
        for movimiento in movimientos_restantes(tablero):
            tablero[movimiento] = 'O'
            puntuacion = minimax(tablero, profundidad + 1, False)
            tablero[movimiento] = ' '
            mejor_puntuacion = max(mejor_puntuacion, puntuacion)
        return mejor_puntuacion
    else:
        mejor_puntuacion = float('inf')
        for movimiento in movimientos_restantes(tablero):
            tablero[movimiento] = 'X'
            puntuacion = minimax(tablero, profundidad + 1, True)
            tablero[movimiento] = ' '
            mejor_puntuacion = min(mejor_puntuacion, puntuacion)
        return mejor_puntuacion

def mejor_movimiento(tablero):
    mejor_puntuacion = -float('inf')
    mejor_mov = None
    for movimiento in movimientos_restantes(tablero):
        tablero[movimiento] = 'O'
        puntuacion = minimax(tablero, 0, False)
        tablero[movimiento] = ' '
        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_mov = movimiento
    return mejor_mov

def boton_click(boton, index):
    if tablero[index] == ' ' and not verificar_ganador(tablero, 'O'):
        tablero[index] = 'X'
        boton.config(text='X')
        if verificar_ganador(tablero, 'X'):
            messagebox.showinfo("Tic-Tac-Toe", "¡Felicidades! Ganaste.")
            resetear_tablero()
        elif not movimientos_restantes(tablero):
            messagebox.showinfo("Tic-Tac-Toe", "Empate.")
            resetear_tablero()
        else:
            movimiento_ia = mejor_movimiento(tablero)
            tablero[movimiento_ia] = 'O'
            botones[movimiento_ia].config(text='O')
            if verificar_ganador(tablero, 'O'):
                messagebox.showinfo("Tic-Tac-Toe", "La IA ha ganado.")
                resetear_tablero()

def resetear_tablero():
    global tablero
    tablero = [' ' for _ in range(9)]
    for boton in botones:
        boton.config(text=' ')

# Crear ventana
ventana = tk.Tk()
ventana.title("Tic-Tac-Toe con IA")

# Crear botones para el tablero
botones = []
for i in range(9):
    boton = tk.Button(ventana, text=' ', font=('Arial', 20), width=5, height=2,
                      command=lambda i=i: boton_click(botones[i], i))
    boton.grid(row=i//3, column=i%3)
    botones.append(boton)

ventana.mainloop()
