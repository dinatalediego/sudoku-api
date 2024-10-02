from flask import Flask, request, jsonify

app = Flask(__name__)

# Función que resuelve el tablero de Sudoku
def resolver_sudoku(tablero):
    empty = encontrar_vacio(tablero)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if es_valido(tablero, num, row, col):
            tablero[row][col] = num

            if resolver_sudoku(tablero):
                return True

            tablero[row][col] = 0

    return False

def es_valido(tablero, num, row, col):
    # Revisa fila
    if num in tablero[row]:
        return False

    # Revisa columna
    if num in [tablero[i][col] for i in range(9)]:
        return False

    # Revisa el cuadrado 3x3
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if tablero[box_row + i][box_col + j] == num:
                return False

    return True

def encontrar_vacio(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None

@app.route('/resolver', methods=['POST'])
def resolver():
    data = request.get_json()

    if 'tablero' not in data:
        return jsonify({'error': 'No se proporcionó un tablero de Sudoku.'}), 400

    tablero = data['tablero']

    if len(tablero) != 9 or any(len(row) != 9 for row in tablero):
        return jsonify({'error': 'El tablero debe ser de 9x9.'}), 400

    if resolver_sudoku(tablero):
        return jsonify({'tablero_resuelto': tablero})
    else:
        return jsonify({'error': 'No se pudo resolver el tablero.'}), 400

@app.route('/')
def index():
    return "Bienvenido a la API de Sudoku"

if __name__ == '__main__':
    app.run()
