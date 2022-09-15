CONNECT = 4

EMPTY_CELL = 0
FIRST_PLAYER = 1
SECOND_PLAYER = 2
ROWS = 7
COLUMNS = 7
Symbols = {
    EMPTY_CELL: "_",
    FIRST_PLAYER: "x",
    SECOND_PLAYER: "o"
}
CountDirection = {
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
    "up_left": (-1, -1),
    "up_right": (-1, 1),
    "down_left": (1, -1),
    "down_right": (1, 1)
}
board = [] # 2D list, rows of columns
spots_left = 0
spots_left_per_column = [] # list, columns
latest_piece = {} # dict {row, column}
current_piece = FIRST_PLAYER

def main():
    reset()
    print_title()

    while(True):
        print_board()

        column = get_column_from_player()
        if not is_valid_column(column):
            print_invalid_column()
            continue

        successful = insert_piece_into_board(column)
        if not successful:
            print_column_full()
            continue

        draw = check_for_draw()
        if draw:
            print_board()
            print_draw()
            break

        win = check_for_win()
        if win:
            print_board()
            print_win()
            break

        next_player()


def reset():
    reset_board()
    reset_spots_left()
    reset_current_piece()

def reset_board():
    global board
    board = [[0 for i in range(COLUMNS)] for i in range(ROWS)]

def reset_spots_left():
    global spots_left_per_column, spots_left
    spots_left = ROWS * COLUMNS
    spots_left_per_column = [ROWS for i in range(COLUMNS)]

def reset_current_piece():
    global current_piece
    current_piece = FIRST_PLAYER

def get_symbol(row, column):
    return Symbols[board[row][column]]

def insert_piece_into_board(column):
    global latest_piece, spots_left
    if can_place_in_column(column):
        row = spots_left_per_column[column] = spots_left_per_column[column] - 1
        spots_left -= 1
        board[row][column] = current_piece
        latest_piece = {
            "row": row,
            "column": column
        }
        return True
    return False

def can_place_in_column(column):
    return spots_left_per_column[column] > 0

def is_valid_column(column):
    return 0 <= column < COLUMNS

def is_valid_row(row):
    return 0 <= row < ROWS

def is_current_piece(row, column):
    return get_piece_in_board(row, column) == current_piece

def get_piece_in_board(row, column):
    if is_valid_row(row) and is_valid_column(column):
        return board[row][column]
    return EMPTY_CELL

def next_player():
    global current_piece
    current_piece = SECOND_PLAYER if current_piece == FIRST_PLAYER else FIRST_PLAYER

def get_column_from_player():
    player_input = input(f"Player {current_piece}: Choose a column (1-7): ")
    try:
        player_input = int(player_input) - 1
        return player_input
    except:
        return -1

def print_board():
    print()
    for row in range(ROWS):
        for column in range(COLUMNS):
            print(f"|{get_symbol(row, column)}", end="")
        print("|")
    for row in range(ROWS):
        print(f" {row+1}", end="")
    print("\n")

def print_title():
    print("WELCOME TO CONNECT 4!!")

def print_column_full():
    print("Sorry! That column is filled! Choose another one!")

def print_invalid_column():
    print("Sorry! That's an invalid column! Choose another one!")

def print_win():
    print(f"Player {current_piece} wins!")

def print_draw():
    print("It's a draw!")

def check_for_draw():
    return spots_left == 0

def check_for_win():
    return check_for_vertical_win() \
        or check_for_horizontal_win() \
        or check_for_diagonal_topleft_bottomright_win() \
        or check_for_diagonal_bottomleft_topright_win()

def check_for_vertical_win():
    return 1 + count_in_direction(CountDirection["down"]) >= CONNECT

def check_for_horizontal_win():
    count = 1 + count_in_direction(CountDirection["left"]) + count_in_direction(CountDirection["right"])
    return count >= CONNECT

def check_for_diagonal_topleft_bottomright_win():
    count = 1 + count_in_direction(CountDirection["up_left"]) + count_in_direction(CountDirection["down_right"])
    return count >= CONNECT

def check_for_diagonal_bottomleft_topright_win():
    count = 1 + count_in_direction(CountDirection["down_left"]) + count_in_direction(CountDirection["up_right"])
    return count >= CONNECT

def count_in_direction(direction):
    return count_in_direction_recursive(latest_piece["row"], latest_piece["column"], direction) - 1

def count_in_direction_recursive(row, column, direction):
    return 1 + count_in_direction_recursive(row + direction[0], column + direction[1], direction) \
        if is_current_piece(row, column) else 0

if __name__ == "__main__":
    main()
