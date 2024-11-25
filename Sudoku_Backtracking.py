import time
import random
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
# Comentarios adicionales:
# - Asegúrate de tener Matplotlib y NumPy instalados en tu entorno de Python.
#   Puedes instalar estas bibliotecas usando 'pip install matplotlib numpy'.
# - Para la animación y el guardado en formato GIF, ImageMagick es una herramienta externa que Matplotlib usa.
# - Si prefieres no usar ImageMagick, puedes guardar la animación en otros formatos como MP4 usando otros 'writers'.
#   Por ejemplo, puedes usar 'ffmpeg' si tienes 'ffmpeg' instalado en tu sistema.
#   Para instalar ffmpeg, sigue las instrucciones en https://ffmpeg.org/download.html.
# - El archivo GIF generado estará en el mismo directorio en el que se ejecuta el código.
#   Si no lo ves, revisa que el código se haya ejecutado correctamente y que tengas permisos de escritura en el directorio.
#JAVIER RODRIGUEZ RODRIGUEZ 230300966
# Parámetros globales
imagenes = []

# Función para dibujar el Sudoku
def dibujar_sudoku(tablero, paso=None, finalizado=False):
    fig, ax = plt.subplots(figsize=(6, 6), dpi=120)  # Ajustar DPI para mejor calidad
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_facecolor("white")

    # Dibujar líneas del Sudoku
    for i in range(10):
        ancho = 3 if i % 3 == 0 else 1  # Líneas gruesas para cuadrantes
        ax.plot([0, 9], [i, i], color="black", lw=ancho)
        ax.plot([i, i], [0, 9], color="black", lw=ancho)

    # Dibujar los números en el tablero
    for fila in range(9):
        for col in range(9):
            num = tablero[fila][col]
            if num != 0:
                ax.text(
                    col + 0.5,
                    8.5 - fila,
                    str(num),
                    ha="center",
                    va="center",
                    fontsize=18,  # Aumentar tamaño de fuente
                    color="green" if finalizado else "black",
                    fontweight="bold",  # Hacer los números más destacados
                )

    # Agregar paso o mensaje final
    if finalizado:
        ax.text(
            4.5,
            -0.5,
            "Sudoku Terminado",
            fontsize=18,
            color="green",
            ha="center",
            va="center",
            weight="bold",
        )
    elif paso is not None:
        ax.text(
            4.5,
            -0.5,
            f"Paso: {paso}",
            fontsize=14,
            color="blue",
            ha="center",
            va="center",
        )

    # Convertir el canvas a imagen usando buffer_rgba()
    fig.canvas.draw()
    buffer = fig.canvas.buffer_rgba()
    image = Image.frombuffer(
        "RGBA",
        fig.canvas.get_width_height(),
        buffer,
        "raw",
        "RGBA",
        0,
        1
    )
    imagenes.append(image.convert("RGB"))  # Convertir a RGB para compatibilidad con GIF
    plt.close(fig)


# Función para verificar si un número es válido
def es_valido(tablero, fila, col, num):
    if num in tablero[fila]:  # Verificar fila
        return False
    if num in (tablero[i][col] for i in range(9)):  # Verificar columna
        return False
    sub_fila, sub_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(sub_fila, sub_fila + 3):  # Verificar subcuadrícula
        for j in range(sub_col, sub_col + 3):
            if tablero[i][j] == num:
                return False
    return True

# Algoritmo Backtracking para resolver el Sudoku
def resolver_sudoku(tablero):
    pasos = 0
    def backtrack():
        nonlocal pasos
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:
                    for num in range(1, 10):
                        if es_valido(tablero, fila, col, num):
                            tablero[fila][col] = num
                            pasos += 1
                            dibujar_sudoku(tablero, paso=pasos)  # Dibujar progreso
                            if backtrack():
                                return True
                            tablero[fila][col] = 0
                    return False
        return True

    if backtrack():
        dibujar_sudoku(tablero, finalizado=True)  # Tablero final
        return True
    return False

# Generar un tablero completo válido
def generar_tablero_completo():
    tablero = [[0] * 9 for _ in range(9)]
    def backtrack():
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if es_valido(tablero, fila, col, num):
                            tablero[fila][col] = num
                            if backtrack():
                                return True
                            tablero[fila][col] = 0
                    return False
        return True
    backtrack()
    return tablero

# Eliminar números del tablero para crear un Sudoku incompleto
def generar_sudoku_aleatorio(completado, celdas_a_vaciar=40):
    sudoku = [fila[:] for fila in completado]
    vaciar = set()
    while len(vaciar) < celdas_a_vaciar:
        fila = random.randint(0, 8)
        col = random.randint(0, 8)
        vaciar.add((fila, col))
    for fila, col in vaciar:
        sudoku[fila][col] = 0
    return sudoku

# Generar GIF
def generar_gif(nombre_archivo="sudoku_resuelto.gif"):
    imagenes[0].save(
        nombre_archivo,
        save_all=True,
        append_images=imagenes[1:],
        duration=100,
        loop=1
    )
    print(f"GIF guardado como {nombre_archivo}")

# Ejemplo de uso
if __name__ == "__main__":
    print("Generando Sudoku Aleatorio...")
    tablero_completo = generar_tablero_completo()
    sudoku = generar_sudoku_aleatorio(tablero_completo)

    print("Resolviendo Sudoku...")
    dibujar_sudoku(sudoku)  # Tablero inicial
    start_time = time.time()
    if resolver_sudoku(sudoku):
        print("Sudoku Resuelto.")
    else:
        print("No se encontró solución.")
    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.6f} segundos")

    generar_gif()
